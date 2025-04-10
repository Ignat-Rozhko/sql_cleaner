import unittest
import sys
import os

# Get the absolute path of the parent directory (the sql_cleaner package)
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(PACKAGE_ROOT, '..')))

from sql_cleaner.processor.sql_processor import SQLProcessor


class TestInsertPreservation(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
    
    def test_preserve_non_target_inserts(self):
        """Test that INSERT statements for non-target tables are preserved"""
        sql = """
        INSERT INTO table1(id, name) VALUES (1, 'test1');
        INSERT INTO table2(id, name) VALUES (2, 'test2');
        INSERT INTO target(id, name) VALUES (3, 'test3');
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The INSERT statements for non-target tables should be preserved
        self.assertIn("INSERT INTO table1", processed)
        self.assertIn("INSERT INTO table2", processed)
        self.assertNotIn("INSERT INTO target", processed)
    
    def test_process_multiple_tables(self):
        """Test processing with multiple target tables"""
        sql = """
        INSERT INTO table1(id, name) VALUES (1, 'test1');
        INSERT INTO table2(id, name) VALUES (2, 'test2');
        INSERT INTO target(id, name) VALUES (3, 'test3');
        """
        
        # Process with multiple target tables
        processed = self.processor.process_sql_content(sql, ['table1', 'target'])
        
        # Only table2 inserts should be preserved
        self.assertNotIn("INSERT INTO table1", processed)
        self.assertIn("INSERT INTO table2", processed)
        self.assertNotIn("INSERT INTO target", processed)
    
    def test_handle_all_tables_targeted(self):
        """Test handling when all tables in the file are targeted"""
        sql = """
        INSERT INTO table1(id, name) VALUES (1, 'test1');
        INSERT INTO table2(id, name) VALUES (2, 'test2');
        """
        
        # Process with all tables in file
        processed = self.processor.process_sql_content(sql, ['table1', 'table2'])
        
        # The result should be empty or contain only whitespace/comments
        self.assertFalse(any(line.strip() for line in processed.split('\n') if not line.strip().startswith('--')))
    
    def test_real_world_example(self):
        """Test with a real-world example similar to AgentHandlerTest.sql"""
        sql = """
        INSERT INTO mten_tenant(id, version, tenant_id, name, external_id, dtype, create_ts, created_by)
        VALUES ('1126775d-4d03-085b-44c2-003b92dc6283', 3, 'example', 'Account', 5, 'Account', '2020-12-31 00:00:00', 'admin');

        INSERT INTO user_(id, version, tenant, username, first_name, last_name, password, active, dtype)
        VALUES ('e0a569d4-9b32-0b2e-c09f-77ff0850976d', 1, 'example', 'example|admin', 'Example', 'Admin', '{noop}password',
                TRUE, 'AccountUser');
                
        INSERT INTO currency (id, name, letter_code, version, tenant_id)
        VALUES ('42130483-df08-8445-00d1-4c208f339890', 'Тенге', 'KZT', 1, 'example');
        """
        
        # Process with just one target table
        processed = self.processor.process_sql_content(sql, ['currency'])
        
        # The other tables' INSERT statements should be preserved
        self.assertIn("INSERT INTO mten_tenant", processed)
        self.assertIn("INSERT INTO user_", processed)
        self.assertNotIn("INSERT INTO currency", processed)


if __name__ == '__main__':
    unittest.main() 