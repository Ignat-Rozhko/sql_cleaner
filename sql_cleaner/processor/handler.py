from abc import ABC, abstractmethod
from typing import Optional, List


class SQLHandler(ABC):
    """
    Abstract base class for SQL handlers in a chain of responsibility pattern.
    """
    
    def __init__(self):
        self._next_handler: Optional[SQLHandler] = None
    
    def set_next(self, handler: 'SQLHandler') -> 'SQLHandler':
        """
        Set the next handler in the chain.
        
        Args:
            handler: The next handler in the chain
            
        Returns:
            The next handler, allowing for method chaining
        """
        self._next_handler = handler
        return handler
    
    def handle(self, content: str, tables_to_process: List[str]) -> str:
        """
        Process the content and pass it to the next handler if one exists.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            Processed SQL content
        """
        processed_content = self.process(content, tables_to_process)
        
        if self._next_handler:
            return self._next_handler.handle(processed_content, tables_to_process)
        
        return processed_content
    
    @abstractmethod
    def process(self, content: str, tables_to_process: List[str]) -> str:
        """
        Process the SQL content according to the handler's specific logic.
        
        Args:
            content: SQL content to process
            tables_to_process: List of tables to process
            
        Returns:
            Processed SQL content
        """
        pass 