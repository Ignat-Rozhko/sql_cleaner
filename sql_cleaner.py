import os
import re
import pathlib
from typing import List, Dict, Tuple, Set


class SQLFileFinder:
    """Finds all SQL files in the provided directory recursively."""
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
    
    def find_sql_files(self) -> List[pathlib.Path]:
        """
        Recursively find all SQL files in the root directory.
        
        Returns:
            List of Path objects representing SQL files.
        """
        sql_files = []
        root_path = pathlib.Path(self.root_dir)
        
        for file_path in root_path.glob("**/*.sql"):
            if file_path.is_file():
                sql_files.append(file_path)
        
        return sql_files


class SQLProcessor:
    """Processes SQL content to modify it according to specified rules."""
    
    def extract_table_names(self, content: str) -> Set[str]:
        """
        Extract a list of table names from the SQL content.
        
        Args:
            content: SQL content as a string
            
        Returns:
            Set of table names
        """
        # Simple approach - improve this with a more robust SQL parser if needed
        tables = set()
        
        # Find table names from "insert into TABLE" statements
        insert_pattern = re.compile(r'insert\s+into\s+(\w+)', re.IGNORECASE)
        tables.update(match.group(1).lower() for match in insert_pattern.finditer(content))
        
        return tables
    
    def _preprocess_content(self, content: str) -> str:
        """
        Preprocess the SQL content to make it easier to parse.
        
        Args:
            content: SQL content as a string
            
        Returns:
            Preprocessed content
        """
        # Make sure each statement is on its own line(s)
        # Put a newline after each semicolon if there's not one already
        content = re.sub(r';(\s*)(?!$)', r';\n\1', content)
        
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        return content
    
    def _split_sql_content(self, content: str) -> List[Dict]:
        """
        Split SQL content into individual SQL statements.
        
        Args:
            content: SQL content as a string
            
        Returns:
            List of dictionaries with information about each statement
        """
        # Preprocess the content to ensure each statement is separated
        content = self._preprocess_content(content)
        
        statements = []
        # Split the content into lines
        content_lines = content.split('\n')
        i = 0
        
        # We'll track SQL statement blocks
        in_statement = False
        statement_start_line = -1
        current_statement_lines = []
        
        while i < len(content_lines):
            line = content_lines[i]
            stripped_line = line.strip()
            
            # Skip empty lines or comment lines if not in a statement
            if (not stripped_line or stripped_line.startswith('--')) and not in_statement:
                i += 1
                continue
            
            # If this is the start of an INSERT statement, track it
            insert_match = re.match(r'^\s*insert\s+into\s+', line, re.IGNORECASE)
            
            if not in_statement and insert_match:
                in_statement = True
                statement_start_line = i
                current_statement_lines = [line]
            # Continue collecting lines for an existing statement
            elif in_statement:
                current_statement_lines.append(line)
                
                # Check if statement ends with a semicolon
                if ';' in line:
                    # We have a complete statement
                    statement_text = '\n'.join(current_statement_lines)
                    
                    # Calculate the position in the original content
                    start_pos = 0
                    for j in range(statement_start_line):
                        start_pos += len(content_lines[j]) + 1  # +1 for newline
                    
                    end_pos = start_pos + len(statement_text)
                    
                    # Identify the table being inserted into
                    table_match = re.search(r'insert\s+into\s+(\w+)', statement_text, re.IGNORECASE)
                    if table_match:
                        table_name = table_match.group(1).lower()
                        
                        # Check if it's a multi-value insert
                        has_multiple_values = self._has_multiple_values(statement_text)
                        
                        statements.append({
                            'start_line': statement_start_line,
                            'end_line': i,
                            'start_pos': start_pos,
                            'end_pos': start_pos + len(statement_text),
                            'text': statement_text,
                            'table': table_name,
                            'has_multiple_values': has_multiple_values
                        })
                    
                    # Reset for the next statement
                    in_statement = False
                    statement_start_line = -1
                    current_statement_lines = []
            
            i += 1
        
        return statements
    
    def _has_multiple_values(self, statement: str) -> bool:
        """
        Check if an INSERT statement has multiple value sets.
        
        Args:
            statement: SQL statement as a string
            
        Returns:
            True if the statement has multiple value sets, False otherwise
        """
        # Look for a pattern like "VALUES (...), (...);"
        # First, strip all whitespace and newlines to simplify the search
        compact_stmt = re.sub(r'\s+', ' ', statement).lower()
        
        # Find the VALUES keyword
        values_match = re.search(r'values\s*\(', compact_stmt)
        if not values_match:
            return False
        
        # Find closing parentheses followed by commas and opening parentheses
        # This indicates multiple value sets
        return bool(re.search(r'\)\s*,\s*\(', compact_stmt[values_match.end():]))
    
    def _extract_value_sets(self, statement: str) -> List[str]:
        """
        Extract all value sets from a multi-value INSERT statement.
        
        Args:
            statement: SQL statement as a string
            
        Returns:
            List of value sets as strings
        """
        # Find the VALUES section
        values_match = re.search(r'values\s*\(', statement, re.IGNORECASE)
        if not values_match:
            return []
        
        # Extract everything after VALUES until the semicolon
        values_section = statement[values_match.end()-1:]  # Include the opening parenthesis
        
        # Split based on level-0 parentheses
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
        
        return value_sets
    
    def find_direct_insert_statements(self, content: str, table_name: str) -> List[Dict]:
        """
        Find INSERT statements directly into the specified table.
        
        Args:
            content: SQL content as a string
            table_name: Name of the table to find insert statements for
            
        Returns:
            List of dictionaries with information about direct insert statements
        """
        table_name = table_name.lower()
        # Use a more precise regex pattern to find INSERT statements for the specific table
        pattern = rf'insert\s+into\s+(?:public\.)?{table_name}\s*\('
        
        statements = []
        for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
            # Find the statement start position
            start_pos = match.start()
            
            # Find the corresponding semicolon that ends this statement
            # Search from the match position to the end of the content
            semicolon_pos = content.find(';', start_pos)
            if semicolon_pos == -1:
                continue  # No semicolon found, invalid SQL
                
            # Extract the complete statement
            statement_text = content[start_pos:semicolon_pos + 1]
            
            # Determine line numbers
            text_before = content[:start_pos]
            start_line = text_before.count('\n')
            text_up_to_end = content[:semicolon_pos]
            end_line = text_up_to_end.count('\n')
            
            # Check if it's a multi-value insert
            has_multiple_values = self._has_multiple_values(statement_text)
            
            statements.append({
                'start_line': start_line,
                'end_line': end_line,
                'start_pos': start_pos,
                'end_pos': semicolon_pos + 1,
                'text': statement_text,
                'table': table_name,
                'has_multiple_values': has_multiple_values
            })
                    
        return statements
    
    def find_reference_insert_statements(self, content: str, table_name: str) -> List[Dict]:
        """
        Find INSERT statements that reference the specified table in another table's insert.
        
        Args:
            content: SQL content as a string
            table_name: Name of the table being referenced
            
        Returns:
            List of dictionaries with information about the reference inserts
        """
        table_name = table_name.lower()
        table_id_pattern = rf'{table_name}_id'
        
        # First, find all INSERT statements
        reference_inserts = []
        
        # Find all INSERT statements in the content
        insert_pattern = r'insert\s+into\s+(?:public\.)?(\w+)\s*\('
        for insert_match in re.finditer(insert_pattern, content, re.IGNORECASE | re.MULTILINE):
            # Skip if this is a direct insert into the target table
            insert_table = insert_match.group(1).lower()
            if insert_table == table_name:
                continue
                
            # Find the statement start position
            start_pos = insert_match.start()
            
            # Find the corresponding semicolon that ends this statement
            semicolon_pos = content.find(';', start_pos)
            if semicolon_pos == -1:
                continue  # No semicolon found, invalid SQL
                
            # Extract the complete statement
            statement_text = content[start_pos:semicolon_pos + 1]
            
            # Check if it references the target table
            if not re.search(table_id_pattern, statement_text, re.IGNORECASE):
                continue
                
            # Extract column list
            column_match = re.search(r'insert\s+into\s+\w+\s*\((.*?)\)', statement_text, re.IGNORECASE | re.DOTALL)
            if not column_match:
                continue
                
            # Get the column list
            columns = column_match.group(1)
            column_list = [c.strip() for c in self._split_with_nested_commas(columns)]
            
            # Find the index of the reference column
            table_id_index = -1
            for idx, col in enumerate(column_list):
                if re.search(table_id_pattern, col, re.IGNORECASE):
                    table_id_index = idx
                    break
                    
            if table_id_index >= 0:
                # Determine line numbers
                text_before = content[:start_pos]
                start_line = text_before.count('\n')
                text_up_to_end = content[:semicolon_pos]
                end_line = text_up_to_end.count('\n')
                
                # Check if it's a multi-value insert
                has_multiple_values = self._has_multiple_values(statement_text)
                
                reference_inserts.append({
                    'start_line': start_line,
                    'end_line': end_line,
                    'start_pos': start_pos,
                    'end_pos': semicolon_pos + 1,
                    'text': statement_text,
                    'table': insert_table,
                    'column_index': table_id_index,
                    'column_list': column_list,
                    'has_multiple_values': has_multiple_values
                })
                
        return reference_inserts
    
    def remove_direct_insert(self, content: str, stmt_info: Dict) -> str:
        """
        Remove a direct INSERT statement from the content.
        
        Args:
            content: SQL content as a string
            stmt_info: Dictionary with information about the statement
            
        Returns:
            Modified SQL content with the statement removed
        """
        # Get the exact statement text to remove
        statement_text = stmt_info['text']
        start_pos = stmt_info['start_pos']
        end_pos = stmt_info['end_pos']
        
        # Ensure we're removing the entire statement
        before = content[:start_pos]
        after = content[end_pos:]
        
        # If there are newlines at both sides, keep only one
        if before.endswith('\n') and after.startswith('\n'):
            return before + after[1:]
        elif not before.endswith('\n') and not after.startswith('\n'):
            # Add a newline if needed
            return before + '\n' + after
            
        return before + after
    
    def remove_reference_from_insert(self, content: str, stmt_info: Dict) -> str:
        """
        Remove the reference to a table from an INSERT statement.
        
        Args:
            content: SQL content as a string
            stmt_info: Dictionary with information about the reference insert
            
        Returns:
            Modified SQL content
        """
        statement = stmt_info['text']
        column_index = stmt_info['column_index']
        
        # Extract column list
        column_match = re.search(r'insert\s+into\s+\w+\s*\((.*?)\)', statement, re.IGNORECASE | re.DOTALL)
        if not column_match:
            return content  # Can't process, return unchanged
            
        columns_str = column_match.group(1)
        columns_list = self._split_with_nested_commas(columns_str)
        
        # Remove the reference column
        if 0 <= column_index < len(columns_list):
            del columns_list[column_index]
            new_columns_str = ', '.join(columns_list)
            
            # Check if this is a multi-value INSERT
            if stmt_info.get('has_multiple_values', False):
                # Handle multi-value INSERT
                # Extract all value sets
                value_sets = self._extract_value_sets(statement)
                
                # Remove the reference value from each set
                new_value_sets = []
                for value_set in value_sets:
                    values_list = self._split_with_nested_commas(value_set[1:-1])  # Remove parentheses
                    if 0 <= column_index < len(values_list):
                        del values_list[column_index]
                        new_value_sets.append('(' + ', '.join(values_list) + ')')
                
                # Build the new statement
                table_part = re.search(r'insert\s+into\s+\w+\s*', statement, re.IGNORECASE).group(0)
                new_statement = f"{table_part}({new_columns_str}) VALUES {', '.join(new_value_sets)};"
            else:
                # Handle single-value INSERT
                values_match = re.search(r'values\s*\((.*?)\);', statement, re.IGNORECASE | re.DOTALL)
                if not values_match:
                    return content  # Can't process, return unchanged
                    
                values_str = values_match.group(1)
                values_list = self._split_with_nested_commas(values_str)
                
                # Remove the reference value
                if 0 <= column_index < len(values_list):
                    del values_list[column_index]
                    new_values_str = ', '.join(values_list)
                    
                    # Create the new statement text
                    new_statement = re.sub(
                        r'insert\s+into\s+(\w+)\s*\(.*?\)',
                        f"insert into \\1 ({new_columns_str})",
                        statement,
                        flags=re.IGNORECASE | re.DOTALL
                    )
                    
                    new_statement = re.sub(
                        r'values\s*\(.*?\);',
                        f"values ({new_values_str});",
                        new_statement,
                        flags=re.IGNORECASE | re.DOTALL
                    )
                else:
                    return content  # Invalid index, return unchanged
            
            # Replace the original statement with the new one
            return content[:stmt_info['start_pos']] + new_statement + content[stmt_info['end_pos']:]
        
        return content
    
    def remove_where_conditions(self, content: str, table_name: str) -> str:
        """
        Remove WHERE conditions that reference the specified table.
        
        Args:
            content: SQL content as a string
            table_name: Name of the table to remove from WHERE conditions
            
        Returns:
            SQL content with WHERE conditions referencing the table removed
        """
        # First, find all aliases for this table
        aliases = self._find_table_aliases(content, table_name)
        
        # Also find columns that are likely references to the table (like company_id)
        potential_reference_columns = [f"{table_name}_id"]
        
        # Process SQL statements individually for better handling
        statements = self._split_into_statements(content)
        results = []
        
        for statement in statements:
            # Skip empty statements
            if not statement.strip():
                results.append(statement)
                continue
            
            # First try to find the main SQL structure with ORDER BY outside of WHERE
            sql_structure = re.match(
                r'(.*?)\s+WHERE\s+(.+?)(?:\s+(ORDER\s+BY.+?))?(;|$)',
                statement,
                re.IGNORECASE | re.DOTALL
            )
            
            if not sql_structure:
                # No WHERE clause in this statement
                results.append(statement)
                continue
                
            before_where = sql_structure.group(1)  # Everything before WHERE
            where_conditions = sql_structure.group(2)  # The conditions part
            order_by_clause = sql_structure.group(3) or ""  # ORDER BY clause if exists
            statement_end = sql_structure.group(4)  # Semicolon or end of string
            
            # Split into individual conditions
            condition_parts = self._split_where_conditions(where_conditions)
            
            # Analyze each condition to see if it references our table
            filtered_condition_parts = []
            for condition in condition_parts:
                # Check if condition references our target table by name
                if re.search(rf'(?:^|\W){re.escape(table_name)}\.', condition, re.IGNORECASE):
                    continue
                
                # Check if condition references one of our aliases
                should_remove = False
                for alias in aliases:
                    if re.search(rf'(?:^|\W){re.escape(alias)}\.', condition, re.IGNORECASE):
                        should_remove = True
                        break
                
                # Check for potential reference columns
                for col in potential_reference_columns:
                    # Looking for table_id = '...' or alias.table_id = '...'
                    if re.search(rf'(?:^|\W)(?:\w+\.)?{re.escape(col)}\s*(?:=|!=|<>|>|<|>=|<=|IS|IN|LIKE)', 
                                 condition, re.IGNORECASE):
                        should_remove = True
                        break
                
                if should_remove:
                    continue
                
                # If we got here, keep this condition
                filtered_condition_parts.append(condition)
                
            # Build the new statement
            if not filtered_condition_parts:
                # No conditions left, remove the WHERE clause entirely
                modified_statement = before_where
                if order_by_clause:
                    modified_statement += f" {order_by_clause}"
                modified_statement += statement_end
            else:
                # Reconstruct the WHERE clause with remaining conditions
                new_where_conditions = ' AND '.join(filtered_condition_parts)
                
                # Create the new WHERE clause with proper formatting
                modified_statement = f"{before_where} WHERE {new_where_conditions}"
                if order_by_clause:
                    modified_statement += f" {order_by_clause}"
                modified_statement += statement_end
            
            results.append(modified_statement)
        
        # Join the results back into a single string
        return ''.join(results)
    
    def _split_into_statements(self, content: str) -> List[str]:
        """
        Split SQL content into individual statements.
        
        Args:
            content: SQL content as a string
            
        Returns:
            List of SQL statements
        """
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        statements = []
        current_statement = ""
        in_string = False
        string_delimiter = None
        
        i = 0
        while i < len(content):
            char = content[i]
            
            # Handle string literals
            if char in ("'", '"'):
                if not in_string:
                    in_string = True
                    string_delimiter = char
                elif string_delimiter == char and (i == 0 or content[i-1] != '\\'):
                    in_string = False
                    string_delimiter = None
            
            # Add character to current statement
            current_statement += char
            
            # Check for semicolon outside of strings
            if char == ';' and not in_string:
                statements.append(current_statement)
                current_statement = ""
            
            i += 1
        
        # Add the last statement if there is one
        if current_statement:
            statements.append(current_statement)
        
        return statements
    
    def _find_table_aliases(self, content: str, table_name: str) -> List[str]:
        """
        Find all aliases for a specified table in the SQL content.
        
        Args:
            content: SQL content as a string
            table_name: Name of the table to find aliases for
            
        Returns:
            List of aliases for the table
        """
        aliases = []
        table_name_pattern = re.escape(table_name)
        
        # Find patterns like "FROM table_name [AS] alias" or "JOIN table_name [AS] alias"
        alias_patterns = [
            # FROM table AS alias or FROM table alias
            rf'FROM\s+{table_name_pattern}(?:\s+AS)?\s+(\w+)(?:\s|,|$)',
            # JOIN table AS alias or JOIN table alias
            rf'JOIN\s+{table_name_pattern}(?:\s+AS)?\s+(\w+)(?:\s|,|$)',
            # FROM schema.table AS alias or FROM schema.table alias
            rf'FROM\s+\w+\.{table_name_pattern}(?:\s+AS)?\s+(\w+)(?:\s|,|$)',
            # JOIN schema.table AS alias or JOIN schema.table alias
            rf'JOIN\s+\w+\.{table_name_pattern}(?:\s+AS)?\s+(\w+)(?:\s|,|$)'
        ]
        
        for pattern in alias_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                aliases.append(match.group(1))
        
        return aliases
    
    def _split_where_conditions(self, where_conditions: str) -> List[str]:
        """
        Split WHERE conditions into individual condition parts, respecting parentheses and operators.
        
        Args:
            where_conditions: The conditions part of a WHERE clause
            
        Returns:
            List of individual condition parts
        """
        conditions = []
        current_condition = ""
        nesting_level = 0
        in_string = False
        string_delimiter = None
        i = 0
        
        while i < len(where_conditions):
            char = where_conditions[i]
            
            # Handle string literals
            if char in ("'", '"'):
                if not in_string:
                    in_string = True
                    string_delimiter = char
                elif string_delimiter == char and (i == 0 or where_conditions[i-1] != '\\'):
                    in_string = False
                    string_delimiter = None
            
            # Skip processing if in a string
            if in_string:
                current_condition += char
                i += 1
                continue
            
            # Handle parentheses to respect nesting
            if char == '(':
                nesting_level += 1
                current_condition += char
            elif char == ')':
                nesting_level -= 1
                current_condition += char
            
            # If at level 0, check for AND/OR operators to split the conditions
            elif nesting_level == 0 and i+2 < len(where_conditions):
                # Look for " AND " or " OR " as separators
                next_5_chars = where_conditions[i:i+5].upper()
                if next_5_chars.startswith(' AND '):
                    if current_condition.strip():
                        conditions.append(current_condition.strip())
                    current_condition = ""
                    i += 5
                    continue
                elif next_5_chars.startswith(' OR '):
                    if current_condition.strip():
                        conditions.append(current_condition.strip())
                    current_condition = ""
                    i += 4
                    continue
                else:
                    current_condition += char
            else:
                current_condition += char
            
            i += 1
        
        # Add the last condition if there is one
        if current_condition.strip():
            conditions.append(current_condition.strip())
        
        return conditions
    
    def _split_with_nested_commas(self, text: str) -> List[str]:
        """
        Split a string by commas, respecting nested structures like parentheses.
        
        Args:
            text: Text to split
            
        Returns:
            List of split items
        """
        result = []
        current = ""
        nesting_level = 0
        in_string = False
        string_delimiter = None
        
        for char in text:
            # Handle string literals to avoid counting parentheses inside strings
            if char == "'" or char == '"':
                if not in_string:
                    in_string = True
                    string_delimiter = char
                elif string_delimiter == char and not (current and current[-1] == '\\'):
                    in_string = False
                    string_delimiter = None
            
            # Only count parentheses outside of string literals
            if not in_string:
                if char in '([{':
                    nesting_level += 1
                elif char in ')]}':
                    nesting_level -= 1
                elif char == ',' and nesting_level == 0:
                    result.append(current.strip())
                    current = ""
                    continue
            
            current += char
        
        if current:
            result.append(current.strip())
            
        return result
    
    def process_sql_content(self, content: str, tables_to_process: List[str] = None) -> str:
        """
        Process SQL content according to the specified rules.
        
        Args:
            content: SQL content as a string
            tables_to_process: List of specific tables to process (if None, all tables are processed)
            
        Returns:
            Processed SQL content
        """
        if not content.strip():
            return content
            
        # Extract all table names if not provided
        all_tables = self.extract_table_names(content)
        tables = tables_to_process or list(all_tables)
        
        # If no tables to process, return the original content
        if not tables:
            return content
        
        # Convert table names to lowercase for case-insensitive comparison
        tables = [t.lower() for t in tables]
        
        modified_content = content
        content_changed = False
        
        # First pass: Remove all direct and reference inserts
        for table in tables:
            # Process each table until all occurrences are handled
            while True:
                previous_content = modified_content
                
                # Find statements for this table
                direct_inserts = self.find_direct_insert_statements(modified_content, table)
                
                # If no more direct inserts, process reference inserts
                if not direct_inserts:
                    reference_inserts = self.find_reference_insert_statements(modified_content, table)
                    
                    # If no more direct inserts and reference inserts, break the loop
                    if not reference_inserts:
                        break
                    
                    # Process reference inserts in reverse order to avoid index issues
                    for stmt in sorted(reference_inserts, key=lambda x: x['start_pos'], reverse=True):
                        modified_content = self.remove_reference_from_insert(modified_content, stmt)
                        content_changed = True
                else:
                    # Process direct inserts in reverse order to avoid index issues
                    for stmt in sorted(direct_inserts, key=lambda x: x['start_pos'], reverse=True):
                        modified_content = self.remove_direct_insert(modified_content, stmt)
                        content_changed = True
                
                # Check if the content changed in this iteration
                if previous_content == modified_content:
                    break
        
        # Second pass: Remove WHERE conditions referencing the tables
        for table in tables:
            previous_content = modified_content
            modified_content = self.remove_where_conditions(modified_content, table)
            if previous_content != modified_content:
                content_changed = True
        
        # Only clean up empty lines if we actually made changes
        if content_changed:
            # Clean up empty lines (more than 2 consecutive newlines)
            modified_content = re.sub(r'\n{3,}', '\n\n', modified_content)
        
        return modified_content


