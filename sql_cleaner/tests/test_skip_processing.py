import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Get the absolute path of the parent directory (the sql_cleaner package)
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(PACKAGE_ROOT, '..')))

from sql_cleaner.processor.sql_processor import SQLProcessor


class TestSkipProcessing(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
    
    def test_content_contains_tables(self):
        """Test that content_contains_tables correctly identifies table references"""
        # Content with direct table reference
        content_with_table = "INSERT INTO target (id, name) VALUES (1, 'test');"
        self.assertTrue(self.processor.content_contains_tables(content_with_table, ['target']))
        
        # Content with JOIN table reference
        content_with_join = "SELECT * FROM product p JOIN target t ON p.target_id = t.id;"
        self.assertTrue(self.processor.content_contains_tables(content_with_join, ['target']))
        
        # Content with WHERE table reference
        content_with_where = "SELECT * FROM product WHERE target_id = 1;"
        self.assertTrue(self.processor.content_contains_tables(content_with_where, ['target']))
        
        # Content with table alias in WHERE
        content_with_alias = "SELECT * FROM target t WHERE t.id = 1;"
        self.assertTrue(self.processor.content_contains_tables(content_with_alias, ['target']))
        
        # Content without any target table references
        content_without_table = "SELECT * FROM product WHERE product_id = 1;"
        self.assertFalse(self.processor.content_contains_tables(content_without_table, ['target']))
        
    def test_skip_processing_for_irrelevant_files(self):
        """Test that files without target tables are not processed"""
        # SQL without target tables
        sql = "SELECT * FROM product WHERE product_id = 1;"
        
        # Mock the handler to verify it's not called
        with patch.object(self.processor.handler, 'handle') as mock_handle:
            result = self.processor.process_sql_content(sql, ['target'])
            
            # Verify the handler was not called
            mock_handle.assert_not_called()
            
            # Verify the content was returned unchanged
            self.assertEqual(sql, result)
    
    def test_process_relevant_files(self):
        """Test that files with target tables are processed"""
        # SQL with target table
        sql = "SELECT * FROM target WHERE id = 1;"
        
        # Make sure content_contains_tables returns True for this SQL
        # This is needed because our mock doesn't affect this method
        with patch.object(self.processor, 'content_contains_tables', return_value=True):
            # Mock the handler to verify it's called and return a modified result
            with patch.object(self.processor.handler, 'handle', return_value="MODIFIED") as mock_handle:
                result = self.processor.process_sql_content(sql, ['target'])
                
                # Verify the handler was called with the correct arguments
                mock_handle.assert_called_once_with(sql, ['target'])
                
                # Verify the content was modified
                self.assertEqual("MODIFIED", result)


if __name__ == '__main__':
    unittest.main() 