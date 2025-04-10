"""
Database configuration module for ClaimBeaver application.
"""
from langchain_community.utilities import SQLDatabase

def get_database(connection_string=None):
    """
    Create and return a SQLDatabase instance.
    
    Args:
        connection_string (str, optional): Database connection string.
            Defaults to MySQL connection for HealthInsuraceEnquirySystem.
    
    Returns:
        SQLDatabase: Configured database instance
    """
    if connection_string is None:
        connection_string = 'mysql+pymysql://root:password@localhost:3306/HealthInsuraceEnquirySystem'
    
    return SQLDatabase.from_uri(connection_string)

# Default database instance
db = get_database()

def get_schema(database=None):
    """
    Get the schema information for the database.
    
    Args:
        database (SQLDatabase, optional): Database instance. Defaults to the global db.
    
    Returns:
        str: Database schema information
    """
    if database is None:
        database = db
    return database.get_table_info()
