import re
from sql_cleaner.processor.handler import SQLHandler
from typing import List


class DeleteHandler(SQLHandler):
    """
    Handler to remove DELETE statements targeting specified tables.
    """
    
    def process(self, content: str, tables_to_process: List[str]) -> str:
        """
        Remove DELETE statements that target tables in the tables_to_process list.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            SQL content with relevant DELETE statements removed
        """
        if not tables_to_process:
            return content
        
        # Split content into statements
        statements = self._split_into_statements(content)
        
        # Process each statement
        filtered_statements = []
        for statement in statements:
            statement = statement.strip()
            if not statement:
                continue
                
            # Check if it's a DELETE targeting a table to process
            if self._is_delete_for_target_table(statement, tables_to_process):
                continue  # Skip this statement
                
            filtered_statements.append(statement)
        
        # Join statements back together
        result = " ".join(filtered_statements)
        
        return result
    
    def _split_into_statements(self, content: str) -> List[str]:
        """
        Split SQL content into statements.
        Handles SQL statements separated by semicolons and new statements on separate lines.
        """
        statements = []
        
        # Split the content by lines
        lines = content.split('\n')
        current_statement = []
        in_statement = False
        statement_type = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line starts with a SQL keyword
            is_new_statement = False
            upper_line = line.upper()
            
            for keyword in ["SELECT", "UPDATE", "DELETE", "INSERT", "CREATE", "ALTER", "DROP"]:
                if upper_line.startswith(keyword) or re.match(r'^\s*' + keyword, upper_line):
                    # This is a new statement
                    is_new_statement = True
                    
                    # If we were already in a statement, save it
                    if in_statement and current_statement:
                        statements.append(' '.join(current_statement))
                        current_statement = []
                    
                    in_statement = True
                    statement_type = keyword
                    break
            
            # Add the line to the current statement
            current_statement.append(line)
            
            # If line ends with semicolon, it's the end of the statement
            if line.endswith(';'):
                if in_statement and current_statement:
                    statements.append(' '.join(current_statement))
                    current_statement = []
                    in_statement = False
        
        # Don't forget the last statement if there is one
        if current_statement:
            statements.append(' '.join(current_statement))
        
        # If we couldn't split by statements, just return the original content
        if not statements:
            return [content]
            
        return statements
    
    def _is_delete_for_target_table(self, statement: str, tables_to_process: List[str]) -> bool:
        """
        Check if a statement is a DELETE statement targeting a table in tables_to_process.
        
        Args:
            statement: SQL statement to check
            tables_to_process: List of tables to process
            
        Returns:
            True if the statement is a DELETE for a target table, False otherwise
        """
        # Convert to lowercase for case-insensitive matching
        stmt_lower = statement.lower().strip()
        
        # Check if it's a DELETE statement
        if not stmt_lower.startswith("delete"):
            return False
            
        # Extract the table name using regex
        match = re.search(r"delete\s+from\s+([^\s;(]+)", stmt_lower)
        if not match:
            return False
            
        table_name = match.group(1)
        
        # Check if table name matches any in the list (case-insensitive)
        return any(table.lower() == table_name for table in tables_to_process) 