from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

# Configure database connection
mysql_uri = 'mysql+pymysql://root:password@localhost:3306/HealthInsuraceEnquirySystem'
db = SQLDatabase.from_uri(mysql_uri)

# Load environment variables and setup the LLM
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(
    openai_api_base="http://192.168.47.232:1234/v1",
    openai_api_key=key,
    model_name="llama-3.2-3b-instruct"
)

def get_schema(db):
    return db.get_table_info()

def parse_sql_query(query_text: str) -> str:
    """
    Cleans up the SQL query output by removing markdown formatting (code fences)
    and any extra characters, ensuring the query is executable.
    """
    pattern = r"```(?:sql)?\s*(.*?)\s*```"
    match = re.search(pattern, query_text, re.DOTALL | re.IGNORECASE)
    if match:
        query_text = match.group(1)
    return query_text.strip()

def run_query(query_text):
    formatted_query = parse_sql_query(query_text)
    print("Query:", formatted_query)
    return db.run(formatted_query)

def ask(question):
    # Step 1: Generate the SQL query from the question and schema.
    template = """Based on the table schema provided below, write only the SQL query that would answer the 
user's question:
{schema}

Question: {question}
SQL Query:"""
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        RunnablePassthrough.assign(schema=lambda x: get_schema(db))
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

    # Step 2: Generate the final natural language answer using the question, SQL query, and SQL response.
    # Modified prompt to avoid extra introductory text.
    full_template = """You are a HealthCare Claims Inquiry Agent. Provide a clear, concise natural language answer 
to the query below. Do not include extra explanatory text.
Table Schema:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
Answer:"""
    full_prompt = ChatPromptTemplate.from_template(full_template)

    full_chain = (
        RunnablePassthrough.assign(query=chain)
        .assign(
            schema=lambda x: get_schema(db),
            response=lambda vars: run_query(vars["query"]),
        )
        | full_prompt
        | llm
    )

    return full_chain.invoke({"question": question}).content

# Create FastAPI app
app = FastAPI()

# Enable CORS to allow the web page to access the API endpoint.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for the /ask endpoint.
class Question(BaseModel):
    question: str

# API endpoint for processing questions.
@app.post("/ask")
async def ask_question(q: Question):
    result = ask(q.question)
    return {"response": result}

# Serve the index.html file at the root URL.
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
