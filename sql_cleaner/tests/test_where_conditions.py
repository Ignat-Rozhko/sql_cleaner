import unittest
import sys
import os

# Get the absolute path of the parent directory (the sql_cleaner package)
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(PACKAGE_ROOT, '..')))

from sql_cleaner.processor.sql_processor import SQLProcessor


class TestWhereConditionRemoval(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
    
    def test_simple_where_condition(self):
        """Test removing a simple WHERE condition with a direct table reference"""
        sql = """
        SELECT * FROM product
        WHERE product_id = 5;
        """
        
        # Process with 'product' table
        processed = self.processor.process_sql_content(sql, ['product'])
        
        # The WHERE clause should be removed entirely
        self.assertEqual("SELECT * FROM product;", processed.strip())
    
    
    def test_simple_where_with_table_id(self):
        """Test removing a simple WHERE condition with target_id reference"""
        sql = """
        SELECT * FROM order o
        WHERE target_id = 5;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The WHERE clause should be removed entirely
        self.assertEqual("SELECT * FROM order o;", processed.strip())
    
    def test_compound_where_condition(self):
        """Test removing a condition from a WHERE clause with multiple conditions"""
        sql = """
        SELECT * FROM product p
        WHERE target_id = 5 AND 
        another_id = 6;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The WHERE clause should still exist, but without the target_id condition
        self.assertIn("WHERE", processed.upper())
        self.assertNotIn("target_id", processed.lower())
        self.assertIn("another_id = 6", processed)
    
    def test_null_check_with_order_by(self):
        """Test removing IS NULL condition with ORDER BY clause"""
        sql = """
        SELECT * FROM product p
        WHERE target_id IS NULL
        ORDER BY p.name;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The WHERE clause should be removed, but ORDER BY preserved
        self.assertEqual("SELECT * FROM product p ORDER BY p.name;", processed.strip())
    
    def test_null_check_with_order_by_and_another_column(self):
        """Test removing IS NULL condition with ORDER BY clause"""
        sql = """
        SELECT * FROM product p
        WHERE some_column = 1
        AND target_id IS NULL
        ORDER BY p.name;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The WHERE clause should be removed, but ORDER BY preserved
        self.assertEqual("SELECT * FROM product p WHERE some_column = 1 ORDER BY p.name;", processed.strip())
    
    def test_non_matching_where_condition(self):
        """Test WHERE conditions that shouldn't be affected"""
        sql = """
        SELECT * FROM product p
        WHERE another_id = 7 AND one_more_id = 8;
        """
        
        # Process with 'target' table (not referenced in the query)
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The WHERE clause should remain unchanged
        self.assertEqual("SELECT * FROM product p WHERE another_id = 7 AND one_more_id = 8;", processed.strip())
    
    def test_where_with_in_clause(self):
        """Test WHERE with IN clause referencing the target table"""
        sql = """
        SELECT * FROM product p
        WHERE another_id = 7 
        AND target_id IN (1, 2, 3);
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The target_id condition should be removed
        self.assertEqual("SELECT * FROM product p WHERE another_id = 7;", processed.strip())
    
    
    def test_table_reference_in_where(self):
        """Test WHERE with direct table reference"""
        sql = """
        SELECT p.id, p.name, t.description
        FROM product p
        JOIN target t ON p.target_id = t.id
        WHERE t.active = true AND p.price > 100;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The t.active condition should be removed
        self.assertIn("WHERE p.price > 100", processed)
        self.assertNotIn("t.active", processed)
    
    def test_complex_where_with_parentheses(self):
        """Test complex WHERE with parentheses and logical operators"""
        sql = """
        SELECT * FROM product p
        WHERE (target_id = 5 OR target_id IS NULL) AND p.price > 0;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The entire target_id condition group should be removed
        self.assertIn("WHERE p.price > 0;", processed)
        self.assertNotIn("target_id", processed.lower())
        self.assertNotIn("OR", processed.upper())
    
    def test_multiple_statements(self):
        """Test processing multiple SQL statements"""
        sql = """
        SELECT * FROM product WHERE target_id = 1;
        SELECT * FROM order WHERE order_id = 100;
        SELECT * FROM invoice WHERE target_id = 5;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # First statement should have WHERE removed
        self.assertIn("SELECT * FROM product", processed)
        self.assertNotIn("WHERE target_id = 1;", processed)
        
        # Second statement should remain unchanged
        self.assertIn("SELECT * FROM order WHERE order_id = 100", processed)
        
        # Third statement should have target_id condition removed
        self.assertIn("SELECT * FROM invoice", processed)
        self.assertNotIn("target_id = 5", processed)
    
    def test_table_alias_detection(self):
        """Test detection and removal of WHERE conditions with table aliases"""
        sql = """
        SELECT p.id, t.name 
        FROM product p
        JOIN target t ON p.target_id = t.id
        WHERE p.active = true AND t.region = 'Europe';
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The t.region condition should be removed
        self.assertIn("WHERE p.active = true", processed)
        self.assertNotIn("t.region", processed)
        self.assertNotIn("Europe", processed)
    
    def test_nested_conditions(self):
        """Test nested WHERE conditions with complex logic"""
        sql = """
        SELECT * FROM product p
        WHERE (
            (p.category = 'Electronics' AND target_id = 10)
            OR
            (p.category = 'Books' AND target_id IS NULL)
        )
        AND p.price > 0;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # All target_id references should be removed
        self.assertIn("WHERE", processed.upper())  # WHERE clause should still exist
        self.assertIn("p.price > 0", processed)    # This condition should remain
        self.assertNotIn("target_id", processed.lower())
    
    def test_between_condition_removal(self):
        """Test removing a BETWEEN condition related to the target table"""
        sql = """
        SELECT * FROM product p
        WHERE p.price > 0 AND target_id BETWEEN 1 AND 10;
        """
        
        # Process with 'target' table
        processed = self.processor.process_sql_content(sql, ['target'])
        
        # The BETWEEN condition should be removed
        self.assertEqual("SELECT * FROM product p WHERE p.price > 0;", processed.strip())
        self.assertNotIn("target_id", processed.lower())
        self.assertNotIn("BETWEEN", processed.upper())


if __name__ == '__main__':
    unittest.main() 