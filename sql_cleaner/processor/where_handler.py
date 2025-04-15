import re
from typing import List, Dict

from sql_cleaner.processor.handler import SQLHandler
from sql_cleaner.processor.utils import (
    split_into_statements,
    find_table_aliases,
    get_table_id_column
)


class WhereHandler(SQLHandler):
    """
    Handler for processing and removing WHERE conditions related to specified tables.
    """
    
    def process(self, content: str, tables_to_process: List[str]) -> str:
        """
        Process the SQL content to remove WHERE conditions related to the specified tables.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            Processed SQL content
        """
        processed_content = content
        
        for table_name in tables_to_process:
            processed_content = self._remove_where_conditions(processed_content, table_name)
        
        return processed_content
    
    def _remove_where_conditions(self, content: str, table_name: str) -> str:
        """
        Remove WHERE conditions related to the specified table.
        
        Args:
            content: SQL content as a string
            table_name: Name of the table to remove conditions for
            
        Returns:
            SQL content with WHERE conditions removed or modified
        """
        statements = split_into_statements(content)
        processed_statements = []
        
        for stmt in statements:
            # Skip empty statements
            if not stmt.strip():
                processed_statements.append(stmt)
                continue
            
            # First try to find the main SQL structure with ORDER BY outside of WHERE
            sql_structure = re.match(
                r'(.*?)\s+WHERE\s+(.+?)(?:\s+(ORDER\s+BY.+?))?(;|$)',
                stmt,
                re.IGNORECASE | re.DOTALL
            )
            
            if not sql_structure:
                # No WHERE clause in this statement
                processed_statements.append(stmt)
                continue
                
            before_where = sql_structure.group(1).strip()  # Everything before WHERE
            where_conditions = sql_structure.group(2).strip()  # The conditions part
            order_by_clause = sql_structure.group(3) or ""  # ORDER BY clause if exists
            statement_end = sql_structure.group(4)  # Semicolon or end of string
            
            # Find all table aliases in this statement
            aliases = find_table_aliases(stmt, table_name)
            
            # Identify columns that could reference the table
            reference_columns = [get_table_id_column(table_name)]
            
            # Process the WHERE conditions
            processed_conditions = self._process_complex_where_conditions(where_conditions, table_name, aliases, reference_columns)
            
            # Clean up any leading/trailing AND/OR
            if processed_conditions:
                processed_conditions = re.sub(r'^\s*(AND|OR)\s+', '', processed_conditions, flags=re.IGNORECASE)
                processed_conditions = re.sub(r'\s+(AND|OR)\s*$', '', processed_conditions, flags=re.IGNORECASE)
            
            # Build the new statement
            if not processed_conditions or processed_conditions.strip() in ["NOT", "AND", "OR"]:
                # No conditions left or just operator keywords without expressions, remove the WHERE clause entirely
                modified_statement = before_where
                if order_by_clause:
                    modified_statement += f" {order_by_clause}"
                modified_statement += statement_end
            else:
                # Create the new WHERE clause with proper formatting
                modified_statement = f"{before_where} WHERE {processed_conditions}"
                if order_by_clause:
                    modified_statement += f" {order_by_clause}"
                modified_statement += statement_end
            
            # Clean up the statement
            # Remove any trailing whitespace before semicolon
            modified_statement = re.sub(r'\s+;', ';', modified_statement)
            
            # Ensure there's a semicolon at the end if the original statement had one
            if statement_end == ';' and not modified_statement.endswith(';'):
                modified_statement += ';'
                
            # Clean up spaces and line breaks
            modified_statement = re.sub(r'\s+', ' ', modified_statement).strip()
            
            processed_statements.append(modified_statement)
        
        return '\n\n'.join(processed_statements)
    
    def _process_complex_where_conditions(self, where_conditions: str, table_name: str, 
                                   aliases: List[str], reference_columns: List[str]) -> str:
        """
        Process complex WHERE conditions with nested parentheses and logical operators.
        
        Args:
            where_conditions: WHERE clause conditions
            table_name: Table name to check for
            aliases: List of table aliases
            reference_columns: List of column names that reference the table
            
        Returns:
            Processed WHERE conditions, or empty string if all conditions should be removed
        """
        # Special handling for NOT operator
        not_match = re.match(r'^NOT\s+\((.*)\)$', where_conditions.strip(), re.IGNORECASE)
        if not_match:
            inner_condition = not_match.group(1).strip()
            # Check if the inner condition references the table
            if self._condition_references_table(inner_condition, table_name, aliases, reference_columns):
                # Process the inner condition
                processed_inner = self._process_complex_where_conditions(inner_condition, table_name, aliases, reference_columns)
                if not processed_inner or processed_inner.strip() == "":
                    # If inner condition is empty after processing, remove the entire NOT expression
                    return ""
                else:
                    # Return the NOT with the processed inner condition
                    return f"NOT ({processed_inner})"
        
        # Handle BETWEEN conditions before other processing
        between_pattern = re.compile(r'(\w+(?:\.\w+)?)\s+BETWEEN\s+(.+?)\s+AND\s+(.+?)(?=\s+AND|\s*$|\s*;)', re.IGNORECASE)
        between_matches = list(between_pattern.finditer(where_conditions))
        
        # Process BETWEEN matches from the end to avoid index issues
        for match in reversed(between_matches):
            between_expr = match.group(0)
            column_name = match.group(1)
            
            # Check if this BETWEEN expression references the target table
            if self._column_references_table(column_name, table_name, aliases, reference_columns):
                # If the BETWEEN is part of a larger AND expression, replace it with empty string for later processing
                where_conditions = where_conditions.replace(between_expr, "")
                
                # Clean up any potential double spaces
                where_conditions = re.sub(r'\s+', ' ', where_conditions)
                
                # Clean up any "AND AND" that might have been created
                where_conditions = re.sub(r'\bAND\s+AND\b', 'AND', where_conditions, flags=re.IGNORECASE)
                
                # Clean up any leading/trailing AND
                where_conditions = re.sub(r'^\s*AND\s+', '', where_conditions, flags=re.IGNORECASE)
                where_conditions = re.sub(r'\s+AND\s*$', '', where_conditions, flags=re.IGNORECASE)
        
        # If where_conditions is now empty or just whitespace, return empty string
        if not where_conditions.strip():
            return ""
        
        # Check if the condition doesn't reference the table at all - if so, return it as is
        # This preserves complex logic with AND/OR operators when they don't reference our target tables
        if not self._condition_references_table(where_conditions, table_name, aliases, reference_columns):
            return where_conditions
            
        # Handle conditions within parentheses recursively
        paren_pattern = r'\(([^()]*(?:\([^()]*\)[^()]*)*)\)'
        
        # Limit the number of recursion to avoid infinite loops
        max_recursion = 10
        recursion_count = 0
        
        while re.search(paren_pattern, where_conditions) and recursion_count < max_recursion:
            recursion_count += 1
            where_conditions = re.sub(
                paren_pattern,
                lambda match: self._handle_parenthesized_condition(
                    match.group(1), table_name, aliases, reference_columns
                ),
                where_conditions
            )
        
        # Final processing of the simplified condition
        return self._process_and_or_conditions(where_conditions, table_name, aliases, reference_columns)
    
    def _handle_parenthesized_condition(self, condition: str, table_name: str,
                                 aliases: List[str], reference_columns: List[str]) -> str:
        """
        Handle a parenthesized condition by processing its contents and deciding if it should be kept.
        
        Args:
            condition: The condition inside parentheses
            table_name: Table name to check for
            aliases: List of table aliases
            reference_columns: List of column names that reference the table
            
        Returns:
            Processed condition, potentially with parentheses, or empty string
        """
        # If the condition is empty, return empty string
        if not condition.strip():
            return ""
            
        # If the condition only contains table references and no AND/OR, remove it entirely
        if self._condition_references_table(condition, table_name, aliases, reference_columns) and \
           " AND " not in condition.upper() and " OR " not in condition.upper():
            return ""
        
        # Process the condition
        processed = self._process_and_or_conditions(condition, table_name, aliases, reference_columns)
        
        # Clean up any extraneous AND/OR operators
        if processed:
            processed = re.sub(r'^\s*(AND|OR)\s+', '', processed, flags=re.IGNORECASE)
            processed = re.sub(r'\s+(AND|OR)\s*$', '', processed, flags=re.IGNORECASE)
        
        if not processed or processed.strip() in ["AND", "OR"]:
            return ""
        else:
            return f"({processed})"
    
    def _process_and_or_conditions(self, where_conditions: str, table_name: str,
                            aliases: List[str], reference_columns: List[str]) -> str:
        """
        Process AND/OR conditions and determine which ones to keep.
        
        Args:
            where_conditions: WHERE clause conditions
            table_name: Table name to check for
            aliases: List of table aliases
            reference_columns: List of column names that reference the table
            
        Returns:
            Processed WHERE conditions, or empty string if all conditions should be removed
        """
        where_conditions = where_conditions.strip()
        
        # If empty, return empty string
        if not where_conditions:
            return ""
            
        # Check if the condition doesn't reference the table at all - if so, return it as is
        # This preserves complex logic with AND/OR operators when they don't reference our target tables
        if not self._condition_references_table(where_conditions, table_name, aliases, reference_columns):
            return where_conditions
            
        # First, try to split by OR
        or_parts = self._split_by_operator(where_conditions, r'\bOR\b')
        
        if len(or_parts) > 1:
            # Process each OR part and keep only those that don't fully reference the table
            processed_parts = []
            for part in or_parts:
                part = part.strip()
                if not part:
                    continue
                    
                # Skip parts that only reference the target table
                if self._condition_references_table(part, table_name, aliases, reference_columns):
                    # If it's a complex condition with AND, process it further
                    if " AND " in part.upper():
                        processed_part = self._process_and_or_conditions(part, table_name, aliases, reference_columns)
                        if processed_part and processed_part.strip() not in ["AND", "OR"]:
                            processed_parts.append(processed_part)
                else:
                    # This part doesn't reference the target table, keep it as is
                    processed_parts.append(part)
            
            if not processed_parts:
                # All parts referenced the table, so remove the entire condition
                return ""
            
            # Join the remaining parts with OR
            return " OR ".join(processed_parts)
        
        # If no OR, split by AND
        and_parts = self._split_by_operator(where_conditions, r'\bAND\b')
        
        if len(and_parts) > 1:
            # Process each AND part and remove those that reference the table
            processed_parts = []
            for part in and_parts:
                part = part.strip()
                if not part:
                    continue
                    
                # Keep only parts that don't reference the target table
                if not self._condition_references_table(part, table_name, aliases, reference_columns):
                    processed_parts.append(part)
            
            if not processed_parts:
                # All parts referenced the table, so remove the entire condition
                return ""
            
            # Join the remaining parts with AND
            return " AND ".join(processed_parts)
        
        # Single condition, check if it references the table
        # If it's a simple condition without AND/OR that references the table, remove it
        if self._condition_references_table(where_conditions, table_name, aliases, reference_columns):
            return ""
        else:
            # Condition doesn't reference the table, so keep it
            return where_conditions
    
    def _split_by_operator(self, condition: str, operator: str) -> List[str]:
        """
        Split a condition by a logical operator, considering proper nesting and string literals.
        
        Args:
            condition: The SQL condition to split
            operator: The operator to split by (as a regex pattern)
            
        Returns:
            List of conditions split by the operator
        """
        parts = []
        matches = list(re.finditer(operator, condition, re.IGNORECASE))
        
        if not matches:
            return [condition]
        
        start_idx = 0
        for match in matches:
            parts.append(condition[start_idx:match.start()].strip())
            start_idx = match.end()
        
        # Add the final part
        parts.append(condition[start_idx:].strip())
        
        return parts
    
    def _column_references_table(self, column_name: str, table_name: str,
                           aliases: List[str], reference_columns: List[str]) -> bool:
        """
        Check if a column name references the specified table.
        
        Args:
            column_name: Column name to check
            table_name: Table name to check for
            aliases: List of table aliases
            reference_columns: List of column names that reference the table
            
        Returns:
            True if the column references the table, False otherwise
        """
        column_name = column_name.lower().strip()
        
        # Check for direct table reference: "table.column"
        if f"{table_name.lower()}." in column_name:
            return True
        
        # Check for alias reference: "t.column"
        for alias in aliases:
            if f"{alias.lower()}." in column_name:
                return True
        
        # Check for reference columns like "table_id"
        for ref_col in reference_columns:
            if ref_col.lower() == column_name:
                return True
        
        return False
    
    def _condition_references_table(self, condition: str, table_name: str,
                              aliases: List[str], reference_columns: List[str]) -> bool:
        """
        Check if a condition references the specified table.
        
        Args:
            condition: SQL condition string
            table_name: Name of the table to check for
            aliases: List of aliases for the table
            reference_columns: List of column names that reference the table
            
        Returns:
            True if the condition references the table, False otherwise
        """
        condition = condition.strip()
        
        # If it's an empty condition, it doesn't reference the table
        if not condition:
            return False
            
        # Special handling for BETWEEN conditions
        between_match = re.search(r'(\w+(?:\.\w+)?)\s+BETWEEN\s+(.+?)\s+AND\s+(.+?)(?=\s+AND|\s*$|\s*;)', condition, re.IGNORECASE)
        if between_match:
            column_name = between_match.group(1)
            # Check if the column references the table
            if self._column_references_table(column_name, table_name, aliases, reference_columns):
                return True
                
            # Also check if the BETWEEN values reference the table (could be table names in complex expressions)
            lower_val = between_match.group(2)
            upper_val = between_match.group(3)
            
            if (table_name.lower() in lower_val.lower() or 
                table_name.lower() in upper_val.lower()):
                return True
                
            # Check aliases in the BETWEEN values
            for alias in aliases:
                if (alias.lower() in lower_val.lower() or 
                    alias.lower() in upper_val.lower()):
                    return True
        
        # Check direct table reference (table.column)
        if re.search(rf'(?:^|\W){re.escape(table_name)}\.', condition, re.IGNORECASE):
            return True
        
        # Check alias references (alias.column)
        for alias in aliases:
            if re.search(rf'(?:^|\W){re.escape(alias)}\.', condition, re.IGNORECASE):
                return True
        
        # Check reference columns (e.g., table_id)
        for col in reference_columns:
            # More precise pattern to avoid false positives
            pattern = rf'(?:^|\W)(?:\w+\.)?{re.escape(col)}\b\s*(?:=|!=|<>|>|<|>=|<=|IS\s+NULL|IS\s+NOT\s+NULL|IN|LIKE|NOT)'
            if re.search(pattern, condition, re.IGNORECASE):
                return True
        
        # Check for cases like p.target_id or product.target_id 
        if re.search(rf'(?:^|\W)\w+\.{re.escape(get_table_id_column(table_name))}\b', condition, re.IGNORECASE):
            return True
             
        return False 