import unittest
import sys
import os

# Get the absolute path of the parent directory (the sql_cleaner package)
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(PACKAGE_ROOT, '..')))

from sql_cleaner.processor.sql_processor import SQLProcessor


class TestInsertStatements(unittest.TestCase):
    def setUp(self):
        self.processor = SQLProcessor()
        
    def test_extract_table_names(self):
        sql_content = """
        insert into table1 (col1, col2) values (1, 2);
        INSERT INTO table2 (col1, col2) VALUES (3, 4);
        insert into TABLE3 (col1, col2, col3) values (5, 6, 7);
        """
        tables = self.processor.extract_table_names(sql_content)
        expected_tables = {'table1', 'table2', 'table3'}
        self.assertEqual(tables, expected_tables)
        
    def test_direct_insert_removal(self):
        """Test removal of direct insert statements for a specific table"""
        sql_content = """
        insert into table1 (col1, col2) values (1, 2);
        INSERT INTO table2 (col1, col2) VALUES (3, 4);
        insert into table1 (col1, col2, col3) values (5, 6, 7);
        """
        processed = self.processor.process_sql_content(sql_content, ['table1'])
        
        # The first table1 insert should be removed
        # Verify the first insert is removed
        self.assertNotIn("table1 (col1, col2) values (1, 2)", processed.lower())
        self.assertNotIn("table1 (col1, col2, col3) values (5, 6, 7)", processed.lower())
        
        # Verify table2 insert remains
        self.assertIn("table2", processed.lower())
        
    def test_multiline_direct_insert_removal(self):
        """Test removal of multiline direct insert statements"""
        sql_content = """
        insert into table1 (col1, col2) 
        values (1, 2);
        
        INSERT INTO table2 (col1, col2) 
        VALUES (3, 4);
        
        insert into table1 (col1, 
                          col2, 
                          col3) 
        values (5, 
               6, 
               7);
        """
        processed = self.processor.process_sql_content(sql_content, ['table1'])
        
        # Should not contain the first table1 insert
        self.assertNotIn("table1 (col1, col2)", processed.lower())
        self.assertNotIn("col3", processed.lower())
        
        # Should contain the table2 insert
        self.assertIn("INSERT INTO table2", processed)
        
    def test_reference_insert_modification(self):
        """Test modification of insert statements referencing a table"""
        sql_content = """
        insert into other_table (id, name, table1_id, created_date)
        values (1, 'test', 100, '2022-01-01');
        insert into other_table (id, name, table1_id, created_date)
        values (1, 'test', 100, '2022-01-01');
        """
        processed = self.processor.process_sql_content(sql_content, ['table1'])
        
        # Should remove the table1_id column and its value
        self.assertIn("other_table", processed.lower())
        self.assertNotIn("table1_id", processed.lower())
        
        # Verify that id, name, and created_date remain
        processed_no_spaces = processed.replace(" ", "").lower()
        self.assertIn("(id,name,created_date)", processed_no_spaces)
        self.assertIn("(1,'test','2022-01-01')", processed_no_spaces)
        self.assertNotIn("100", processed_no_spaces)
        
    def test_complex_case_with_company_table(self):
        """Test with a real example similar to the provided SQL files"""
        sql_content = """
        insert into company (id, name, tenant_id, version, created_by, created_date, last_modified_date)
        values ('edbc3c83-8721-8982-2aed-60aa2cf67022', 'organization1', '1', 1, 'account1', '2022-01-01 00:00:00',
                '2022-01-01 00:00:00');
                
        insert into price_change (id, version, number, date, document_state, user_id, price_type_id, company_id, tenant_id,
                                currency_id)
        values ('ca9e7aa9-81cf-a73c-4129-28c8c8fb3a0e', '1', '1', '2022-01-01 00:00:00', 'DRAFT',
                '60885987-1b61-4247-94c7-dff348347f93',
                '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 'edbc3c83-8721-8982-2aed-60aa2cf67022', '1',
                '42130483-df08-8445-00d1-4c208f339890'),
            ('ca9e7aa9-81cf-a73c-4129-28c8c8fb3a0e', '1', '1', '2022-01-01 00:00:00', 'DRAFT',
                '60885987-1b61-4247-94c7-dff348347f93',
                '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 'bdbc3c83-8721-8982-2aed-60aa2cf67022', '1',
                '42130483-df08-8445-00d1-4c208f339890');

        insert into company (id, name, tenant_id, version, created_by, created_date, last_modified_date)
        values ('edbc3c83-8721-8982-2aed-60aa2cf67022', 'organization1', '1', 1, 'account1', '2022-01-01 00:00:00',
                '2022-01-01 00:00:00');
                
                
        insert into price_change (id, version, number, date, document_state, user_id, price_type_id, company_id, tenant_id,
                                currency_id)
        values ('ca9e7aa9-81cf-a73c-4129-28c8c8fb3a0e', '1', '1', '2022-01-01 00:00:00', 'DRAFT',
                '60885987-1b61-4247-94c7-dff348347f93',
                '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 'edbc3c83-8721-8982-2aed-60aa2cf67022', '1',
                '42130483-df08-8445-00d1-4c208f339890'),
            ('ca9e7aa9-81cf-a73c-4129-28c8c8fb3a0e', '1', '1', '2022-01-01 00:00:00', 'DRAFT',
                '60885987-1b61-4247-94c7-dff348347f93',
                '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 'bdbc3c83-8721-8982-2aed-60aa2cf67022', '1',
                '42130483-df08-8445-00d1-4c208f339890');
        """
        
        # Test processing the company table
        processed = self.processor.process_sql_content(sql_content, ['company'])
        
        # Direct insert into company should be removed
        self.assertNotIn("company (id", processed.lower())
        
        # Reference to company_id should be removed
        self.assertIn("price_change", processed.lower())
        self.assertNotIn("company_id", processed.lower())
        self.assertNotIn("'edbc3c83-8721-8982-2aed-60aa2cf67022'", processed.lower())
        self.assertNotIn("'bdbc3c83-8721-8982-2aed-60aa2cf67022'", processed.lower())
        
    def test_price_table_processing(self):
        """Test with a price table example"""
        sql_content = """
        insert into price (id, product_id, price_type_id, value, version)
        values ('5fbb8a8a-e527-3775-5f49-1f15afb2d919', '93b35ec7-ce46-5444-ec49-a6e563dedc45',
                '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 100, 1);
                
        insert into price_history (id, price_id, value, start_date, end_date, version)
        values ('a5aa94d1-7b3a-d302-a557-43c847e47383', '5fbb8a8a-e527-3775-5f49-1f15afb2d919',
                100, '2022-01-01', '2022-12-31', 1);
        """
        
        # Test processing the price table
        processed = self.processor.process_sql_content(sql_content, ['price'])
        
        # Direct insert into price should be removed
        self.assertNotIn("price (id", processed.lower())
        
        # Reference to price_id should be removed
        self.assertIn("price_history", processed.lower())
        self.assertNotIn("price_id", processed.lower())
        
    def test_multi_value_insert(self):
        """Test processing a multi-value INSERT statement"""
        sql_content = """
        INSERT INTO company (id, name, tenant_id, version)
        VALUES ('c276c9f6-7da6-4622-818b-b1d837fc8142', 'ТОО "Трэйд"', 'example', 1),
               ('c276c9f6-7da6-4622-818b-b1d837fc9253', 'my fail company', 'example', 1);
        
        INSERT INTO product (id, name, company_id, version)
        VALUES ('dd76c9f6-7da6-4622-818b-b1d837fc8142', 'Product 1', 'c276c9f6-7da6-4622-818b-b1d837fc8142', 1),
               ('ee76c9f6-7da6-4622-818b-b1d837fc9253', 'Product 2', 'c276c9f6-7da6-4622-818b-b1d837fc9253', 1);
        """
        
        # Test direct multi-value INSERT removal
        processed = self.processor.process_sql_content(sql_content, ['company'])
        
        # Direct insert into company should be removed
        self.assertNotIn("company (id", processed.lower())
        
        # But product insert should remain
        self.assertIn("product", processed.lower())
        
        # Company_id should be removed from product insert
        self.assertNotIn("company_id", processed.lower())
        
        # Check that the values are correctly removed as well
        self.assertNotIn("c276c9f6-7da6-4622-818b-b1d837fc8142", processed)
        self.assertNotIn("c276c9f6-7da6-4622-818b-b1d837fc9253", processed)
        
    def test_recycle_bin_id_removal(self):
        """Test that recycle_bin_id is properly removed from complex multiline INSERT statements"""
        sql_content = """
        insert into public.currency (id, name, letter_code, digital_code, created_by, created_date,
                                 last_modified_by,
                                 last_modified_date, recycle_bin_id, version, tenant_id)
        values (gen_random_uuid(), 'Тенге', 'KZT', '398', 'admin', '2022-02-22 22:22:22.000000', null,
                '2022-02-22 22:22:22.000000', null, 1, ?);
        """
        
        # Process the SQL with recycle_bin in tables_to_process
        processed = self.processor.process_sql_content(sql_content, ['recycle_bin'])
        
        # Verify that recycle_bin_id column is removed
        self.assertIn("currency", processed.lower())
        self.assertNotIn("recycle_bin_id", processed.lower())
        
        # Verify the value structure is preserved correctly without extra parentheses
        self.assertIn("values (gen_random_uuid(), 'Тенге', 'KZT', '398', 'admin', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', 1, ?);", processed)
        
        # Verify no duplicate closing parentheses
        self.assertNotIn("));", processed)


if __name__ == '__main__':
    unittest.main() 