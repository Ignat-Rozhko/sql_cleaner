
    -- Test 1: Simple;
    
    -- Test 2:;
    
    -- Test 3: WHERE clause with table alias AND c.tenant_id = 'example';
    
    -- Test 4: Complex WHERE with AND conditions ORDER BY p.name;
    
    -- Test 5:;
    
    -- Test 6: More complex example with nested conditions and multiple joins
    SELECT p.id, p.name, c.name as company_name, u.username
    FROM product p 
    JOIN company c ON p.company_id = c.id
    JOIN users u ON p.created_by = u.id WHERE u.role = 'admin' ORDER BY p.name;
    