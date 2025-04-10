"""
Pydantic models for request and response validation.
"""
from pydantic import BaseModel

class Question(BaseModel):
    """
    Model for question requests.
    """
    question: str

class Response(BaseModel):
    """
    Model for API responses.
    """
    response: str
