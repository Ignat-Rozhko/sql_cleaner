set session_replication_role = replica;

insert into public.employee (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                             last_modified_date, first_name, middle_name, last_name, position_id, code,
                             team_id, recycle_bin_id)
values ('15cc0e3a-8921-1589-f7a4-c6fb6df38e66', 'иванов', 'acc', 2, '01', '2023-05-15 11:25:01.252000', '01',
        '2023-05-19 12:04:33.013000', 'иван', 'иванович', 'иванов', null, '0000000001',
        null, null);

