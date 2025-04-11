import unittest
from sql_cleaner.processor.comment_removal_handler import CommentRemovalHandler


class TestCommentRemovalHandler(unittest.TestCase):
    def setUp(self):
        self.handler = CommentRemovalHandler()
        self.tables_to_process = ["TARGET_TABLE"]

    def test_single_line_comment_removal(self):
        sql = "SELECT * FROM table1 -- This is a comment"
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_multiple_single_line_comments(self):
        sql = """
        SELECT * FROM table1 -- This is a comment
        WHERE id = 1 -- Another comment
        """
        expected = "SELECT * FROM table1 WHERE id = 1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_multi_line_comment_removal(self):
        sql = """
        SELECT * FROM table1
        /* This is a
        multi-line
        comment */
        WHERE id = 1
        """
        expected = "SELECT * FROM table1 WHERE id = 1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_nested_comments_are_removed(self):
        sql = """
        SELECT *
        /* Outer comment
           /* Nested comment */
           Still in outer comment
        */ 
        FROM table1
        """
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_comment_in_string_literals_preserved(self):
        sql = "SELECT '-- This is not a comment' FROM table1"
        expected = "SELECT '-- This is not a comment' FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_mixed_comments(self):
        sql = """
        SELECT 
            col1, -- Comment 1
            /* Multi-line
            comment */
            col2, 
            col3 -- Comment 2
        FROM table1
        """
        expected = "SELECT col1, col2, col3 FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_comment_at_beginning(self):
        sql = """
        -- Initial comment
        SELECT * FROM table1
        """
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)

    def test_comment_at_end(self):
        sql = """
        SELECT * FROM table1
        -- Final comment
        """
        expected = "SELECT * FROM table1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)
    
    def test_no_comments(self):
        sql = "SELECT * FROM table1 WHERE id = 1"
        expected = "SELECT * FROM table1 WHERE id = 1"
        result = self.handler.process(sql, self.tables_to_process)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main() 