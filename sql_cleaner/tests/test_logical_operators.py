import unittest
import sys
import os

# Get the absolute path of the parent directory (the sql_cleaner package)
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(PACKAGE_ROOT, '..')))

from sql_cleaner.processor.sql_processor import SQLProcessor


class TestLogicalOperatorPreservation(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
    
    def test_not_with_or_operators(self):
        """Test that NOT with OR operators is preserved correctly"""
        sql = """
        SELECT jsonb_build_object(
               'type', 'DeletedProductResponse',
               'productId', agg.product_ids
        )
        FROM (
             SELECT jsonb_agg(p.external_id) as product_ids
             FROM product_agent pa
             JOIN product p ON pa.product_id = p.id
             WHERE pa.agent_id = :agentId
               AND (p.created_date >= :date OR p.last_modified_date >= :date)
               AND pa.is_available = false
        ) as agg
        WHERE NOT (agg.product_ids = '[]'::jsonb OR agg.product_ids IS NULL);
        """
        
        # Process with 'target' table - should not affect the NOT (... OR ...) condition
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The NOT with OR should be preserved exactly as is
        self.assertIn("WHERE NOT (agg.product_ids = '[]'::jsonb OR agg.product_ids IS NULL)", processed)
    
    def test_not_with_and_operators(self):
        """Test that NOT with AND operators is preserved correctly"""
        sql = """
        SELECT jsonb_build_object(
               'type', 'DeletedProductResponse',
               'productId', agg.product_ids
        )
        FROM (
             SELECT jsonb_agg(p.external_id) as product_ids
             FROM product_agent pa
             JOIN product p ON pa.product_id = p.id
             WHERE pa.agent_id = :agentId
               AND (p.created_date >= :date OR p.last_modified_date >= :date)
               AND pa.is_available = false
        ) as agg
        WHERE NOT (agg.product_ids = '[]'::jsonb AND agg.product_ids IS NULL);
        """
        
        # Process with 'target' table - should not affect the NOT (... AND ...) condition
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The NOT with AND should be preserved exactly as is
        self.assertIn("WHERE NOT (agg.product_ids = '[]'::jsonb AND agg.product_ids IS NULL)", processed)
    
    def test_not_with_table_reference(self):
        """Test that NOT with table reference is handled correctly"""
        sql = """
        SELECT * FROM product p
        WHERE NOT (p.target_id IS NULL OR p.target_id = 0);
        """
        
        # Process with 'target' table - this should remove the condition
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The entire WHERE clause should be removed
        self.assertEqual("SELECT * FROM product p;", processed.strip())
    
    def test_complex_nested_logic(self):
        """Test complex nested logical conditions"""
        sql = """
        SELECT * FROM product p
        WHERE (p.category_id = 1 OR p.category_id = 2)
          AND NOT (
              (p.price < 100 AND p.target_id IS NULL)
              OR
              (p.price >= 100 AND p.target_id = 5)
          );
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The target_id references should be removed but category_id and price conditions preserved
        self.assertIn("WHERE (p.category_id = 1 OR p.category_id = 2)", processed)
        self.assertIn("AND NOT", processed)
        self.assertIn("p.price < 100", processed)
        self.assertIn("p.price >= 100", processed)
        self.assertNotIn("target_id", processed)

    def test_deleted_products_query(self):
        """Test the specific deleted products query that was having issues"""
        sql = """
        SELECT jsonb_build_object(
               'type', 'DeletedProductResponse',
               'productId', agg.product_ids
        )
        FROM (
             SELECT jsonb_agg(p.external_id) as product_ids
             FROM product_agent pa
             JOIN product p ON pa.product_id = p.id
             WHERE pa.agent_id = :agentId
               AND (p.created_date >= :date OR p.last_modified_date >= :date)
               AND pa.is_available = false
        ) as agg
        WHERE NOT (agg.product_ids = '[]'::jsonb OR agg.product_ids IS NULL);
        """
        
        # Process with 'target' table - should not affect the NOT condition
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # Check the important parts of the query
        self.assertIn("SELECT jsonb_build_object", processed)
        self.assertIn("'type', 'DeletedProductResponse'", processed)
        self.assertIn("'productId', agg.product_ids", processed)
        self.assertIn("SELECT jsonb_agg(p.external_id) as product_ids", processed)
        self.assertIn("FROM product_agent pa", processed)
        self.assertIn("JOIN product p ON pa.product_id = p.id", processed)
        self.assertIn("WHERE pa.agent_id = :agentId", processed)
        self.assertIn("AND (p.created_date >= :date OR p.last_modified_date >= :date)", processed)
        self.assertIn("AND pa.is_available = false", processed)
        
        # Specifically verify that the OR was not changed to AND in the NOT condition
        self.assertIn("NOT (agg.product_ids = '[]'::jsonb OR agg.product_ids IS NULL)", processed)
        self.assertNotIn("NOT (agg.product_ids = '[]'::jsonb AND agg.product_ids IS NULL)", processed)


if __name__ == '__main__':
    unittest.main() 