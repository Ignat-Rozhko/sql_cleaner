import unittest
from sql_cleaner.processor.join_handler import JoinHandler
from sql_cleaner.processor.where_handler import WhereHandler

class TestJoinStatementHandler(unittest.TestCase):
    def setUp(self):
        self.handler = JoinHandler(where_handler=WhereHandler())
        self.tables_to_process = ["TARGET_TABLE", "PRODUCT_BALANCE_CHANGE"]
    
    def test_empty_tables_list(self):
        sql = "SELECT * FROM table1 JOIN table2 ON table1.id = table2.id"
        result = self.handler.process(sql, [])
        self.assertEqual(result, sql)
    
    def test_remove_entire_join_with_target_table(self):
        sql = "SELECT * FROM table1 JOIN TARGET_TABLE ON table1.id = TARGET_TABLE.id"
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_remove_entire_join_with_target_table_case_insensitive(self):
        sql = "SELECT * FROM table1 JOIN target_table ON table1.id = target_table.id"
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_remove_conditions_referencing_target_table(self):
        sql = "SELECT * FROM table1 JOIN valid_table ON table1.id = valid_table.id AND TARGET_TABLE.col = valid_table.col"
        expected = "SELECT * FROM table1 JOIN valid_table ON table1.id = valid_table.id"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_remove_all_conditions_referencing_target_table(self):
        sql = "SELECT * FROM table1 JOIN valid_table ON TARGET_TABLE.id = valid_table.id"
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_multiple_joins_with_target_tables(self):
        sql = """
        SELECT * FROM table1 
        JOIN valid_table ON table1.id = valid_table.id 
        JOIN TARGET_TABLE ON table1.id = TARGET_TABLE.id 
        JOIN another_table ON table1.id = another_table.id AND PRODUCT_BALANCE_CHANGE.status = 'active'
        """
        expected = "SELECT * FROM table1 JOIN valid_table ON table1.id = valid_table.id JOIN another_table ON table1.id = another_table.id"
        result = self.handler.process(sql, self.tables_to_process)
        # Normalize spaces for comparison
        result = ' '.join(result.split())
        expected = ' '.join(expected.split())
        self.assertEqual(result, expected)
    
    def test_join_with_table_alias(self):
        sql = "SELECT * FROM table1 JOIN TARGET_TABLE t ON table1.id = t.id"
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_with_as_alias(self):
        sql = "SELECT * FROM table1 JOIN TARGET_TABLE AS t ON table1.id = t.id"
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_without_on_clause(self):
        sql = "SELECT * FROM table1 JOIN TARGET_TABLE JOIN valid_table ON table1.id = valid_table.id"
        expected = "SELECT * FROM table1 JOIN valid_table ON table1.id = valid_table.id"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_with_different_join_types(self):
        sql = """
        SELECT * FROM table1 
        LEFT JOIN TARGET_TABLE ON table1.id = TARGET_TABLE.id 
        RIGHT JOIN valid_table ON table1.id = valid_table.id AND PRODUCT_BALANCE_CHANGE.col = valid_table.col
        """
        expected = "SELECT * FROM table1 RIGHT JOIN valid_table ON table1.id = valid_table.id"
        result = self.handler.process(sql, self.tables_to_process)
        # Normalize spaces for comparison
        result = ' '.join(result.split())
        expected = ' '.join(expected.split())
        self.assertEqual(result, expected)
    
    def test_join_with_parentheses(self):
        sql = "SELECT * FROM table1 JOIN logs ON (TARGET_TABLE.id = logs.tid AND valid_table.id = logs.vid)"
        expected = "SELECT * FROM table1 JOIN logs ON (valid_table.id = logs.vid)"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_with_target_reference_in_middle(self):
        sql = "SELECT * FROM table1 JOIN items ON valid_id = items.id AND TARGET_TABLE.status = items.status AND items.active = 1"
        expected = "SELECT * FROM table1 JOIN items ON valid_id = items.id AND items.active = 1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_with_target_reference_at_end(self):
        sql = "SELECT * FROM table1 JOIN archive ON valid_table.id = archive.valid_column AND TARGET_TABLE.id = archive.tid"
        expected = "SELECT * FROM table1 JOIN archive ON valid_table.id = archive.valid_column"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_with_no_target_references(self):
        sql = "SELECT * FROM table1 JOIN partners ON valid_table.id = partners.id"
        expected = "SELECT * FROM table1 JOIN partners ON valid_table.id = partners.id"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_join_with_similar_table_name(self):
        sql = "SELECT * FROM table1 JOIN TARGET_TABLE_HISTORY ON table1.id = TARGET_TABLE_HISTORY.id"
        expected = "SELECT * FROM table1 JOIN TARGET_TABLE_HISTORY ON table1.id = TARGET_TABLE_HISTORY.id"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_reversed_join_condition(self):
        sql = "SELECT * FROM table1 JOIN users ON users.id = TARGET_TABLE.user_id AND users.valid_id = valid_table.id"
        expected = "SELECT * FROM table1 JOIN users ON users.valid_id = valid_table.id"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_join_alias_and_where_conditions(self):
        sql = """
        SELECT main_table.*
        FROM main_table
        JOIN TARGET_TABLE t ON t.id = main_table.tid
        WHERE main_table.name = 'Example'
        AND t.status = 'active';
        """
        expected = """
        SELECT main_table.*
        FROM main_table
        WHERE main_table.name = 'Example';
        """
        result = self.handler.process(sql, self.tables_to_process)
        result = ' '.join(result.split())
        expected = ' '.join(expected.split())
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main() 