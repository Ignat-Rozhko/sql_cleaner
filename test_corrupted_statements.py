import unittest
from sql_cleaner import SQLProcessor


class TestCorruptedStatements(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
        
    def test_no_corrupted_fragments(self):
        """Test that no corrupted fragments like 'ininininin' are left in processed content."""
        # This is the simplified SQL content that caused the issue
        sql_content = """
        set session_replication_role = replica;

        insert into public.mobile_plan_month (id, version, plan_period)
        values ('test-id', 1, '2023-06-01 12:00:42.959000');

        insert into public.employee (id, name, tenant_id)
        values ('employee-id', 'Test Employee', '123');
        """
        
        # Process the content removing mobile_plan_month table
        processed = self.processor.process_sql_content(sql_content, ['mobile_plan_month'])
        
        # Print the processed content for debugging
        print("PROCESSED CONTENT:")
        print(processed)
        
        # Verify no partial "in" fragments remain
        self.assertNotIn("in\n", processed)
        self.assertNotIn("\nin", processed)
        self.assertNotIn("ini", processed)
        
        # The insert for mobile_plan_month should be removed
        self.assertNotIn("mobile_plan_month", processed.lower())
        
        # The employee insert should still be present
        self.assertIn("employee", processed.lower())
        
    def test_multiline_statements(self):
        """Test that multiline SQL statements are correctly processed without leaving fragments."""
        sql_content = """
        insert into mobile_plan_month (
            id, 
            version, 
            plan_period
        )
        values (
            'test-id', 
            1, 
            '2023-06-01 12:00:42.959000'
        );
        
        -- This should remain in the file
        insert into employee (id, name, tenant_id)
        values ('employee-id', 'Test Employee', '123');
        """
        
        processed = self.processor.process_sql_content(sql_content, ['mobile_plan_month'])
        
        print("PROCESSED MULTILINE CONTENT:")
        print(processed)
        
        # No fragments should remain
        self.assertNotIn("in\n", processed)
        self.assertNotIn("\nin", processed)
        self.assertNotIn("ini", processed)
        
        # The multiline insert should be removed
        self.assertNotIn("mobile_plan_month", processed.lower())
        
        # The employee insert should still be present
        self.assertIn("employee", processed.lower())


if __name__ == '__main__':
    unittest.main() 