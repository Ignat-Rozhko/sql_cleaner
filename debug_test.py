#!/usr/bin/env python3
from sql_cleaner import SQLProcessor

def test_direct_insert_removal():
    processor = SQLProcessor()
    
    sql_content = """
        insert into table1 (col1, col2) values (1, 2);
        INSERT INTO table2 (col1, col2) VALUES (3, 4);
        insert into table1 (col1, col2, col3) values (5, 6, 7);
        """
    
    print("=== Original SQL Content ===")
    print(sql_content)
    
    processed = processor.process_sql_content(sql_content, ['table1'])
    
    print("\n=== Processed SQL Content ===")
    print(processed)
    
    print("\n=== Direct Insert Statements Found ===")
    direct_inserts = processor.find_direct_insert_statements(sql_content, 'table1')
    print(f"Found {len(direct_inserts)} direct inserts: {direct_inserts}")
    
    print("\n=== All SQL Statements ===")
    statements = processor._split_sql_content(sql_content)
    for i, stmt in enumerate(statements):
        print(f"Statement {i+1}:")
        print(f"  Table: {stmt['table']}")
        print(f"  Lines {stmt['start_line']}-{stmt['end_line']}")
        print(f"  Positions {stmt['start_pos']}-{stmt['end_pos']}")
        print(f"  Content: {stmt['text']}")


def test_reference_modification():
    processor = SQLProcessor()
    
    sql_content = """
        insert into other_table (id, name, table1_id, created_date)
        values (1, 'test', 100, '2022-01-01');
        """
    
    print("=== Original SQL Content ===")
    print(sql_content)
    
    processed = processor.process_sql_content(sql_content, ['table1'])
    
    print("\n=== Processed SQL Content ===")
    print(processed)
    print(f"Processed content (with spaces removed): {processed.lower().replace(' ', '')}")
    
    print("\n=== Reference Statements Found ===")
    ref_inserts = processor.find_reference_insert_statements(sql_content, 'table1')
    for ref in ref_inserts:
        print(f"Found reference at lines {ref['start_line']}-{ref['end_line']}")
        print(f"Column index: {ref['column_index']}")
        print(f"Statement: {ref['text']}")


if __name__ == "__main__":
    print("Testing direct insert removal:")
    test_direct_insert_removal()
    
    print("\n\n=============================================\n")
    
    print("Testing reference modification:")
    test_reference_modification() 