def process_sql_files(directory: str, tables_to_process: List[str] = None, tables_file: str = None):
    """
    Orchestrate SQL file finding and processing.
    
    Args:
        directory: Directory to search for SQL files
        tables_to_process: List of specific tables to process (if None, all tables are processed)
        tables_file: Path to a file containing table names to process (one per line)
    """
    finder = SQLFileFinder(directory)
    processor = SQLProcessor()
    
    # If a tables file is provided, read tables from it
    if tables_file:
        try:
            with open(tables_file, 'r', encoding='utf-8') as f:
                tables_from_file = [line.strip() for line in f if line.strip()]
            
            # If tables_to_process is also provided, combine them
            if tables_to_process:
                tables_to_process = tables_to_process + tables_from_file
            else:
                tables_to_process = tables_from_file
                
            print(f"Using {len(tables_to_process)} tables from file: {tables_file}")
        except Exception as e:
            print(f"Error reading tables file {tables_file}: {e}")
    
    sql_files = finder.find_sql_files()
    print(f"Found {len(sql_files)} SQL files to process")
    
    for file_path in sql_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"Processing {file_path}")
            modified_content = processor.process_sql_content(content, tables_to_process)
            
            # Write back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            print(f"Successfully processed {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Process SQL files to remove specified tables.')
    parser.add_argument('directory', help='Directory to search for SQL files')
    parser.add_argument('--tables', nargs='*', help='Specific tables to process')
    parser.add_argument('--tables-file', help='Path to a file containing table names to process (one per line)')
    
    args = parser.parse_args()
    
    if not args.tables and not args.tables_file:
        print("Warning: No tables specified. Either provide tables via --tables or --tables-file")
    
    process_sql_files(args.directory, args.tables, args.tables_file) 