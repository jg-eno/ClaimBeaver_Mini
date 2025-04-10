"""
LLM service module providing different language model implementations.
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMService:
    """
    Service for handling different LLM implementations.
    """
    def __init__(self, model_type="gemini", model_name=None, api_base=None):
        """
        Initialize the LLM service.
        
        Args:
            model_type (str): Type of model to use ('openai' or 'gemini')
            model_name (str, optional): Name of the model to use
            api_base (str, optional): Base URL for API requests
        """
        self.model_type = model_type
        
        # Try to initialize the requested model type, fall back to the other if it fails
        try:
            self._initialize_model(model_type, model_name, api_base)
        except Exception as e:
            print(f"Error initializing {model_type} model: {str(e)}")
            print(f"Trying fallback model type...")
            
            # If the requested model type fails, try the other one
            fallback_type = "openai" if model_type == "gemini" else "gemini"
            try:
                self._initialize_model(fallback_type, model_name, api_base)
                print(f"Successfully initialized fallback {fallback_type} model")
                self.model_type = fallback_type
            except Exception as fallback_error:
                print(f"Error initializing fallback model: {str(fallback_error)}")
                print("Please make sure either LM Studio is running or Google API key is valid")
                # Don't raise here, let the application continue and fail gracefully when the LLM is actually used
                self.llm = DummyLLM()
    
    def _initialize_model(self, model_type, model_name, api_base):
        """Initialize the specified model type"""
        if model_type == "gemini":
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set")
                
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model=model_name or "gemini-2.0-flash",
                temperature=0.7
            )
        elif model_type == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
                
            # For LM Studio, any non-empty string works as API key
            if api_key.lower() == 'lm-studio':
                api_key = 'sk-no-key-required'
                
            self.llm = ChatOpenAI(
                openai_api_base=api_base or "http://localhost:1234/v1",
                openai_api_key=api_key,
                model_name=model_name or "llama-3.2-3b-instruct",
                temperature=0.7
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def create_sql_chain(self, get_schema_func):
        """
        Create a chain for generating SQL queries from natural language.
        
        Args:
            get_schema_func: Function to get database schema
            
        Returns:
            Chain: LangChain chain for SQL generation
        """
        template = """Based on the table schema provided below, write only the SQL query that would answer the 
user's question:
{schema}

Question: {question}
SQL Query:"""
        prompt = ChatPromptTemplate.from_template(template)

        chain = (
            RunnablePassthrough.assign(schema=lambda x: get_schema_func())
            | prompt
            | self.llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
        )
        
        return chain
        
    def create_answer_chain(self, get_schema_func, run_query_func, sql_chain):
        """
        Create a chain for generating natural language answers from SQL results.
        
        Args:
            get_schema_func: Function to get database schema
            run_query_func: Function to run SQL queries
            sql_chain: Chain for generating SQL queries
            
        Returns:
            Chain: LangChain chain for answer generation
        """
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
            RunnablePassthrough.assign(query=sql_chain)
            .assign(
                schema=lambda x: get_schema_func(),
                response=lambda vars: run_query_func(vars["query"]),
            )
            | full_prompt
            | self.llm
        )
        
        return full_chain


class DummyLLM:
    """A dummy LLM class that returns error messages when no real LLM is available"""
    
    def bind(self, **kwargs):
        """Return self for bind operations"""
        return self
        
    def invoke(self, *args, **kwargs):
        """Return an error message when invoked"""
        return type('obj', (object,), {
            'content': "ERROR: No LLM service is available. Please make sure LM Studio is running or Google API key is valid."
        })
        
    def __call__(self, *args, **kwargs):
        """Return an error message when called"""
        return self.invoke(*args, **kwargs)
