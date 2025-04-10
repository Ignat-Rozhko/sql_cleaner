# SQL Cleaner

A Python utility for cleaning SQL files by removing specific table inserts and references.

## Features

- Recursively finds SQL files in a directory
- Removes direct INSERT statements for specified tables
- Removes references to specified tables in other INSERT statements
- Handles multi-value INSERT statements (e.g., `VALUES (...), (...), (...)`)
- Preserves the structure of SQL files
- Works with complex SQL statements and maintains formatting

## Usage

### Command Line

```bash
python sql_cleaner.py <directory> [table1 table2 ...]
```

- `<directory>`: Directory to search for SQL files recursively
- `[table1 table2 ...]`: Optional list of tables to process (if not provided, all tables found will be processed)

### Programmatic Usage

```python
from sql_cleaner import SQLFileFinder, SQLProcessor

# Find SQL files
finder = SQLFileFinder('/path/to/sql/files')
sql_files = finder.find_sql_files()

# Process a specific file
processor = SQLProcessor()
with open(sql_files[0], 'r', encoding='utf-8') as f:
    content = f.read()

# Clean specific tables
processed_content = processor.process_sql_content(content, ['company', 'price'])

# Write back to file
with open(sql_files[0], 'w', encoding='utf-8') as f:
    f.write(processed_content)
```

## Testing

Run the tests using:

```bash
python -m unittest test_sql_processor.py
```

## Examples

The tool is designed to:

1. Remove direct inserts into specified tables:
   ```sql
   -- Before:
   insert into company (id, name) values (1, 'name');
   
   -- After: (completely removed)
   ```

2. Remove references to specified tables in other inserts:
   ```sql
   -- Before:
   insert into price_change (id, company_id, value) values (1, 2, 100);
   
   -- After:
   insert into price_change (id, value) values (1, 100);
   ```

3. Handle multi-value INSERT statements:
   ```sql
   -- Before:
   INSERT INTO product (id, name, company_id, version)
   VALUES ('prod1', 'Product 1', 'comp1', 1),
          ('prod2', 'Product 2', 'comp2', 1);
   
   -- After (when removing company table references):
   INSERT INTO product (id, name, version)
   VALUES ('prod1', 'Product 1', 1),
          ('prod2', 'Product 2', 1);
   ``` 