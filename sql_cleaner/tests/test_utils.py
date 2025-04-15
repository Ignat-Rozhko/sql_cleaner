import unittest
from sql_cleaner.processor.utils import get_table_id_column


class TestUtils(unittest.TestCase):
    def test_get_table_id_column(self):
        """Test the get_table_id_column function for different table name cases"""
        # Test normal table name
        self.assertEqual(get_table_id_column("users"), "users_id")
        
        # Test table name ending with underscore
        self.assertEqual(get_table_id_column("users_"), "users_id")
        
        # Test table name with multiple underscores
        self.assertEqual(get_table_id_column("user_profiles_"), "user_profiles_id")
        
        # Test table name with no underscores
        self.assertEqual(get_table_id_column("product"), "product_id")
        
        # Test empty table name
        self.assertEqual(get_table_id_column(""), "_id")
        
        # Test table name with just underscore
        self.assertEqual(get_table_id_column("_"), "_id") 