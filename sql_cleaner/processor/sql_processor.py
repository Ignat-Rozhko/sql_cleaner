from typing import List, Set

from sql_cleaner.processor.handler import SQLHandler
from sql_cleaner.processor.insert_handler import InsertHandler
from sql_cleaner.processor.where_handler import WhereHandler
from sql_cleaner.processor.utils import extract_table_names


class SQLProcessor:
    """
    Main processor that chains together handlers to process SQL content.
    """
    
    def __init__(self):
        """Initialize the chain of responsibility for SQL processing."""
        # Create handlers
        insert_handler = InsertHandler()
        where_handler = WhereHandler()
        
        # Set up the chain
        insert_handler.set_next(where_handler)
        
        # The first handler in the chain
        self.handler = insert_handler
    
    def extract_table_names(self, content: str) -> Set[str]:
        """
        Extract a list of table names from the SQL content.
        
        Args:
            content: SQL content as a string
            
        Returns:
            Set of table names
        """
        return extract_table_names(content)
    
    def process_sql_content(self, content: str, tables_to_process: List[str] = None) -> str:
        """
        Process SQL content by applying all handlers in the chain.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            Processed SQL content
        """
        if not content:
            return content
        
        if not tables_to_process:
            tables_to_process = list(self.extract_table_names(content))
        
        # Process the content through the chain of handlers
        return self.handler.handle(content, tables_to_process) 