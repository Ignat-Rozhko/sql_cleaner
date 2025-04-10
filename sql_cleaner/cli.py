import os
import sys
import argparse
from typing import List, Optional

from sql_cleaner.processor.file_finder import SQLFileFinder
from sql_cleaner.processor.sql_processor import SQLProcessor


def read_tables_from_file(file_path: str) -> List[str]:
    """
    Read table names from a file.
    
    Args:
        file_path: Path to the file with table names
        
    Returns:
        List of table names
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def process_sql_files(directory: str, tables_to_process: Optional[List[str]] = None, tables_file: Optional[str] = None):
    """
    Process all SQL files in a directory recursively.
    
    Args:
        directory: Directory to search for SQL files
        tables_to_process: List of tables to process
        tables_file: Path to a file containing table names
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        return
    
    # Load tables from file if specified
    if tables_file:
        tables_from_file = read_tables_from_file(tables_file)
        if tables_to_process:
            tables_to_process.extend(tables_from_file)
        else:
            tables_to_process = tables_from_file
    
    # Find SQL files
    finder = SQLFileFinder(directory)
    sql_files = finder.find_sql_files()
    
    if not sql_files:
        print(f"No SQL files found in directory: {directory}")
        return
    
    print(f"Found {len(sql_files)} SQL files to process.")
    
    # Create SQL processor
    processor = SQLProcessor()
    
    # Process each file
    for file_path in sql_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If no tables are specified, extract them from the content
            if not tables_to_process:
                tables_from_content = processor.extract_table_names(content)
                if not tables_from_content:
                    print(f"No tables found in file: {file_path}")
                    continue
                
                tables_for_file = list(tables_from_content)
            else:
                tables_for_file = tables_to_process
            
            # Process the content
            processed_content = processor.process_sql_content(content, tables_for_file)
            
            # Write the processed content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            print(f"Processed file: {file_path}")
        
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}", file=sys.stderr)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Clean SQL files by removing specific table inserts and references.')
    parser.add_argument('directory', help='Directory to search for SQL files recursively')
    parser.add_argument('tables', nargs='*', help='Tables to process (if not provided, all tables found will be processed)')
    parser.add_argument('--tables-file', help='Path to a file containing table names to process')
    
    args = parser.parse_args()
    
    process_sql_files(args.directory, args.tables, args.tables_file)


if __name__ == '__main__':
    main() 