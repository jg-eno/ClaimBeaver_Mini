"""
Main application entry point for ClaimBeaver.
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the FastAPI app from routes
from app.api.routes import app

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=port)
