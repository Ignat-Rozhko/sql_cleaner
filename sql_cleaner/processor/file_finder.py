import pathlib
from typing import List


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