import re
from typing import Dict, List, Tuple

from sql_cleaner.processor.handler import SQLHandler
from sql_cleaner.processor.utils import split_into_statements, split_with_nested_commas, get_table_id_column


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
            reference_column = get_table_id_column(table_name)
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
        # Create a clean/normalized version for parsing
        clean_stmt = re.sub(r'\s+', ' ', statement)
        
        # Extract column list from the INSERT statement
        column_match = re.search(r'insert\s+into\s+\w+(?:\.?\w+)?\s*\(([^)]+)\)', clean_stmt, re.IGNORECASE)
        if not column_match:
            return statement
            
        column_str = column_match.group(1)
        columns = [col.strip() for col in split_with_nested_commas(column_str)]
        
        # Check for multi-value INSERT
        if 'values' in clean_stmt.lower() and re.search(r'\)\s*,\s*\(', clean_stmt):
            return self._process_multi_value_insert(statement, reference_column, columns)
        
        # Find the exact column by name
        reference_idx = -1
        for i, col in enumerate(columns):
            if reference_column.lower() == col.lower():
                reference_idx = i
                break
                
        if reference_idx == -1:
            return statement  # Column not found
            
        # Build new column list excluding the reference column
        new_columns = [col for i, col in enumerate(columns) if i != reference_idx]
        new_column_str = ', '.join(new_columns)
        
        # Get the prefix (everything before column list)
        prefix = statement[:statement.find('(', statement.lower().find('insert'))]
        
        # Find 'VALUES' keyword
        values_idx = statement.lower().find('values')
        if values_idx == -1:
            return statement
            
        # The part between closing column parenthesis and 'VALUES'
        middle_part = statement[statement.find(')', statement.find('(')) + 1:values_idx]
        
        # Extract values from after VALUES
        after_values = statement[values_idx + 6:].strip()
        
        # Parse values using nested parenthesis counting to find balanced closing paren
        open_count = 0
        values_end_pos = -1
        in_string = False
        string_char = None
        
        for i, char in enumerate(after_values):
            if char in ['"', "'"]:
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char and (i == 0 or after_values[i-1] != '\\'):
                    in_string = False
                    string_char = None
            
            if not in_string:
                if char == '(':
                    open_count += 1
                elif char == ')':
                    open_count -= 1
                    if open_count == 0:
                        values_end_pos = i
                        break
        
        if values_end_pos == -1:
            return statement  # Failed to extract values
        
        # Extract values content and split into individual values
        values_content = after_values[:values_end_pos].strip()
        if values_content.startswith('('):
            values_content = values_content[1:]  # Remove opening paren
        
        values = split_with_nested_commas(values_content)
        
        # Remove the value at reference_idx
        if reference_idx < len(values):
            values.pop(reference_idx)
        
        # Get what comes after the values parenthesis
        rest_of_stmt = after_values[values_end_pos+1:].strip() 
        
        # Rebuild the SQL statement
        rebuilt_sql = f"{prefix}({new_column_str}){middle_part}values ("
        rebuilt_sql += ', '.join(values)
        rebuilt_sql += ')'
        
        # Add any remaining parts (typically just a semicolon)
        if rest_of_stmt:
            rebuilt_sql += rest_of_stmt
        
        return rebuilt_sql
    
    def _process_multi_value_insert(self, statement: str, reference_column: str, columns=None) -> str:
        """
        Process a multi-value INSERT statement to remove references to the specified column.
        
        Args:
            statement: SQL statement to process
            reference_column: Column name to remove references to
            columns: Pre-parsed column list if available
            
        Returns:
            Processed SQL statement
        """
        # Create a clean/normalized version for parsing
        clean_stmt = re.sub(r'\s+', ' ', statement)
        
        # Extract column list if not provided
        if columns is None:
            column_match = re.search(r'insert\s+into\s+\w+(?:\.?\w+)?\s*\(([^)]+)\)', clean_stmt, re.IGNORECASE)
            if not column_match:
                return statement
                
            column_str = column_match.group(1)
            columns = [col.strip() for col in split_with_nested_commas(column_str)]
        
        # Find the exact column by name
        reference_idx = -1
        for i, col in enumerate(columns):
            if reference_column.lower() == col.lower():
                reference_idx = i
                break
                
        if reference_idx == -1:
            return statement  # Column not found
            
        # Remove the column from the column list
        new_columns = [col for i, col in enumerate(columns) if i != reference_idx]
        new_column_str = ', '.join(new_columns)
        
        # Get the parts of the SQL statement
        prefix = statement[:statement.find('(', statement.lower().find('insert'))]
        
        # Find 'VALUES' keyword
        values_idx = statement.lower().find('values')
        if values_idx == -1:
            return statement
            
        # The part between closing column parenthesis and 'VALUES'
        middle_part = statement[statement.find(')', statement.find('(')) + 1:values_idx]
        
        # Process the multi-value section
        after_values = statement[values_idx + 6:].strip()
        
        # Trace through each value set
        value_sets = []
        open_count = 0
        current_set = ""
        in_string = False
        string_char = None
        
        i = 0
        while i < len(after_values):
            char = after_values[i]
            
            # Handle string boundaries
            if char in ['"', "'"]:
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char and (i == 0 or after_values[i-1] != '\\'):
                    in_string = False
                    string_char = None
            
            # Process parentheses
            if not in_string:
                if char == '(':
                    if open_count == 0:
                        # Start of a new value set
                        current_set = ""
                    open_count += 1
                elif char == ')':
                    open_count -= 1
                    if open_count == 0:
                        # End of a value set
                        value_sets.append(current_set)
                        current_set = ""
                        
                        # Check if there are more value sets
                        j = i + 1
                        while j < len(after_values) and after_values[j] in ', \t\n\r':
                            j += 1
                        
                        if j < len(after_values) and after_values[j] == '(':
                            # There's another value set
                            i = j - 1  # Will be incremented in the loop
                        else:
                            # No more value sets
                            rest_of_stmt = after_values[i+1:].strip()
                            break
            
            # Add character to current set if we're in one
            if open_count > 0 and char != '(' and (open_count > 1 or char != ')'):
                current_set += char
            
            i += 1
        
        # Process each value set to remove the reference column's value
        processed_sets = []
        for value_set in value_sets:
            values = split_with_nested_commas(value_set)
            
            # Remove the reference value
            if reference_idx < len(values):
                values.pop(reference_idx)
                
            processed_sets.append(f"({', '.join(values)})")
        
        # Get what's left after the last value set
        rest_of_stmt = after_values[after_values.rfind(')')+1:].strip()
        
        # Rebuild the SQL with modified column list and value sets
        rebuilt_sql = f"{prefix}({new_column_str}){middle_part}values "
        rebuilt_sql += ', '.join(processed_sets)
        
        # Add any remaining parts (typically just a semicolon)
        if rest_of_stmt:
            rebuilt_sql += " " + rest_of_stmt
            
        return rebuilt_sql 