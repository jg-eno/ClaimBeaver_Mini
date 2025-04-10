"""
API routes for the ClaimBeaver application.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import os

from app.models.schemas import Question, Response
from app.api.inquiry_agent import InquiryAgent

# Create FastAPI app
app = FastAPI(title="ClaimBeaver API", description="Healthcare Claims Inquiry System")

# Enable CORS to allow the web page to access the API endpoint.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a dependency for the inquiry agent
def get_inquiry_agent():
    """
    Dependency to get the inquiry agent.
    
    Returns:
        InquiryAgent: Configured inquiry agent
    """
    model_type = os.getenv("LLM_TYPE", "gemini")
    model_name = os.getenv("LLM_MODEL_NAME", None)
    api_base = os.getenv("LLM_API_BASE", None)
    
    return InquiryAgent(model_type, model_name, api_base)

# API endpoint for processing questions.
@app.post("/ask", response_model=Response)
async def ask_question(q: Question, agent: InquiryAgent = Depends(get_inquiry_agent)):
    """
    Process a healthcare inquiry.
    
    Args:
        q (Question): Question model with the user's inquiry
        agent (InquiryAgent): Inquiry agent dependency
        
    Returns:
        Response: Response model with the answer
    """
    result = agent.ask(q.question)
    return Response(response=result)

# Serve the index.html file at the root URL.
@app.get("/", response_class=HTMLResponse)
async def get_index():
    """
    Serve the main HTML interface.
    
    Returns:
        FileResponse: HTML file response
    """
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "static")
    return FileResponse(os.path.join(static_dir, "index.html"))
