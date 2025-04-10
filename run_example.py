#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
from sql_cleaner import SQLProcessor

def main():
    # Create a backup of the examples directory
    examples_dir = Path("examples")
    backup_dir = Path("examples_backup")
    
    # Create backup if it doesn't exist
    if not backup_dir.exists() and examples_dir.exists():
        print(f"Creating backup of examples in {backup_dir}")
        shutil.copytree(examples_dir, backup_dir)
    
    # Define tables to process
    tables_to_process = ["company", "price"]
    
    # Process a single file as an example
    processor = SQLProcessor()
    
    # Process PriceChangeServiceTest.sql
    file_path = examples_dir / "PriceChangeServiceTest.sql"
    if file_path.exists():
        print(f"Processing {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original content size: {len(content)} characters")
        
        # Process the content
        processed_content = processor.process_sql_content(content, tables_to_process)
        
        print(f"Processed content size: {len(processed_content)} characters")
        print(f"Difference: {len(content) - len(processed_content)} characters removed")
        
        # Write the processed content to a new file
        output_file = Path("examples_processed") / file_path.name
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print(f"Processed file written to {output_file}")
    else:
        print(f"File {file_path} not found")
    
    # Test multi-value INSERT handling
    print("\n=== Testing multi-value INSERT handling ===")
    multi_value_sql = """
    INSERT INTO company (id, name, tenant_id, version)
    VALUES ('c276c9f6-7da6-4622-818b-b1d837fc8142', 'ТОО "Трэйд"', 'example', 1),
           ('c276c9f6-7da6-4622-818b-b1d837fc9253', 'my fail company', 'example', 1);
    
    INSERT INTO product (id, name, company_id, version)
    VALUES ('dd76c9f6-7da6-4622-818b-b1d837fc8142', 'Product 1', 'c276c9f6-7da6-4622-818b-b1d837fc8142', 1),
           ('ee76c9f6-7da6-4622-818b-b1d837fc9253', 'Product 2', 'c276c9f6-7da6-4622-818b-b1d837fc9253', 1);
    """
    
    print("\nOriginal SQL:")
    print(multi_value_sql)
    
    print("\nProcessed SQL (removing 'company' table):")
    processed_multi_value = processor.process_sql_content(multi_value_sql, ['company'])
    print(processed_multi_value)
    
    # Write to a file
    multi_value_file = Path("examples_processed/multi_value_example.sql")
    with open(multi_value_file, "w", encoding="utf-8") as f:
        f.write(processed_multi_value)
    
    print(f"\nProcessed multi-value example written to {multi_value_file}")
    
    # Check which tables were found by the processor
    print("\nTables detected in the example:")
    tables = processor.extract_table_names(multi_value_sql)
    print(", ".join(tables))
    
    # Find direct inserts
    direct_inserts = processor.find_direct_insert_statements(multi_value_sql, 'company')
    print(f"\nFound {len(direct_inserts)} direct insert statement(s) for 'company' table")
    
    for i, stmt in enumerate(direct_inserts):
        print(f"  Statement {i+1}:")
        print(f"    Table: {stmt['table']}")
        print(f"    Has multiple values: {stmt['has_multiple_values']}")
        print(f"    Content: {stmt['text'][:100]}..." if len(stmt['text']) > 100 else f"    Content: {stmt['text']}")
    
    # Find reference inserts
    reference_inserts = processor.find_reference_insert_statements(multi_value_sql, 'company')
    print(f"\nFound {len(reference_inserts)} reference insert statement(s) for 'company' table")
    
    for i, stmt in enumerate(reference_inserts):
        print(f"  Statement {i+1}:")
        print(f"    Table: {stmt['table']}")
        print(f"    Referenced column: {stmt['column_list'][stmt['column_index']]}")
        print(f"    Has multiple values: {stmt['has_multiple_values']}")
        print(f"    Content: {stmt['text'][:100]}..." if len(stmt['text']) > 100 else f"    Content: {stmt['text']}")

if __name__ == "__main__":
    main() 