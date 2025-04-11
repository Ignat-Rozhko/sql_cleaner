import re
from sql_cleaner.processor.handler import SQLHandler
from typing import List


class CommentRemovalHandler(SQLHandler):
    """
    Handler to remove SQL comments from the content before other handlers process it.
    This handler should be the first in the chain.
    """
    
    def process(self, content: str, tables_to_process: List[str]) -> str:
        """
        Remove both single-line (--) and multi-line (/* */) SQL comments.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            SQL content with comments removed
        """
        # Process the SQL content to handle nested comments and string literals
        result = ""
        i = 0
        in_string = False
        in_comment = False
        comment_depth = 0  # Track nesting level of comments
        
        while i < len(content):
            # Handle string literals
            if content[i:i+1] == "'" and comment_depth == 0 and not in_comment:
                in_string = not in_string
                result += content[i]
                i += 1
                continue
                
            # Skip everything inside string literals
            if in_string:
                result += content[i]
                i += 1
                continue
                
            # Handle single-line comments
            if content[i:i+2] == "--" and comment_depth == 0:
                in_comment = True
                i += 2
                continue
                
            # End single-line comment at newline
            if in_comment and content[i:i+1] in ["\n", "\r"]:
                in_comment = False
                result += " "  # Add a space to replace the comment
                
            # Handle multi-line comments - opening
            if content[i:i+2] == "/*" and not in_comment:
                comment_depth += 1
                i += 2
                continue
                
            # Handle multi-line comments - closing
            if content[i:i+2] == "*/" and comment_depth > 0:
                comment_depth -= 1
                i += 2
                if comment_depth == 0:
                    result += " "  # Add a space to replace the comment
                continue
                
            # Skip over commented content
            if in_comment or comment_depth > 0:
                i += 1
                continue
                
            # Normal character
            result += content[i]
            i += 1
            
        # Replace multiple spaces with a single space
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip() 