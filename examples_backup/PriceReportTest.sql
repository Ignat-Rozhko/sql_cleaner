insert into public.user_ (id, version, username, first_name, last_name, password, email, active, time_zone_id, tenant, dtype)
values ('4f55b02c-a3e1-0a4d-cc9b-f34f67702756', 1, 'user', null, null, '{bcrypt}$2a$10$MyIcPRMEdWsRtQssdOGvo.v.SHT4EEj9aPBYSaBc1Vm0zaESShSAm', null, true, null, '1', 'AccountUser');

insert into public.currency (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  letter_code, digital_code)
values ('023cbb09-dc43-4325-9f9f-8c62cb803760', 'Тенге', '1', 1, 'admin', '2023-01-04 00:00:00.000000', null, '2022-02-22 22:22:22.000000', null,  'KZT', '398');

insert into public.price_type (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id)
values ('d3e0e4ba-3229-46cb-bd54-986725b62afe', 'Закупочная', '1', 1, 'admin', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', null),
       ('356a5135-35df-4743-bae7-4ec0e0ba142e', 'Розничная', '1', 1, 'admin', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', null);

insert into public.unit (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  short_name, code)
values ('ef65335e-03e7-496e-bba8-8170f4e3310b', 'Штука', '1', 1, 'admin', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', null, 'шт.', '1');

insert into public.product (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  parent_id, is_directory, type_, article_number, code)
values ('237b9c66-a5c8-48c9-87da-f3cd754150c3', 'group1', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', null,null, true, null, null, '0000000001'),
       ('d6bc281a-059c-8abf-8b42-147ef0f82302', 'group11', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', null, '237b9c66-a5c8-48c9-87da-f3cd754150c3', true, null, null, '0000000002'),
       ('756292ee-9e9d-fd6c-9b36-8d25327cd480', 'group111', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, 'd6bc281a-059c-8abf-8b42-147ef0f82302', true, null, null, '0000000003'),
       ('cdd897ca-3ab9-faf9-67d5-324098948746', 'product1', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, '756292ee-9e9d-fd6c-9b36-8d25327cd480', false, 'PRODUCT', null, '0000000004'),
       ('96297115-f664-76c9-5f65-9246d1f3ec9c', 'product2', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, '756292ee-9e9d-fd6c-9b36-8d25327cd480', false, 'PRODUCT', null, '0000000005'),
       ('2cf47f82-25ce-810c-cddf-346d8423cd3c', 'product3', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, 'd6bc281a-059c-8abf-8b42-147ef0f82302', false, 'PRODUCT', null, '0000000006'),
       ('e9727f3c-2676-eb5f-3780-1291494d7c95', 'product4', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, '756292ee-9e9d-fd6c-9b36-8d25327cd480', false, 'PRODUCT', null, '0000000007'),
       ('c039500a-ab3c-2eb7-997c-85dc0896ab68', 'group2', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000', null,null, true, null, null, '0000000008'),
       ('88fcb332-e41e-4199-3f3b-947483dc39d6', 'product5', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, 'c039500a-ab3c-2eb7-997c-85dc0896ab68', false, 'PRODUCT', null, '0000000009'),
       ('6cd7195f-1153-8c71-3280-c1fe8e4a2cfb', 'product6', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, 'c039500a-ab3c-2eb7-997c-85dc0896ab68', false, 'PRODUCT', null, '0000000010'),
       ('a3f0de43-b9c1-fd73-443a-88e5d05da9c6', 'product7', '1', 1, 'user', '2022-02-22 22:22:22.000000', null, '2022-02-22 22:22:22.000000',null, null, false, 'PRODUCT', null, '0000000011');

insert into public.product_unit (id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  unit_id, product_id, coefficient)
values ('f135ebd5-c8ef-9401-1b31-9ed68100cf03', 1, 'user', '2023-04-27 13:39:55.197000', null, '2023-04-27 13:39:55.197000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', 'cdd897ca-3ab9-faf9-67d5-324098948746', 1),
       ('ee7b1101-696d-bff1-dc97-8320a15d2e4d', 1, 'user', '2023-04-27 13:40:15.569000', null, '2023-04-27 13:40:15.569000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', '96297115-f664-76c9-5f65-9246d1f3ec9c', 1),
       ('b89346d4-487a-5a21-5196-1325b903a9b4', 1, 'user', '2023-04-27 13:40:31.614000', null, '2023-04-27 13:40:31.614000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', '2cf47f82-25ce-810c-cddf-346d8423cd3c', 1),
       ('7f62c93a-4dc5-c460-d119-68559154adb4', 1, 'user', '2023-04-27 13:40:49.772000', null, '2023-04-27 13:40:49.772000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', 'e9727f3c-2676-eb5f-3780-1291494d7c95', 1),
       ('3d6199ed-ed58-044e-ab4f-2e3349f150d2', 1, 'user', '2023-04-27 13:41:18.978000', null, '2023-04-27 13:41:18.978000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', '88fcb332-e41e-4199-3f3b-947483dc39d6', 1),
       ('5c73186b-d3bf-4bab-5173-d35cbfe2a024', 1, 'user', '2023-04-27 13:41:35.075000', null, '2023-04-27 13:41:35.075000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', '6cd7195f-1153-8c71-3280-c1fe8e4a2cfb', 1),
       ('7dd9620d-7d8f-132f-33e0-5049f35db0ec', 1, 'user', '2023-04-27 13:46:35.284000', null, '2023-04-27 13:46:35.284000', null, 'ef65335e-03e7-496e-bba8-8170f4e3310b', 'a3f0de43-b9c1-fd73-443a-88e5d05da9c6', 1);

UPDATE product SET product_unit_id = null WHERE id= '237b9c66-a5c8-48c9-87da-f3cd754150c3';
UPDATE product SET product_unit_id = null WHERE id= 'd6bc281a-059c-8abf-8b42-147ef0f82302';
UPDATE product SET product_unit_id = null WHERE id= '756292ee-9e9d-fd6c-9b36-8d25327cd480';
UPDATE product SET product_unit_id = 'f135ebd5-c8ef-9401-1b31-9ed68100cf03' WHERE id= 'cdd897ca-3ab9-faf9-67d5-324098948746';
UPDATE product SET product_unit_id = 'ee7b1101-696d-bff1-dc97-8320a15d2e4d' WHERE id= '96297115-f664-76c9-5f65-9246d1f3ec9c';
UPDATE product SET product_unit_id = 'b89346d4-487a-5a21-5196-1325b903a9b4' WHERE id= '2cf47f82-25ce-810c-cddf-346d8423cd3c';
UPDATE product SET product_unit_id = '7f62c93a-4dc5-c460-d119-68559154adb4' WHERE id= 'e9727f3c-2676-eb5f-3780-1291494d7c95';
UPDATE product SET product_unit_id = null WHERE id= 'c039500a-ab3c-2eb7-997c-85dc0896ab68';
UPDATE product SET product_unit_id = '3d6199ed-ed58-044e-ab4f-2e3349f150d2' WHERE id= '88fcb332-e41e-4199-3f3b-947483dc39d6';
UPDATE product SET product_unit_id = '5c73186b-d3bf-4bab-5173-d35cbfe2a024' WHERE id= '6cd7195f-1153-8c71-3280-c1fe8e4a2cfb';
UPDATE product SET product_unit_id = '7dd9620d-7d8f-132f-33e0-5049f35db0ec' WHERE id= 'a3f0de43-b9c1-fd73-443a-88e5d05da9c6';

insert into public.storage (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  code)
values ('7cd41c60-d4c4-05bc-28b8-30e59fc792bc', 'storage', '1', 1, 'user', '2023-04-27 14:59:59.617000' , null, '2023-04-27 14:59:59.617000', null, '0000000001');

insert into public.company (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  identification_number, legal_address, real_address, email, contact_phone, beneficiary_code, vat_certificate_series, vat_certificate_number, vat_certificate_date, storage_id, cashier_id, bank_account_id, director_employee_id, accountant_general_employee_id, code)
values ('bfb85dbe-a557-abb3-4490-fc2c241db760', 'company', '1', 1, 'user', '2023-04-27 13:39:10.605000', null, '2023-04-27 15:00:11.656000', null, null, null, null, null, null, null, null, null, null, '7cd41c60-d4c4-05bc-28b8-30e59fc792bc', null, null, null, null, '0000000001');

insert into public.product_balance (id, product_id, storage_id, amount, created_by, created_date, recycle_bin_id,  last_modified_by, last_modified_date, version, company_id)
values ('e26d6c54-f876-b39e-ef3c-b6ea0413328a', '6cd7195f-1153-8c71-3280-c1fe8e4a2cfb', '7cd41c60-d4c4-05bc-28b8-30e59fc792bc', 2.000, 'user', '2023-04-27 15:01:15.872000', null, null, '2023-04-27 15:01:15.872000', 1, 'bfb85dbe-a557-abb3-4490-fc2c241db760');

insert into public.price_change (id, number, date, document_state, document_type, user_id, currency_id, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id,  price_type_id, company_id, note)
values ('96c75db7-35d3-0948-4515-3350be4940e9', '000000000000001', '2023-04-27 13:52:06.955000', 'APPLIED', 'PRICE_CHANGE', '4f55b02c-a3e1-0a4d-cc9b-f34f67702756', '023cbb09-dc43-4325-9f9f-8c62cb803760', '1', 1, 'user', '2023-04-27 13:52:07.022000', null, '2023-04-27 13:52:07.022000', null, 'd3e0e4ba-3229-46cb-bd54-986725b62afe', 'bfb85dbe-a557-abb3-4490-fc2c241db760', null);

insert into public.product_price (id, price_change_id, start_at, price_type_id, product_id, price, company_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id)
values ('cf90d33d-0bf0-0a94-672f-08e73d7674f3', '96c75db7-35d3-0948-4515-3350be4940e9', '2023-04-27 00:00:00.000000', 'd3e0e4ba-3229-46cb-bd54-986725b62afe', '2cf47f82-25ce-810c-cddf-346d8423cd3c', 32.00, 'bfb85dbe-a557-abb3-4490-fc2c241db760', 1, 'user', '2023-04-27 13:52:07.045000', null, '2023-04-27 13:52:07.045000', null),
       ('762c6eae-8989-693f-b551-375b0a5d2cb2', '96c75db7-35d3-0948-4515-3350be4940e9', '2023-04-27 00:00:00.000000', 'd3e0e4ba-3229-46cb-bd54-986725b62afe', 'cdd897ca-3ab9-faf9-67d5-324098948746', 12.00, 'bfb85dbe-a557-abb3-4490-fc2c241db760', 1, 'user', '2023-04-27 13:52:07.045000', null, '2023-04-27 13:52:07.045000', null);

insert into public.price_change_product_price (id, price_change_id, product_id, price, number, version)
values ('216ea913-7af3-5c82-14e0-f215a50d632e', '96c75db7-35d3-0948-4515-3350be4940e9', '2cf47f82-25ce-810c-cddf-346d8423cd3c', 32.00, 2, 1),
       ('59cc5cf3-4230-cb06-c59a-2e17d2973ba5', '96c75db7-35d3-0948-4515-3350be4940e9', 'cdd897ca-3ab9-faf9-67d5-324098948746', 12.00, 1, 1);

insert into public.user_setting (id, version, created_by)
values ('33b4ef07-4e81-d986-3e5c-9a4c9e3bb63d', 1, 'admin');

UPDATE user_setting SET default_company_id = 'bfb85dbe-a557-abb3-4490-fc2c241db760' WHERE id = '33b4ef07-4e81-d986-3e5c-9a4c9e3bb63d';
UPDATE user_ SET user_setting_id = '33b4ef07-4e81-d986-3e5c-9a4c9e3bb63d' WHERE id = '4f55b02c-a3e1-0a4d-cc9b-f34f67702756';

insert into public.sec_role_assignment (id, version, create_ts, created_by, update_ts, updated_by, delete_ts, deleted_by, username, role_code, role_type)
VALUES ('198d4269-ccdb-3d4d-551c-9e8532a28459', 1, '2023-05-18 16:18:30.641000', 'admin', '2023-05-18 16:18:30.641000', null, null, null, 'user', 'account-admin', 'resource'),
       ('7b923536-5895-e477-ef2a-7060032dc375', 1, '2023-05-18 16:18:30.671000', 'admin', '2023-05-18 16:18:30.671000', null, null, null, 'user', 'custom-report-run', 'resource');

