insert into mten_tenant (id, name, external_id, version, tenant_id)
values ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'account1', 123, 1, '1');

INSERT INTO user_ (id, version, username)
VALUES ('60885987-1b61-4247-94c7-dff348347f93', 1, 'user1');

insert into price_type (id, name, version, tenant_id)
values ('20c94172-6f19-a3d4-a3ac-dd5e6b445db0', 'Закупочная', 1, '1');

insert into product (id, external_id, name, type_, is_directory, version, tenant_id)
values ('93b35ec7-ce46-5444-ec49-a6e563dedc45', '93b35ec7-ce46-5444-ec49-a6e563dedc45', 'Стол',
        'PRODUCT', false, 1, '1'),
       ('973494a6-d1aa-c915-de3f-6788f2884232', '973494a6-d1aa-c915-de3f-6788f2884232', 'Стул',
        'PRODUCT', false, 1, '1');

insert into currency (id, name, version)
values ('42130483-df08-8445-00d1-4c208f339890', 'Тенге', 1);

insert into company (id, name, tenant_id, version, created_by, created_date, last_modified_date)
values ('edbc3c83-8721-8982-2aed-60aa2cf67022', 'organization1', '1', 1, 'account1', '2022-01-01 00:00:00',
        '2022-01-01 00:00:00');

insert into product_price (id, price_type_id, product_id, start_at, price, company_id, version) VALUES ('1fbb8a8a-e527-3775-5f49-1f15afb2d919', '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', '93b35ec7-ce46-5444-ec49-a6e563dedc45', '2022-01-01 00:00:00', 11, 'edbc3c83-8721-8982-2aed-60aa2cf67022', 1), ('25aa94d1-7b3a-d302-a557-43c847e47383', '20c94172-6f19-a3d4-a3ac-dd5e6b445db0', '973494a6-d1aa-c915-de3f-6788f2884232', '2022-01-01 00:00:00', 22, 'edbc3c83-8721-8982-2aed-60aa2cf67022', 1);

