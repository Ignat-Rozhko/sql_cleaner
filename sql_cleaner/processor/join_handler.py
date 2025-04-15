import re
from typing import List

from sql_cleaner.processor.handler import SQLHandler
from sql_cleaner.processor.utils import split_into_statements, find_table_aliases, get_table_id_column
from sql_cleaner.processor.where_handler import WhereHandler


class JoinHandler(SQLHandler):
    """
    Handler for processing and removing JOIN statements related to specified tables.
    Uses a WhereHandler dependency to clean up related WHERE conditions.
    """
    def __init__(self, where_handler: WhereHandler):
        """
        Initialize the JoinHandler with a WhereHandler instance.
        
        Args:
            where_handler: An instance of WhereHandler.
        """
        super().__init__()  # Call the parent class initializer
        self.where_handler = where_handler
    
    def process(self, content: str, tables_to_process: List[str]) -> str:
        """
        Process the SQL content to remove JOIN statements related to the specified tables.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            Processed SQL content
        """
        if not tables_to_process:
            return content
            
        processed_content = content
        
        for table_name in tables_to_process:
            processed_content = self._remove_direct_joins(processed_content, table_name)
            processed_content = self._remove_reference_joins(processed_content, table_name)
        
        return processed_content
    
    def _remove_direct_joins(self, content: str, table_name: str) -> str:
        """
        Remove JOIN statements directly targeting the specified table and then
        use the injected WhereHandler to clean up conditions related to the table's alias if found.
        
        Args:
            content: SQL content as a string
            table_name: Table name to remove joins for
            
        Returns:
            SQL content with direct joins and related WHERE conditions removed
        """
        # Check if the content is a multi-line SQL statement
        has_multiline_format = '\n' in content
        
        # Process using statement-by-statement approach
        statements = split_into_statements(content)
        processed_statements = []
        
        for stmt in statements:
            # Skip empty statements
            if not stmt.strip():
                processed_statements.append(stmt)
                continue
                
            # Process this statement to remove direct joins with the target table
            # Look for JOIN clauses with the target table (with or without ON clause)
            # Capture the alias if present (group 2)
            join_pattern = re.compile(
                rf'(\s+(?:LEFT|RIGHT|INNER|OUTER|CROSS|FULL|)?\s*JOIN\s+(?:public\.)?{table_name}(?:\s+(?:AS\s+)?(\w+))?)(\s+ON\s+.+?|\s*)(?=\s+(?:LEFT|RIGHT|INNER|OUTER|CROSS|FULL|)?\s*JOIN|\s*$|\s*;|\s*WHERE|\s*GROUP|\s*ORDER|\s*HAVING)',
                re.IGNORECASE | re.DOTALL
            )
            
            # Process all matches from the end to avoid index issues
            matches = list(join_pattern.finditer(stmt))
            
            target_table_alias = None # Variable to store the alias
            
            if matches:
                # Replace each match with empty string and capture alias
                for match in reversed(matches):
                    join_clause = match.group(0)
                    alias = match.group(2) # Group 2 captures the alias name

                    if alias:
                        target_table_alias = alias # Store the last found alias

                    stmt = stmt.replace(join_clause, "")
                
                # Clean up any duplicate spaces after removing joins
                stmt = re.sub(r'\s+', ' ', stmt).strip()

            # If an alias was found for the removed table, use the injected WhereHandler to clean conditions
            if target_table_alias:
                # Process the statement to remove WHERE conditions related to the alias
                # Note: WhereHandler.process expects a list of tables
                stmt = self.where_handler.process(stmt, [target_table_alias]) 
                # WhereHandler.process splits into statements again, but since we pass one, it's fine.
                # It also adds extra newlines which we might need to clean up later if format is strict.

            processed_statements.append(stmt)
        
        # Join the statements based on original format
        if has_multiline_format:
            # Join statements; WhereHandler might add extra newlines, clean them up if needed
            result = '\n'.join(s.strip() for s in processed_statements if s.strip()) 
        else:
            # Join statements for single-line format
            result = ' '.join(s.strip() for s in processed_statements if s.strip()) 
            
        return result
    
    def _remove_reference_joins(self, content: str, table_name: str) -> str:
        """
        Remove join conditions referencing the specified table.
        
        Args:
            content: SQL content as a string
            table_name: Table name to remove references for
            
        Returns:
            SQL content with join references removed
        """
        # Check if the content is a multi-line SQL statement
        has_multiline_format = '\n' in content
        
        # Process using statement-by-statement approach
        statements = split_into_statements(content)
        processed_statements = []
        
        for stmt in statements:
            # Skip empty statements
            if not stmt.strip():
                processed_statements.append(stmt)
                continue
                
            # Process ON clauses that reference the target table
            aliases = find_table_aliases(stmt, table_name)
            reference_column = get_table_id_column(table_name)
            
            # If no references to the table in the statement, keep it as is
            if (not any(f"{alias}." in stmt.lower() for alias in aliases) and 
                table_name.lower() + "." not in stmt.lower() and
                reference_column.lower() not in stmt.lower()):
                processed_statements.append(stmt)
                continue
                
            # Find all JOIN ... ON clauses
            join_on_pattern = re.compile(
                r'(\s+(?:LEFT|RIGHT|INNER|OUTER|CROSS|FULL|)?\s*JOIN\s+(?:\w+)(?:\s+AS\s+\w+|\s+\w+)?)\s+(ON\s+.+?)(?=\s+(?:LEFT|RIGHT|INNER|OUTER|CROSS|FULL|)?\s*JOIN|\s*$|\s*;|\s*WHERE|\s*GROUP|\s*ORDER|\s*HAVING)',
                re.IGNORECASE | re.DOTALL
            )
            
            # Process all matches
            position = 0
            result = []
            
            for match in join_on_pattern.finditer(stmt):
                join_part = match.group(1)
                on_clause = match.group(2)
                
                # Add text before this match
                result.append(stmt[position:match.start()])
                position = match.end()
                
                # Process the ON clause to remove references to the target table
                processed_on = self._process_on_clause(on_clause, table_name, aliases, reference_column)
                
                if processed_on:
                    # Keep this JOIN with the modified ON clause
                    result.append(f"{join_part} {processed_on}")
                else:
                    # This JOIN only referenced the target table, so remove it entirely
                    pass
            
            # Add remaining text
            result.append(stmt[position:])
            
            # Join the result and clean up
            modified_stmt = ''.join(result).strip()
            modified_stmt = re.sub(r'\s+', ' ', modified_stmt)
            
            processed_statements.append(modified_stmt)
        
        # Join the statements based on original format
        if has_multiline_format:
            result = '\n'.join(s for s in processed_statements if s.strip())
        else:
            result = ' '.join(s for s in processed_statements if s.strip())
            
        return result
    
    def _process_on_clause(self, on_clause: str, table_name: str, aliases: List[str], reference_column: str) -> str:
        """
        Process the ON clause to remove references to the target table.
        
        Args:
            on_clause: The ON clause to process
            table_name: Name of the table to remove references for
            aliases: Aliases for the table
            reference_column: Foreign key column referencing the table
            
        Returns:
            Processed ON clause, or empty string if all conditions reference the target table
        """
        # Always ensure ON keyword is present
        if not on_clause.strip().upper().startswith("ON"):
            on_clause = "ON " + on_clause.strip()
            
        # Check if this is a simple condition without AND/OR
        if " AND " not in on_clause.upper() and " OR " not in on_clause.upper():
            # If the simple condition references the target table, remove the entire JOIN
            if (f"{table_name.lower()}." in on_clause.lower() or 
                any(f"{alias.lower()}." in on_clause.lower() for alias in aliases) or
                reference_column.lower() in on_clause.lower()):
                return ""
            return on_clause
            
        # Handle complex conditions with parentheses
        if "(" in on_clause and ")" in on_clause:
            # Extract conditions inside parentheses and process them
            paren_pattern = r'\(([^()]*(?:\([^()]*\)[^()]*)*)\)'
            on_clause = re.sub(
                paren_pattern,
                lambda match: self._handle_parenthesized_condition(
                    match.group(1), table_name, aliases, reference_column
                ),
                on_clause
            )
            
        # Process AND conditions
        and_parts = self._split_conditions(on_clause, "AND")
        valid_parts = []
        
        for part in and_parts:
            part = part.strip()
            if not part:
                continue
                
            # Skip the "ON" keyword when checking conditions
            if part.upper() == "ON":
                valid_parts.append(part)
                continue
                
            # Remove "ON" from the beginning if present
            if part.upper().startswith("ON "):
                part = part[3:].strip()
                
            # Keep only parts that don't reference the target table
            if not self._condition_references_table(part, table_name, aliases, reference_column):
                valid_parts.append(part)
                
        if not valid_parts:
            # All parts referenced the table, so remove the entire clause
            return ""
            
        # Join the valid parts with AND, ensuring ON keyword is present
        result = " AND ".join(valid_parts)
        if not result.upper().startswith("ON "):
            result = "ON " + result
            
        return result
    
    def _handle_parenthesized_condition(self, condition: str, table_name: str, 
                                aliases: List[str], reference_column: str) -> str:
        """
        Process a condition inside parentheses.
        
        Args:
            condition: The condition inside parentheses
            table_name: Table name to check for
            aliases: List of table aliases
            reference_column: Foreign key column referencing the table
            
        Returns:
            Processed condition, with or without parentheses
        """
        # Make sure not to pass "ON" inside the parentheses
        if condition.upper().startswith("ON "):
            condition = condition[3:].strip()
            
        processed = self._process_on_clause(condition, table_name, aliases, reference_column)
        
        # Remove any "ON" keyword that might have been added in processing
        if processed and processed.upper().startswith("ON "):
            processed = processed[3:].strip()
            
        if not processed:
            return ""
        return f"({processed})"
    
    def _split_conditions(self, condition: str, operator: str) -> List[str]:
        """
        Split a condition by a logical operator.
        
        Args:
            condition: The SQL condition to split
            operator: The operator to split by (e.g., "AND", "OR")
            
        Returns:
            List of conditions split by the operator
        """
        parts = []
        pattern = rf'\b{operator}\b'
        matches = list(re.finditer(pattern, condition, re.IGNORECASE))
        
        if not matches:
            return [condition]
            
        start_idx = 0
        
        for match in matches:
            parts.append(condition[start_idx:match.start()].strip())
            start_idx = match.end()
            
        # Add the final part
        parts.append(condition[start_idx:].strip())
        
        return [p for p in parts if p.strip()]
    
    def _condition_references_table(self, condition: str, table_name: str,
                             aliases: List[str], reference_column: str) -> bool:
        """
        Check if a condition references the specified table.
        
        Args:
            condition: SQL condition string
            table_name: Name of the table to check for
            aliases: List of aliases for the table
            reference_column: Foreign key column referencing the table
            
        Returns:
            True if the condition references the table, False otherwise
        """
        condition = condition.strip()
        
        # If it's an empty condition, it doesn't reference the table
        if not condition:
            return False
            
        # Check direct table reference (table.column)
        if f"{table_name.lower()}." in condition.lower():
            return True
            
        # Check alias references (alias.column)
        for alias in aliases:
            if f"{alias.lower()}." in condition.lower():
                return True
                
        # Check reference column (e.g., table_id)
        if reference_column.lower() in condition.lower():
            return True
                
        return False 