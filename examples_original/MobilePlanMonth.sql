set session_replication_role = replica;

insert into public.employee (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                             last_modified_date, first_name, middle_name, last_name, position_id, code,
                             team_id, recycle_bin_id)
values ('15cc0e3a-8921-1589-f7a4-c6fb6df38e66', 'иванов', 'acc', 2, '01', '2023-05-15 11:25:01.252000', '01',
        '2023-05-19 12:04:33.013000', 'иван', 'иванович', 'иванов', null, '0000000001',
        null, null);

insert into public.mobile_plan_month (id, version, plan_period,
                               plan_sum_month, plan_sum_day, plan_sum_fact, plan_type, agent_id, recycle_bin_id,
                               work_days_count, product_id, parent_id, unit)
values ('052d2837-bba6-aa92-4d37-ad94626487c6', 1, '2023-06-01 12:00:42.959000', 0, 0, 0, null,
        '15cc0e3a-8921-1589-f7a4-c6fb6df38e66', null, 23, null, null, null),
       ('97c855fe-ffec-ceef-d988-ce11a7c47f68', 1, '2023-06-01 12:00:42.959000', 10, 0, 5, 'OnlySum',
        '15cc0e3a-8921-1589-f7a4-c6fb6df38e66', null, 23, '7c8809ba-4b97-ee0f-a174-6d1c01015184',
        '052d2837-bba6-aa92-4d37-ad94626487c6', 'CURRENCY'),
       ('2fd0fd6e-d9f7-58d9-b8f3-7ad3a087bfca', 1, '2023-06-01 13:00:03.398000', 1, 0.043, 0.5, 'WeightPlan',
        '15cc0e3a-8921-1589-f7a4-c6fb6df38e66', null, 23, '7c8809ba-4b97-ee0f-a174-6d1c01015184',
        '052d2837-bba6-aa92-4d37-ad94626487c6', 'TON'),
       ('0000000e-d9f7-58d9-b8f3-0000a087bfca', 1, '2023-06-01 13:00:03.398000', 1, 0.043, 0.5, 'WeightPlan',
        '15cc0e3a-8921-1589-f7a4-c6fb6df38e66', null, 23, '7c8809ba-4b97-ee0f-a174-6d1c01015184',
        '052d2837-bba6-aa92-4d37-ad94626487c6', 'TON');