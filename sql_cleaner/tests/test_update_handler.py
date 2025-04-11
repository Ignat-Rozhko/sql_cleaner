import unittest
from sql_cleaner.processor.update_handler import UpdateHandler


class TestUpdateHandler(unittest.TestCase):
    def setUp(self):
        self.handler = UpdateHandler()
        self.tables_to_process = ["TARGET_TABLE"]

    def test_empty_tables_list(self):
        sql = "UPDATE some_table SET status = 'active' WHERE id = 1;"
        result = self.handler.process(sql, [])
        self.assertEqual(result, sql)

    def test_remove_update_for_target_table(self):
        sql = "UPDATE TARGET_TABLE SET status = 'active' WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, "")

    def test_remove_update_for_target_table_case_insensitive(self):
        sql = "update target_table set status = 'active' where id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, "")

    def test_keep_update_for_non_target_table(self):
        sql = "UPDATE other_table SET status = 'active' WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, sql)

    def test_remove_multiple_update_statements(self):
        sql = """
        UPDATE other_table SET name = 'Test' WHERE id = 1;
        UPDATE TARGET_TABLE SET status = 'inactive' WHERE user_id = 5;
        UPDATE another_table SET updated_at = NOW() WHERE created_at < '2023-01-01';
        """
        # We expect only the non-target statements
        result = self.handler.process(sql, self.tables_to_process)
        self.assertIn("UPDATE other_table SET name = 'Test' WHERE id = 1", result)
        self.assertIn("UPDATE another_table SET updated_at = NOW() WHERE created_at < '2023-01-01'", result)
        self.assertNotIn("TARGET_TABLE", result)

    def test_handle_complex_update(self):
        sql = """
        UPDATE TARGET_TABLE 
        SET status = (SELECT status FROM reference_table WHERE id = TARGET_TABLE.ref_id)
        WHERE active = 1;
        """
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, "")

    def test_handle_mixed_statements(self):
        sql = """
        SELECT * FROM table1;
        UPDATE TARGET_TABLE SET status = 'inactive' WHERE id = 1;
        DELETE FROM table2 WHERE status = 'obsolete';
        """
        # We expect the SELECT and DELETE statements to remain
        result = self.handler.process(sql, self.tables_to_process)
        self.assertIn("SELECT * FROM table1", result)
        self.assertIn("DELETE FROM table2 WHERE status = 'obsolete'", result)
        self.assertNotIn("TARGET_TABLE", result)

    def test_keep_similar_table_names(self):
        sql = "UPDATE TARGET_TABLE_HISTORY SET status = 'archived' WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, sql)

    def test_quoted_table_names(self):
        sql = "UPDATE 'TARGET_TABLE' SET status = 'inactive' WHERE id = 1;"
        result = self.handler.process(sql, self.tables_to_process)
        # Should not match quoted table names differently
        self.assertEqual(result, sql)
        
    def test_statements_without_semicolons(self):
        sql = """
        UPDATE TARGET_TABLE SET status = 'inactive' WHERE id = 1
        SELECT * FROM other_table
        """
        result = self.handler.process(sql, self.tables_to_process)
        self.assertIn("SELECT * FROM other_table", result)
        self.assertNotIn("TARGET_TABLE", result)


if __name__ == "__main__":
    unittest.main() 