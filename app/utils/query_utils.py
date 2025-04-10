"""
Utility functions for processing SQL queries.
"""
import re

def parse_sql_query(query_text: str) -> str:
    """
    Cleans up the SQL query output by removing markdown formatting (code fences)
    and any extra characters, ensuring the query is executable.
    
    Args:
        query_text (str): Raw SQL query text, potentially with markdown formatting
    
    Returns:
        str: Cleaned SQL query ready for execution
    """
    pattern = r"```(?:sql)?\s*(.*?)\s*```"
    match = re.search(pattern, query_text, re.DOTALL | re.IGNORECASE)
    if match:
        query_text = match.group(1)
    return query_text.strip()

def run_query(db, query_text):
    """
    Run a SQL query on the database.
    
    Args:
        db: Database instance
        query_text (str): SQL query to execute
    
    Returns:
        str: Query results
    """
    formatted_query = parse_sql_query(query_text)
    print("Query:", formatted_query)
    return db.run(formatted_query)
