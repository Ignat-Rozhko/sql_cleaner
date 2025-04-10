
    -- Test 1: Simple;
    
    -- Test 2: WHERE p.version > 0;
    
    -- Test 3: WHERE clause with table alias;
    
    -- Test 4: Complex WHERE with AND conditions AND p.version > 0 ORDER BY p.name;
    
    -- Test 5: WHERE clause with no conditions that need removal
    SELECT p.id, p.name FROM product p 
    WHERE p.version > 0 AND p.name LIKE '%Test%';
    
    -- Test 6: More complex example with nested conditions and multiple joins
    SELECT p.id, p.name, c.name as company_name, u.username
    FROM product p 
    JOIN company c ON p.company_id = c.id
    JOIN users u ON p.created_by = u.id WHERE u.role = 'admin' ORDER BY p.name;
    