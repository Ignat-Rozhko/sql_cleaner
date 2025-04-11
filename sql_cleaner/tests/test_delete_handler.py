import unittest
from sql_cleaner.processor.delete_handler import DeleteHandler


class TestDeleteHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DeleteHandler()
        self.tables_to_process = ["TARGET_TABLE"]

    def test_empty_tables_list(self):
        sql = "DELETE FROM some_table WHERE id = 1;"
        result = self.handler.process(sql, [])
        self.assertEqual(result, sql)

    def test_remove_delete_for_target_table(self):
        sql = "DELETE FROM TARGET_TABLE WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, "")

    def test_remove_delete_for_target_table_case_insensitive(self):
        sql = "delete from target_table where id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, "")

    def test_keep_delete_for_non_target_table(self):
        sql = "DELETE FROM other_table WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, sql)

    def test_remove_multiple_delete_statements(self):
        sql = """
        DELETE FROM other_table WHERE id = 1;
        DELETE FROM TARGET_TABLE WHERE status = 'inactive';
        DELETE FROM another_table WHERE updated_at < NOW();
        """
        # We expect only the non-target statements
        result = self.handler.process(sql, self.tables_to_process)
        self.assertIn("DELETE FROM other_table WHERE id = 1", result)
        self.assertIn("DELETE FROM another_table WHERE updated_at < NOW()", result)
        self.assertNotIn("TARGET_TABLE", result)

    def test_handle_complex_delete(self):
        sql = """
        DELETE FROM TARGET_TABLE 
        WHERE id IN (SELECT id FROM reference_table WHERE status = 'obsolete');
        """
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, "")

    def test_handle_mixed_statements(self):
        sql = """
        SELECT * FROM table1;
        DELETE FROM TARGET_TABLE WHERE id = 1;
        UPDATE table2 SET status = 'active';
        """
        # We expect the SELECT and UPDATE statements to remain
        result = self.handler.process(sql, self.tables_to_process)
        self.assertIn("SELECT * FROM table1", result)
        self.assertIn("UPDATE table2 SET status = 'active'", result)
        self.assertNotIn("TARGET_TABLE", result)

    def test_keep_similar_table_names(self):
        sql = "DELETE FROM TARGET_TABLE_HISTORY WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, sql)

    def test_quoted_table_names(self):
        sql = "DELETE FROM 'TARGET_TABLE' WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        # Should not match quoted table names differently
        self.assertEqual(result, sql)
        
    def test_statements_without_semicolons(self):
        sql = """
        DELETE FROM TARGET_TABLE WHERE id = 1
        SELECT * FROM other_table
        """
        result = self.handler.process(sql, self.tables_to_process)
        self.assertIn("SELECT * FROM other_table", result)
        self.assertNotIn("TARGET_TABLE", result)


if __name__ == "__main__":
    unittest.main() 