# SQL Cleaner Test Suite

This directory contains test files for the SQL Cleaner library, which processes SQL files to remove or modify statements related to specified tables.

## Test Files

### test_sql_processor.py

Tests the core SQL processing functionality:
- Table name extraction
- Direct insert statement removal
- Reference insert modification
- Multi-value insert handling

### test_where_conditions.py

Tests the WHERE condition removal functionality:
- Simple WHERE conditions (`WHERE target_id = 5`)
- Compound conditions (`WHERE target_id = 5 AND another_id = 6`)
- NULL checks (`WHERE target_id IS NULL`)
- Conditions not related to target tables
- Table references via aliases
- Complex nested conditions
- ORDER BY clause preservation

## Known Limitations

The current implementation has some limitations:
- Complex subqueries might not be properly handled
- Function expressions in WHERE clauses (like `EXTRACT(YEAR FROM target_date)`) may not be correctly parsed
- Some complex operator expressions (LIKE, BETWEEN) may have limited support

## Running Tests

To run all tests:
```bash
python3 -m unittest discover
```

To run specific test files:
```bash
python3 test_sql_processor.py
python3 test_where_conditions.py
```

## Future Improvements

Potential future improvements to the test suite:
1. Add more complex test cases
2. Add tests for edge cases and error conditions
3. Add performance tests for large SQL files
4. Improve test coverage for complex SQL constructs 