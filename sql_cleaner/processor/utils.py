import re
from typing import List, Dict, Set, Tuple


def preprocess_content(content: str) -> str:
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


def extract_table_names(content: str) -> Set[str]:
    """
    Extract a list of table names from the SQL content.
    
    Args:
        content: SQL content as a string
        
    Returns:
        Set of table names
    """
    content_lower = content.lower()
    tables = set()
    
    # Find table names from "insert into TABLE" statements
    insert_pattern = re.compile(r'insert\s+into\s+(\w+)', re.IGNORECASE)
    tables.update(match.group(1).lower() for match in insert_pattern.finditer(content))
    
    # Find table names from "FROM TABLE" statements
    from_pattern = re.compile(r'from\s+(\w+)(?:\s+|$|\s*;)', re.IGNORECASE)
    tables.update(match.group(1).lower() for match in from_pattern.finditer(content))
    
    # Find table names from "JOIN TABLE" statements
    join_pattern = re.compile(r'join\s+(\w+)', re.IGNORECASE)
    tables.update(match.group(1).lower() for match in join_pattern.finditer(content))
    
    # Find table names from "DELETE FROM TABLE" statements
    delete_pattern = re.compile(r'delete\s+from\s+(\w+)', re.IGNORECASE)
    tables.update(match.group(1).lower() for match in delete_pattern.finditer(content))
    
    # Find table names from "UPDATE TABLE" statements
    update_pattern = re.compile(r'update\s+(\w+)', re.IGNORECASE)
    tables.update(match.group(1).lower() for match in update_pattern.finditer(content))
    
    # Additional checks for references to fields with table_id suffix
    table_id_pattern = re.compile(r'(\w+)_id', re.IGNORECASE)
    potential_table_ids = [match.group(1) for match in table_id_pattern.finditer(content_lower)]
    
    # Add only singular form of potential tables referenced by *_id
    tables.update(table_id for table_id in potential_table_ids)
    
    return tables


def split_into_statements(content: str) -> List[str]:
    """
    Split SQL content into separate statements.
    
    Args:
        content: SQL content as a string
        
    Returns:
        List of SQL statements
    """
    # Preprocess to ensure proper formatting
    content = preprocess_content(content)
    
    # Split on semicolons, but handle those within quotes
    statements = []
    current_statement = []
    in_string = False
    string_delimiter = None
    
    for char in content:
        # Handle string boundaries
        if char in ["'", '"']:
            if not in_string:
                in_string = True
                string_delimiter = char
            elif string_delimiter == char and current_statement and current_statement[-1] != '\\':
                in_string = False
                string_delimiter = None
        
        # Append to current statement
        current_statement.append(char)
        
        # If we hit a semicolon and we're not inside a string, end the statement
        if char == ';' and not in_string:
            statements.append(''.join(current_statement).strip())
            current_statement = []
    
    # Add any remaining content as a statement (if it's not just whitespace)
    if current_statement and ''.join(current_statement).strip():
        statements.append(''.join(current_statement).strip())
    
    return [stmt for stmt in statements if stmt.strip()]


def find_table_aliases(content: str, table_name: str) -> List[str]:
    """
    Find all aliases for a given table in the SQL content.
    
    Args:
        content: SQL content as a string
        table_name: Name of the table to find aliases for
        
    Returns:
        List of table aliases
    """
    # Find all references to the table with potential aliases
    # This captures patterns like "FROM table_name alias" or "FROM table_name AS alias"
    alias_pattern = re.compile(
        rf'(?:from|join)\s+{table_name}\s+(?:as\s+)?(\w+)',
        re.IGNORECASE
    )
    
    aliases = []
    for match in alias_pattern.finditer(content):
        aliases.append(match.group(1).lower())
    
    return aliases


def split_with_nested_commas(text: str) -> List[str]:
    """
    Split a string by commas, respecting nested structures with parentheses.
    
    Args:
        text: Text to split
        
    Returns:
        List of comma-separated parts
    """
    result = []
    current_part = ""
    nesting_level = 0
    in_string = False
    string_delimiter = None
    
    for char in text:
        # Handle string boundaries
        if char in ["'", '"']:
            if not in_string:
                in_string = True
                string_delimiter = char
            elif string_delimiter == char and not (current_part and current_part[-1] == '\\'):
                in_string = False
                string_delimiter = None
        
        # Track nesting level if not in a string
        if not in_string:
            if char == '(':
                nesting_level += 1
            elif char == ')':
                nesting_level -= 1
        
        # Process comma separators
        if char == ',' and nesting_level == 0 and not in_string:
            result.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
    
    if current_part.strip():
        result.append(current_part.strip())
    
    return result 