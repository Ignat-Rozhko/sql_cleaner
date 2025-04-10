import unittest
import sys
import os

# Get the absolute path of the parent directory (the sql_cleaner package)
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(PACKAGE_ROOT, '..')))

from sql_cleaner.processor.sql_processor import SQLProcessor


class TestEmptyFilePreservation(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
    
    def test_preserve_with_comment_when_all_tables_removed(self):
        """Test that empty files are preserved with a comment"""
        sql = """
        INSERT INTO table1(id, name) VALUES (1, 'test1');
        INSERT INTO table2(id, name) VALUES (2, 'test2');
        """
        
        # Extract tables from content
        tables = self.processor.extract_table_names(sql)
        self.assertEqual(2, len(tables))
        
        # Process with all tables
        processed = self.processor.process_sql_content(sql, list(tables))
        
        # The result should not be empty but contain a comment
        self.assertTrue(processed.strip())
        self.assertIn("-- All content was removed", processed)
    
    def test_agent_handler_scenario(self):
        """Test the real-world AgentHandlerTest.sql scenario"""
        sql = """
        INSERT INTO mten_tenant(id, version, tenant_id, name, external_id, dtype, create_ts, created_by)
        VALUES ('1126775d-4d03-085b-44c2-003b92dc6283', 3, 'example', 'Account', 5, 'Account', '2020-12-31 00:00:00', 'admin');

        INSERT INTO user_(id, version, tenant, username, first_name, last_name, password, active, dtype)
        VALUES ('e0a569d4-9b32-0b2e-c09f-77ff0850976d', 1, 'example', 'example|admin', 'Example', 'Admin', '{noop}password',
                TRUE, 'AccountUser');
                
        INSERT INTO currency (id, name, letter_code, version, tenant_id)
        VALUES ('42130483-df08-8445-00d1-4c208f339890', 'Тенге', 'KZT', 1, 'example');
        """
        
        # Extract tables from content
        tables = self.processor.extract_table_names(sql)
        self.assertEqual(3, len(tables))
        
        # Process with all tables
        processed = self.processor.process_sql_content(sql, list(tables))
        
        # The result should not be empty but contain a comment
        self.assertTrue(processed.strip())
        self.assertIn("-- All content was removed", processed)


if __name__ == '__main__':
    unittest.main() 