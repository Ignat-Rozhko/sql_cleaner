INSERT INTO mten_tenant(id, version, tenant_id, name, external_id, dtype, create_ts, created_by)
VALUES ('1126775d-4d03-085b-44c2-003b92dc6283', 3, 'example', 'Account', 5, 'Account', '2020-12-31 00:00:00', 'admin');

INSERT INTO user_(id, version, tenant, username, first_name, last_name, password, active, dtype)
VALUES ('e0a569d4-9b32-0b2e-c09f-77ff0850976d', 1, 'example', 'example|admin', 'Example', 'Admin', '{noop}password',
        true, 'AccountUser');

INSERT INTO sec_role_assignment(id, version, username, role_code, role_type, create_ts, created_by)
VALUES ('1d8bd433-7f52-4c56-32d4-47157a1c0d12', 2, 'example|admin', 'account-admin', 'resource',
        '2022-08-09 03:33:28.334', 'admin');

INSERT INTO company (id, name, tenant_id, version)
VALUES ('c276c9f6-7da6-4622-818b-b1d837fc8142', 'ТОО "Трэйд"', 'example', 1),
       ('c276c9f6-7da6-4622-818b-b1d837fc9253', 'my fail company', 'example', 1);

INSERT INTO storage(id, name, last_modified_date, version, tenant_id)
VALUES ('0c6d48f3-f5b2-11e4-b7e2-f2fede4d0845', 'test storage', '2020-12-31 00:00:00', 1, 'example'),
       ('5e05e110-dc6f-4a9a-a3f3-93c84181c3d7', 'test2 storage', '2020-12-31 00:00:00', 1, 'example');

INSERT INTO price_type(id, name, last_modified_date, version, tenant_id)
VALUES ('92a557c6-1782-11e8-80cd-2c59e59d72e1', 'test price type', '2020-12-31 00:00:00', 1, 'example'),
       ('93a667c6-1782-11e8-80cd-2c59e59d72e1', 'second test price type', '2020-12-31 00:00:00', 1, 'example');

INSERT INTO employee (id, first_name, last_name, middle_name, tenant_id, version, name)
VALUES ('ff782e2b-cf1f-11df-909f-00241d21221f', 'Vaska', 'Vaska', 'Vaska', 'example', 1, 'черный лорд'),
       ('ff782e4b-cf1f-11df-909f-00241d21221f', 'led', 'tv', 'show', 'example', 1, 'star лорд');

INSERT INTO license(id, last_modified_date,
                    version, tenant_id, company_id, agent_uuid, code)
