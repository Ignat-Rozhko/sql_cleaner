import unittest
from sql_cleaner import SQLProcessor

class TestSimple(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
        
    def test_direct_insert_removal(self):
        # Test removal of direct insert statements for a specific table
        sql_content = """
        insert into table1 (col1, col2) values (1, 2);
        INSERT INTO table2 (col1, col2) VALUES (3, 4);
        insert into table1 (col1, col2, col3) values (5, 6, 7);
        """
        processed = self.processor.process_sql_content(sql_content, ['table1'])
        
        print("PROCESSED CONTENT:")
        print(processed)
        
        # The first table1 insert should be removed
        # Verify the first insert is removed
        self.assertNotIn("table1 (col1, col2) values (1, 2)", processed.lower())
        self.assertNotIn("table1 (col1, col2, col3) values (5, 6, 7)", processed.lower())
        
        # Verify table2 insert remains
        self.assertIn("table2", processed.lower())

if __name__ == '__main__':
    unittest.main() 