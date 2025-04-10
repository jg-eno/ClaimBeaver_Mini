"""
Healthcare inquiry agent module.
"""
from functools import partial
from app.database.db_config import db, get_schema
from app.utils.query_utils import run_query
from app.utils.llm_service import LLMService

class InquiryAgent:
    """
    Agent for handling healthcare inquiries.
    """
    def __init__(self, model_type="openai", model_name=None, api_base=None):
        """
        Initialize the inquiry agent.
        
        Args:
            model_type (str): Type of model to use ('openai' or 'gemini')
            model_name (str, optional): Name of the model to use
            api_base (str, optional): Base URL for API requests
        """
        self.llm_service = LLMService(model_type, model_name, api_base)
        self.sql_chain = self.llm_service.create_sql_chain(get_schema)
        
        # Create a partial function that already knows about the database
        self.db_run_query = partial(run_query, db)
        
        self.answer_chain = self.llm_service.create_answer_chain(
            get_schema, 
            self.db_run_query, 
            self.sql_chain
        )
    
    def ask(self, question):
        """
        Process a healthcare inquiry.
        
        Args:
            question (str): User's healthcare question
            
        Returns:
            str: Answer to the user's question
        """
        return self.answer_chain.invoke({"question": question}).content
