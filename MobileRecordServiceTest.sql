INSERT INTO mten_tenant (id, name, external_id, version, tenant_id)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'account1', 123, 1, '1');

INSERT INTO user_(id, version, tenant, username, first_name, last_name, password, active, dtype)
VALUES ('e0a569d4-9b32-0b2e-c09f-77ff0850976d', 1, '1', '1|admin', '1', 'Admin', '{noop}password',
        TRUE, 'AccountUser');

INSERT INTO sec_role_assignment(id, version, username, role_code, role_type, create_ts, created_by)
VALUES ('1d8bd433-7f52-4c56-32d4-47157a1c0d12', 2, '1|admin', 'account-exchange', 'resource',
        '2022-08-09 03:33:28.334', 'admin');

INSERT INTO employee (id, external_id, first_name, last_name, tenant_id, version, name)
VALUES ('425ce4e5-9cf6-11e5-ad8a-2c59e59d72e1', '325ce4e5-9cf6-11e5-ad8a-2c59e59d72e1', 'Vaska', 'Vaska', '1', 1,
        'черный лорд');

INSERT INTO storage (id, external_id, name, version, tenant_id)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', '48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'storage name', 1, '1');

INSERT INTO product (id, external_id, name, type_, is_directory, version, tenant_id)
VALUES ('93b35ec7-ce46-5444-ec49-a6e563dedc45', '93b35ec7-ce46-5444-ec49-a6e563dedc45', 'Стол',
        'PRODUCT', FALSE, 1, '1'),
       ('973494a6-d1aa-c915-de3f-6788f2884232', '973494a6-d1aa-c915-de3f-6788f2884232', 'Стул',
        'PRODUCT', FALSE, 1, '1');

INSERT INTO unit (id, external_id, name, version, short_name, tenant_id)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', '48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'unit name 1', 1, 'un1.', '1'),
       ('48f5c314-f5e2-06a1-8c9a-7ab03a823622', '48f5c314-f5e2-06a1-8c9a-7ab03a823622', 'unit name 2', 1, 'un2.', '1');

INSERT INTO product_unit (id, unit_id, product_id, coefficient, version)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        1, 1),
       ('48f5c314-f5e2-06a1-8c9a-7ab03a823622', '48f5c314-f5e2-06a1-8c9a-7ab03a823622',
        '973494a6-d1aa-c915-de3f-6788f2884232',
        10, 1);

INSERT INTO price_type (id, external_id, name, version, tenant_id)
VALUES ('20c94172-6f19-a3d4-a3ac-dd5e6b445db0', '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 'Закупочная', 1, '1');

INSERT INTO company (id, name, version, tenant_id)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'company name', 1, '1');

INSERT INTO currency (id, name, version, tenant_id)
VALUES ('42130483-df08-8445-00d1-4c208f339890', 'Тенге', 1, '1'),
       ('c70c8c81-2c1a-410b-9ff4-2c5de9127466', 'Рубли', 1, '1');

INSERT INTO cashier (id, external_id, name, last_modified_date, currency_id, tenant_id, version)
VALUES ('3bfc8376-bf78-41ef-8a22-73a3caa4ae36', '3bfc8376-bf78-41ef-8a22-73a3caa4ae35', 'test cashBox',
        '2020-12-31 00:00:00',
        '42130483-df08-8445-00d1-4c208f339890', '1', 1),
       ('39ce43f8-177d-4cf1-87b5-3069b19e57a6', '39ce43f8-177d-4cf1-87b5-3069b19e57a5', 'test cashBox2',
        '2020-12-31 00:00:00',
        '42130483-df08-8445-00d1-4c208f339890', '1', 1);

INSERT INTO client (id, external_id, name, debt, default_price_type_id, version, tenant_id)
VALUES ('58f5c314-f5e2-06a1-8c9a-7ab03a823611', '48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'client name', 2.55,
        '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 1, '1');

INSERT INTO client_contract (id, tenant_id, external_id, client_id, name, date, number, version)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823644', '1', '48f5c314-f5e2-06a1-8c9a-7ab03a823644', '58f5c314-f5e2-06a1-8c9a-7ab03a823611', 'contract name',
        '2022-01-01 00:00:00', '123', 1);

INSERT INTO client_outlet(id, external_id, tenant_id, name, version, client_id)
VALUES ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', '48f5c314-f5e2-06a1-8c9a-7ab03a823611', '1', 'outlet name', 1, '58f5c314-f5e2-06a1-8c9a-7ab03a823611');

UPDATE client
SET default_contract_id ='48f5c314-f5e2-06a1-8c9a-7ab03a823644'
WHERE id = '48f5c314-f5e2-06a1-8c9a-7ab03a823611';

UPDATE product
SET product_unit_id = '48f5c314-f5e2-06a1-8c9a-7ab03a823611'
WHERE id IN ('93b35ec7-ce46-5444-ec49-a6e563dedc45', '973494a6-d1aa-c915-de3f-6788f2884232');

