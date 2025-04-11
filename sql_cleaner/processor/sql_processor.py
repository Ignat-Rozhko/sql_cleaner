from typing import List, Set
import re

from sql_cleaner.processor.handler import SQLHandler
from sql_cleaner.processor.insert_handler import InsertHandler
from sql_cleaner.processor.where_handler import WhereHandler
from sql_cleaner.processor.join_handler import JoinHandler
from sql_cleaner.processor.comment_removal_handler import CommentRemovalHandler
from sql_cleaner.processor.utils import extract_table_names, find_table_aliases


class SQLProcessor:
    """
    Main processor that chains together handlers to process SQL content.
    """
    
    def __init__(self):
        """Initialize the chain of responsibility for SQL processing."""
        # Create handlers
        comment_removal_handler = CommentRemovalHandler()
        insert_handler = InsertHandler()
        where_handler = WhereHandler()
        join_handler = JoinHandler(where_handler=where_handler)
        # Set up the chain
        comment_removal_handler.set_next(insert_handler)
        insert_handler.set_next(where_handler)
        where_handler.set_next(join_handler)
        
        # The first handler in the chain
        self.handler = comment_removal_handler
    
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
        
        # Skip processing if none of the target tables exist in the content
        if not self.content_contains_tables(content, tables_to_process):
            return content
        
        # Process the content through the chain of handlers
        processed_content = self.handler.handle(content, tables_to_process)
        
        # If the processed content is empty, add a comment to preserve the file
        if not processed_content.strip():
            original_table_list = ", ".join(sorted(self.extract_table_names(content)))
            return f"-- All content was removed by sql_cleaner\n-- Original tables: {original_table_list}\n"
        
        return processed_content
    
    def content_contains_tables(self, content: str, tables_to_process: List[str]) -> bool:
        """
        Check if any of the target tables exist in the content.
        
        Args:
            content: SQL content to check
            tables_to_process: List of tables to check for
            
        Returns:
            True if any target table exists in the content, False otherwise
        """
        if not tables_to_process:
            return False
        
        content_lower = content.lower()
        
        # Extract table names from the content
        tables_in_content = self.extract_table_names(content)
        
        # Check against each table to process (case insensitive)
        for table in tables_to_process:
            table_lower = table.lower()
            
            # Check if table exists in set of extracted tables
            if table_lower in tables_in_content:
                return True
            
            # Look for other references that might not be caught by extract_table_names
            if self._check_table_references(content, table):
                return True
            
            # Check for table ID references (like 'table_id' column)
            if f"{table_lower}_id" in content_lower:
                return True
        
        return False
    
    def _check_table_references(self, content: str, table_name: str) -> bool:
        """
        Check for table references in ways not caught by extract_table_names.
        
        Args:
            content: SQL content to check
            table_name: Table name to check for
            
        Returns:
            True if table is referenced, False otherwise
        """
        content_lower = content.lower()
        table_lower = table_name.lower()
        
        # Check for table name in joins
        if f"join {table_lower}" in content_lower:
            return True
        
        # Check for table name in WHERE clauses (table reference or table_id reference)
        if f"{table_lower}." in content_lower or f"{table_lower}_id" in content_lower:
            return True
        
        # Check for direct table name mentioned in FROM clause
        if re.search(rf'from\s+{table_lower}\b', content_lower):
            return True
        
        # Check for direct table name mentioned in INSERT, UPDATE, DELETE
        if re.search(rf'insert\s+into\s+{table_lower}\b', content_lower) or \
           re.search(rf'update\s+{table_lower}\b', content_lower) or \
           re.search(rf'delete\s+from\s+{table_lower}\b', content_lower):
            return True
        
        # Find table aliases and check for references through them
        for alias in find_table_aliases(content, table_name):
            if f"{alias}." in content_lower:
                return True
        
        return False 