VALUES ('a62cea1e-e47e-48ab-a33a-3786b798bf4f', '2020-12-31 00:00:00', 1, 'example',
        'c276c9f6-7da6-4622-818b-b1d837fc8142',
        'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
       ('a62cea3e-e47e-48ab-a33a-3786b798bf4f', '2020-12-31 00:00:00', 1, 'example',
        'c276c9f6-7da6-4622-818b-b1d837fc8142',
        'ff782e4b-cf1f-11df-909f-00241d21221f', 1);

INSERT INTO currency (id, name, letter_code, version, tenant_id)
VALUES ('42130483-df08-8445-00d1-4c208f339890', 'Тенге', 'KZT', 1, 'example'),
       ('c70c8c81-2c1a-410b-9ff4-2c5de9127466', 'Рубли', 'RUB', 1, 'example');

INSERT INTO agent_setting (id, currency_id, can_change_price, can_create_partners, main_storage_id, main_price_type_id,
                    check_outlet_gps, is_hard_route, is_check_gps, default_delivery_date, use_agreements,
                    last_modified_date,
                    version, tenant_id, radius_gps, employee_id, recycle_bin_id, set_price_type_from_order, add_article_to_product_name)
VALUES ('a62cea1e-e47e-48ab-a33a-3786b798bf4f', 'c70c8c81-2c1a-410b-9ff4-2c5de9127466', false, false, '0c6d48f3-f5b2-11e4-b7e2-f2fede4d0845',
        '92a557c6-1782-11e8-80cd-2c59e59d72e1',
        true, true, true, 1, false, '2020-12-31 00:00:00', 1, 'example', 100,
        'ff782e2b-cf1f-11df-909f-00241d21221f', null, false, false),
       ('a62cea3e-e47e-48ab-a33a-3786b798bf4f', 'c70c8c81-2c1a-410b-9ff4-2c5de9127466', false, false, '0c6d48f3-f5b2-11e4-b7e2-f2fede4d0845',
        '92a557c6-1782-11e8-80cd-2c59e59d72e1',
        true, true, true, 1, false, '2020-12-31 00:00:00', 1, 'example', 100,
        'ff782e4b-cf1f-11df-909f-00241d21221f', null, false, false);

INSERT INTO product(id, external_id, name, tenant_id, version, created_date, last_modified_date, is_directory, parent_id, recycle_bin_id)
VALUES ('42a8f484-ecd0-4042-be9a-359eba4ebf1f', '42a8f484-ecd0-4042-be9a-359eba4ebf1f', 'test dir', 'example', 1,
        '2011-12-31 00:00:00', '2011-12-31 00:00:00', true, null, null),
       ('4bc39a16-869f-4cfc-8c5f-5d84ab69d6eb', '4bc39a16-869f-4cfc-8c5f-5d84ab69d6eb', 'test product', 'example', 1,
        '2020-12-31 00:00:00', '2021-12-31 00:00:00', false, null, null),
       ('8067a2ad-2b78-4983-b521-33553309276a', '8067a2ad-2b78-4983-b521-33553309276a', 'test dir2', 'example', 1,
        '2020-12-31 00:00:00', null, true, null, null),
       ('8487bcd7-0e0a-46ea-970f-b918f77fd27c', '8487bcd7-0e0a-46ea-970f-b918f77fd27c', 'test dir3', 'example', 1,
        '2020-12-31 00:00:00', '2021-12-31 00:00:00', true, null, null),
       ('ff6639e4-4d50-4bf3-92d2-bfb93f1a8883', 'ff6639e4-4d50-4bf3-92d2-bfb93f1a8883', 'test dir4', 'example', 1,
        '2020-12-31 00:00:00', null, true, null, null),
       ('15b108af-4691-447c-a162-22c909e6c417', '15b108af-4691-447c-a162-22c909e6c417', 'test dir5', 'example', 1,
        '2020-12-31 00:00:00', null, true, null, null),
       ('136262f5-50e1-44e9-8c20-2f2fdbd50635', '136262f5-50e1-44e9-8c20-2f2fdbd50635', 'test dir6', 'example', 1,
        '2010-12-31 00:00:00', null, true, null, null),
       ('137262f5-50e1-44e9-8c20-2f2fdbd50635', '137262f5-50e1-44e9-8c20-2f2fdbd50635', 'test dir 7', 'example', 1,
        '2010-12-31 00:00:00', null, true, null, null),
       ('137372f9-50e1-44e9-8c20-2f2fdbd50635', '137372f9-50e1-44e9-8c20-2f2fdbd50635', 'test dir 8 child', 'example', 1,
        '2010-12-31 00:00:00', null, true, '42a8f484-ecd0-4042-be9a-359eba4ebf1f', null),
       ('19812f85-8d5a-4d83-8516-cec5067fbc9d', '19812f85-8d5a-4d83-8516-cec5067fbc9d', 'test product2', 'example', 1,
        '2010-12-31 00:00:00', null, false, '42a8f484-ecd0-4042-be9a-359eba4ebf1f', null),
       ('d23b0bb9-5ea2-4da2-a6dd-ff4a95199513', 'd23b0bb9-5ea2-4da2-a6dd-ff4a95199513', 'test product3', 'example', 1,
        '2020-12-31 00:00:00', null, false, '42a8f484-ecd0-4042-be9a-359eba4ebf1f', null),
       ('4de38476-1d4f-4472-9c5c-a36087cf20fb', '4de38476-1d4f-4472-9c5c-a36087cf20fb', 'test product3', 'example', 1,
        '2020-12-31 00:00:00', null, false, '42a8f484-ecd0-4042-be9a-359eba4ebf1f', null);

-- product 4de38476-1d4f-4472-9c5c-a36087cf20fb
INSERT INTO product_price (id, start_at, price_type_id, product_id, price, company_id, version)
values ('92a667c6-1782-11e8-80cd-2c59e59d72e1', '2022-03-03', '92a557c6-1782-11e8-80cd-2c59e59d72e1',
        '4de38476-1d4f-4472-9c5c-a36087cf20fb', 500, 'c276c9f6-7da6-4622-818b-b1d837fc8142', 1),
       ('92a777c6-1782-11e8-80cd-2c59e59d72e1', '2022-03-03', '93a667c6-1782-11e8-80cd-2c59e59d72e1',
        '4de38476-1d4f-4472-9c5c-a36087cf20fb', 400, 'c276c9f6-7da6-4622-818b-b1d837fc9253', 1);

INSERT INTO product_balance (id, product_id, storage_id, amount, version, company_id)
VALUES ('92a667c6-1782-11e8-80cd-2c59e59d72e1', '4de38476-1d4f-4472-9c5c-a36087cf20fb',
        '0c6d48f3-f5b2-11e4-b7e2-f2fede4d0845', 333, 1, 'c276c9f6-7da6-4622-818b-b1d837fc8142'),
       ('92a777c6-1782-11e8-80cd-2c59e59d72e1', '4de38476-1d4f-4472-9c5c-a36087cf20fb',
        '5e05e110-dc6f-4a9a-a3f3-93c84181c3d7', 666, 1, 'c276c9f6-7da6-4622-818b-b1d837fc9253');

INSERT INTO product_agent (id, created_date, last_modified_date, product_id, agent_id, version)
VALUES
    ('1f2b9211-5baf-465d-86f8-981bff92b61c', '2020-12-31 00:00:00', '2020-12-31 00:00:00',
     '42a8f484-ecd0-4042-be9a-359eba4ebf1f', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
    ('37075f48-ea2c-4e17-9039-96d243984729', '2020-12-31 00:00:00', '2020-12-31 00:00:00',
     '8067a2ad-2b78-4983-b521-33553309276a', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
    ('3ea8bae5-ce34-407c-b7c2-5ca702589b18', '2020-12-31 00:00:00', '2020-12-31 00:00:00',
     '8487bcd7-0e0a-46ea-970f-b918f77fd27c', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
    ('3f80ff79-b1af-4ccf-a7c6-3083e770f237', '2020-12-31 00:00:00', '2020-12-31 00:00:00',
     'ff6639e4-4d50-4bf3-92d2-bfb93f1a8883', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
    ('d71ce70d-bca1-47b1-9271-67de75a3f57d', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
     '15b108af-4691-447c-a162-22c909e6c417', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
    ('ee7be3a8-cdbe-49c9-8e71-38f766e6e41e', '2010-12-31 00:00:00', null, '136262f5-50e1-44e9-8c20-2f2fdbd50635',
     'ff782e2b-cf1f-11df-909f-00241d21221f', 1);


INSERT INTO price_agent (id, created_date, last_modified_date, price_id, agent_id, version)
values ('92a557c9-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '92a557c6-1782-11e8-80cd-2c59e59d72e1', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
       ('92a557c6-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '93a667c6-1782-11e8-80cd-2c59e59d72e1', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
       ('92a557c8-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '92a557c6-1782-11e8-80cd-2c59e59d72e1', 'ff782e4b-cf1f-11df-909f-00241d21221f', 1),
       ('92a557c5-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '93a667c6-1782-11e8-80cd-2c59e59d72e1', 'ff782e4b-cf1f-11df-909f-00241d21221f', 1);

INSERT INTO storage_agent (id, created_date, last_modified_date, storage_id, agent_id, version)
values ('92a557c9-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '0c6d48f3-f5b2-11e4-b7e2-f2fede4d0845', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
       ('92a557c6-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '5e05e110-dc6f-4a9a-a3f3-93c84181c3d7', 'ff782e2b-cf1f-11df-909f-00241d21221f', 1),
       ('92a557c8-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '0c6d48f3-f5b2-11e4-b7e2-f2fede4d0845', 'ff782e4b-cf1f-11df-909f-00241d21221f', 1),
       ('92a557c5-1782-11e8-80cd-2c59e59d72e1', '2010-12-31 00:00:00', '2010-12-31 00:00:00',
        '5e05e110-dc6f-4a9a-a3f3-93c84181c3d7', 'ff782e4b-cf1f-11df-909f-00241d21221f', 1);