import re

def check_table_references(content, table_name):
    """
    Check for table references in ways not caught by extract_table_names.
    """
    content_lower = content.lower()
    table_lower = table_name.lower()
    
    # Check for table name in joins
    if f"join {table_lower}" in content_lower:
        return True
    
    # Check for table name in WHERE clauses (table reference or table_id reference)
    if f"{table_lower}." in content_lower or f"{table_lower}_id" in content_lower:
        return True
    
    # Check for direct table name mentioned in FROM clause
    if re.search(rf'from\s+{table_lower}\b', content_lower):
        return True
    
    return False

# Читаем файл
with open('agent_exporter.sql', 'r') as f:
    content = f.read()

# Проверяем ссылки на таблицу
if check_table_references(content, 'RECYCLE_BIN'):
    print("Файл содержит ссылки на таблицу RECYCLE_BIN")
else:
    print("Файл НЕ содержит ссылки на таблицу RECYCLE_BIN")

# Проверяем упоминание recycle_bin_id
if "recycle_bin_id" in content.lower():
    print("Файл содержит упоминания recycle_bin_id")
else:
    print("Файл НЕ содержит упоминания recycle_bin_id") 