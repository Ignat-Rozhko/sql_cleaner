import re
from typing import Dict, List, Tuple

from sql_cleaner.processor.handler import SQLHandler
from sql_cleaner.processor.utils import split_into_statements, split_with_nested_commas


class InsertHandler(SQLHandler):
    """
    Handler for processing and removing direct INSERT statements
    for specified tables and references to specified tables in other INSERT statements.
    """
    
    def process(self, content: str, tables_to_process: List[str]) -> str:
        """
        Process the SQL content to remove direct inserts and modify references.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            Processed SQL content
        """
        processed_content = content
        
        for table_name in tables_to_process:
            processed_content = self._remove_direct_inserts(processed_content, table_name)
            processed_content = self._modify_reference_inserts(processed_content, table_name)
        
        return processed_content
    
    def _remove_direct_inserts(self, content: str, table_name: str) -> str:
        """
        Remove INSERT statements directly targeting the specified table.
        
        Args:
            content: SQL content as a string
            table_name: Table name to remove inserts for
            
        Returns:
            SQL content with direct inserts removed
        """
        statements = split_into_statements(content)
        processed_statements = []
        
        for stmt in statements:
            # Check if this statement is an insert into the target table
            if not re.search(rf'insert\s+into\s+(?:public\.)?{table_name}\s*\(', stmt, re.IGNORECASE):
                processed_statements.append(stmt)
        
        # Join statements back together
        return '\n\n'.join(processed_statements)
    
    def _modify_reference_inserts(self, content: str, table_name: str) -> str:
        """
        Modify INSERT statements that reference the specified table.
        
        Args:
            content: SQL content as a string
            table_name: Table name to remove references for
            
        Returns:
            SQL content with references modified
        """
        statements = split_into_statements(content)
        processed_statements = []
        
        for stmt in statements:
            # Skip direct inserts into the table (handled by _remove_direct_inserts)
            if re.search(rf'insert\s+into\s+(?:public\.)?{table_name}\s*\(', stmt, re.IGNORECASE):
                continue
                
            # Check if this statement is an insert that references the target table
            reference_column = f"{table_name}_id"
            if reference_column.lower() in stmt.lower():
                # Process this statement to remove the reference
                stmt = self._process_reference_insert(stmt, reference_column)
                
            processed_statements.append(stmt)
        
        # Join statements back together
        return '\n\n'.join(processed_statements)
    
    def _process_reference_insert(self, statement: str, reference_column: str) -> str:
        """
        Process an INSERT statement to remove references to the specified column.
        
        Args:
            statement: SQL statement to process
            reference_column: Column name to remove references to
            
        Returns:
            Processed SQL statement
        """
        # Extract the column list and values from the INSERT statement
        column_match = re.search(r'insert\s+into\s+\w+\s*\((.*?)\)', statement, re.IGNORECASE | re.DOTALL)
        values_match = re.search(r'values\s*\((.*?)\)', statement, re.IGNORECASE | re.DOTALL)
        
        if not column_match or not values_match:
            # This is not a standard INSERT statement, return it unchanged
            return statement
        
        column_str = column_match.group(1)
        values_str = values_match.group(1)
        
        # Split columns and values
        columns = split_with_nested_commas(column_str)
        values = split_with_nested_commas(values_str)
        
        # Check for multi-value insert
        if 'values' in statement.lower() and re.search(r'\)\s*,\s*\(', statement):
            return self._process_multi_value_insert(statement, reference_column)
        
        # Find the index of the reference column
        reference_idx = -1
        for i, col in enumerate(columns):
            if reference_column.lower() in col.lower():
                reference_idx = i
                break
        
        if reference_idx == -1:
            # Reference column not found in this statement
            return statement
        
        # Remove the reference column and its value
        columns.pop(reference_idx)
        if reference_idx < len(values):
            values.pop(reference_idx)
        
        # Build the modified statement
        new_column_str = ', '.join(columns)
        new_values_str = ', '.join(values)
        
        # Replace the column list and values in the original statement
        modified_stmt = re.sub(
            r'\((.*?)\)', f'({new_column_str})', 
            statement, 
            count=1, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        modified_stmt = re.sub(
            r'values\s*\((.*?)\)', f'values ({new_values_str})', 
            modified_stmt, 
            count=1, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        return modified_stmt
    
    def _process_multi_value_insert(self, statement: str, reference_column: str) -> str:
        """
        Process a multi-value INSERT statement to remove references to the specified column.
        
        Args:
            statement: SQL statement to process
            reference_column: Column name to remove references to
            
        Returns:
            Processed SQL statement
        """
        # Extract the column list and values section from the INSERT statement
        column_match = re.search(r'insert\s+into\s+\w+\s*\((.*?)\)', statement, re.IGNORECASE | re.DOTALL)
        values_section_match = re.search(r'values\s*(.*?);', statement, re.IGNORECASE | re.DOTALL)
        
        if not column_match or not values_section_match:
            return statement
        
        column_str = column_match.group(1)
        values_section = values_section_match.group(1)
        
        # Split columns
        columns = split_with_nested_commas(column_str)
        
        # Find the index of the reference column
        reference_idx = -1
        for i, col in enumerate(columns):
            if reference_column.lower() in col.lower():
                reference_idx = i
                break
        
        if reference_idx == -1:
            # Reference column not found in this statement
            return statement
        
        # Remove the reference column
        columns.pop(reference_idx)
        
        # Extract each value set and remove the corresponding value
        value_sets = []
        current_set = ""
        nesting_level = 0
        in_string = False
        string_delimiter = None
        
        for char in values_section:
            if char == "'" or char == '"':
                if not in_string:
                    in_string = True
                    string_delimiter = char
                elif string_delimiter == char and not (current_set and current_set[-1] == '\\'):
                    in_string = False
                    string_delimiter = None
            
            if not in_string:
                if char == '(':
                    nesting_level += 1
                    if nesting_level == 1:
                        current_set = "("
                        continue
                elif char == ')':
                    nesting_level -= 1
                    if nesting_level == 0:
                        current_set += ")"
                        value_sets.append(current_set)
                        current_set = ""
                        continue
            
            if current_set or nesting_level > 0:
                current_set += char
        
        # Process each value set to remove the reference value
        processed_value_sets = []
        for value_set in value_sets:
            # Remove the parentheses
            values_str = value_set[1:-1]
            
            # Split into individual values
            values = split_with_nested_commas(values_str)
            
            # Remove the reference value
            if reference_idx < len(values):
                values.pop(reference_idx)
            
            # Rebuild the value set
            processed_value_sets.append(f"({', '.join(values)})")
        
        # Build the modified statement
        new_column_str = ', '.join(columns)
        new_values_section = ', '.join(processed_value_sets)
        
        # Replace the column list and values in the original statement
        modified_stmt = re.sub(
            r'\((.*?)\)', f'({new_column_str})', 
            statement, 
            count=1, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        modified_stmt = re.sub(
            r'values\s*(.*?);', f'values {new_values_section};', 
            modified_stmt, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        return modified_stmt 