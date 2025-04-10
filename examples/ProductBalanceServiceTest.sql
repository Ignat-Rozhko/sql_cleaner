insert into mten_tenant (id, name, external_id, version, tenant_id)
values ('e7422469-324a-49a5-b798-dac05a0d1242', 'account1', 123, 1, '1');

insert into user_ (id, version, username, tenant, dtype)
VALUES ('dbd0646a-e22f-5587-2758-dc44810e91b1', 1, 'user1', '1', 'AccountUser');

insert into storage (id, name, version, tenant_id)
values ('fc1f671f-876f-1163-6da1-d9ab14f649f3', 'storage name1', 1, '1'),
       ('0934b00a-aecd-b0ef-8dfd-ac2f67937a1a', 'storage name2', 1, '1');

insert into product (id, external_id, name, type_, is_directory, version, tenant_id)
values ('93b35ec7-ce46-5444-ec49-a6e563dedc45', '93b35ec7-ce46-5444-ec49-a6e563dedc45', 'Стол', 'PRODUCT', false, 1, '1'),
       ('973494a6-d1aa-c915-de3f-6788f2884232', '973494a6-d1aa-c915-de3f-6788f2884232', 'Стул', 'PRODUCT', false, 1, '1'),
       ('973494a6-d1aa-c915-de3f-6788f2884211', '973494a6-d1aa-c915-de3f-6788f2884211', 'Диван', 'PRODUCT', false, 1, '1');

insert into unit (id, external_id, name, version, short_name, tenant_id, code)
values ('4eeb5be2-479d-f7ca-fa23-c628775ba5b2', '4eeb5be2-479d-f7ca-fa23-c628775ba5b2', 'unit name 1', 1, 'un1.', '1', '0000000001'),
       ('670a8f85-36ea-9a0e-0726-66720daf6ae3', '670a8f85-36ea-9a0e-0726-66720daf6ae3', 'unit name 2', 1, 'un2.', '1', '0000000002');

insert into product_unit (id, unit_id, product_id, coefficient, version)
values ('32364ec1-a073-b750-12d9-b2c9cccb7830', '4eeb5be2-479d-f7ca-fa23-c628775ba5b2',
        '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        1, 1),
       ('764129db-92e2-4a9b-d31b-b7654a8ab030', '670a8f85-36ea-9a0e-0726-66720daf6ae3',
        '973494a6-d1aa-c915-de3f-6788f2884232',
        10, 1);

insert into price_type (id, name, version, tenant_id)
values ('2809fea3-d2cd-3080-2a9c-4949eb6324c1', 'Закупочная', 1, '1');

insert into company (id, name, version, tenant_id)
values ('16211934-cb14-8dba-fb66-a3f8007ae0af', 'company name', 1, '1');

insert into client (id, external_id, name, debt, default_price_type_id, version, tenant_id)
values ('48f5c314-f5e2-06a1-8c9a-7ab03a823611', '48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'client name', 2.55,
        '2809fea3-d2cd-3080-2a9c-4949eb6324c1', 1, '1');

insert into client_contract (id, external_id, client_id, name, date, number, version)
values ('48f5c314-f5e2-06a1-8c9a-7ab03a823644', '48f5c314-f5e2-06a1-8c9a-7ab03a823644', '48f5c314-f5e2-06a1-8c9a-7ab03a823611', 'contract name',
        '2022-01-01 00:00:00', '123', 1);

update client
SET default_contract_id ='48f5c314-f5e2-06a1-8c9a-7ab03a823644'
where id = '48f5c314-f5e2-06a1-8c9a-7ab03a823611';


update product
SET product_unit_id = '32364ec1-a073-b750-12d9-b2c9cccb7830'
where id in ('93b35ec7-ce46-5444-ec49-a6e563dedc45', '973494a6-d1aa-c915-de3f-6788f2884232',
             '973494a6-d1aa-c915-de3f-6788f2884211');

insert into currency (id, name, version)
values ('d790d425-5081-5d67-9314-60abb572b79f', 'Тенге', 1);

insert into position_ (id, name, version, tenant_id)
values ('15a26fa7-7c52-d194-ca81-731273f30cc5', 'Торговый представитель', 1, 1);

insert into employee (id, position_id, first_name, last_name, middle_name, version, tenant_id, name)
values ('b834cf95-4083-269e-1a29-27946160769b', '15a26fa7-7c52-d194-ca81-731273f30cc5', 'Джон', 'Смитт', 'Иванов', 1, 1,
        'дарт вейдер темный рыцарь');

-- transfer
insert into transfer (id, number, date, document_state, document_type, version, company_id, storage_from_id,
                      storage_to_id,
                      user_id, tenant_id, currency_id)
values ('93b35ec7-ce46-5444-ec49-a6e563de1111', '1', '2022-01-01 00:00:00', 'APPLIED', 'TRANSFER', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', 'fc1f671f-876f-1163-6da1-d9ab14f649f3',
        '0934b00a-aecd-b0ef-8dfd-ac2f67937a1a', 'dbd0646a-e22f-5587-2758-dc44810e91b1', '1',
        'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de2222', '1', '2022-01-01 00:00:00', 'DRAFT', 'TRANSFER', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', 'fc1f671f-876f-1163-6da1-d9ab14f649f3',
        '0934b00a-aecd-b0ef-8dfd-ac2f67937a1a', 'dbd0646a-e22f-5587-2758-dc44810e91b1', '1',
        'd790d425-5081-5d67-9314-60abb572b79f');


insert into transfer_product (id, version, number, product_id, product_unit_id, amount, cost_price, transfer_id)
values ('8b0fb4c4-409c-5758-6db4-8374d534714b', 1, 1, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 1, 100,
        '93b35ec7-ce46-5444-ec49-a6e563de1111'),
       ('8b0fb4c4-409c-5758-6db4-8374d5342222', 1, 2, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 1, 100,
        '93b35ec7-ce46-5444-ec49-a6e563de2222');

-- receipt
insert into receipt (id, number, date, document_state, document_type, version, company_id, client_id,
                     client_contract_id, storage_id, user_id, tenant_id, currency_id)
values ('93b35ec7-ce46-5444-ec49-a6e563de1111', '1', '2022-01-01 00:00:00', 'APPLIED', 'GOODS_RECEIPT', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', 'fc1f671f-876f-1163-6da1-d9ab14f649f3',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de2222', '1', '2022-01-01 00:00:00', 'DRAFT', 'GOODS_RECEIPT', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', 'fc1f671f-876f-1163-6da1-d9ab14f649f3',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de3333', '1', '2022-01-01 00:00:00', 'APPLIED', 'GOODS_RECEIPT', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', '0934b00a-aecd-b0ef-8dfd-ac2f67937a1a',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de4444', '1', '2022-01-01 00:00:00', 'DRAFT', 'GOODS_RECEIPT', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', '0934b00a-aecd-b0ef-8dfd-ac2f67937a1a',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f');

insert into receipt_product (id, version, number, product_id, product_unit_id, amount, price, receipt_id)
values ('93b35ec7-ce46-5444-ec49-a6e563de1111', 1, 1, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 10, 100,
        '93b35ec7-ce46-5444-ec49-a6e563de1111'),
       ('973494a6-d1aa-c915-de3f-6788f2882222', 1, 2, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 10, 1000,
        '93b35ec7-ce46-5444-ec49-a6e563de2222'),
       ('93b35ec7-ce46-5444-ec49-a6e563de3333', 1, 3, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 10, 100,
        '93b35ec7-ce46-5444-ec49-a6e563de3333'),
       ('973494a6-d1aa-c915-de3f-6788f2884444', 1, 4, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 10, 1000,
        '93b35ec7-ce46-5444-ec49-a6e563de4444');

-- sale
insert into sale (id, number, date, document_state, document_type, version, company_id, client_id,
                  client_contract_id, storage_id, user_id, tenant_id, currency_id)
values ('93b35ec7-ce46-5444-ec49-a6e563de1111', '1', '2022-01-01 00:00:00', 'APPLIED', 'SALE', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', 'fc1f671f-876f-1163-6da1-d9ab14f649f3',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de2222', '1', '2022-01-01 00:00:00', 'DRAFT', 'SALE', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', 'fc1f671f-876f-1163-6da1-d9ab14f649f3',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de3333', '1', '2022-01-01 00:00:00', 'APPLIED', 'SALE', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', '0934b00a-aecd-b0ef-8dfd-ac2f67937a1a',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f'),
       ('93b35ec7-ce46-5444-ec49-a6e563de4444', '1', '2022-01-01 00:00:00', 'DRAFT', 'SALE', '1',
        '16211934-cb14-8dba-fb66-a3f8007ae0af', '48f5c314-f5e2-06a1-8c9a-7ab03a823611',
        '48f5c314-f5e2-06a1-8c9a-7ab03a823644', '0934b00a-aecd-b0ef-8dfd-ac2f67937a1a',
        'dbd0646a-e22f-5587-2758-dc44810e91b1', '1', 'd790d425-5081-5d67-9314-60abb572b79f');

insert into sale_product (id, version, number, product_id, product_unit_id, amount, price, sale_id)
values ('93b35ec7-ce46-5444-ec49-a6e563de1111', 1, 1, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 100, 100,
        '93b35ec7-ce46-5444-ec49-a6e563de1111'),
       ('973494a6-d1aa-c915-de3f-6788f2882222', 1, 2, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 100, 1000,
        '93b35ec7-ce46-5444-ec49-a6e563de2222'),
       ('93b35ec7-ce46-5444-ec49-a6e563de3333', 1, 3, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 100, 100,
        '93b35ec7-ce46-5444-ec49-a6e563de3333'),
       ('973494a6-d1aa-c915-de3f-6788f2884444', 1, 4, '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        '32364ec1-a073-b750-12d9-b2c9cccb7830', 100, 1000,
        '93b35ec7-ce46-5444-ec49-a6e563de4444');


insert into product_balance (id, product_id, storage_id, company_id, amount, version)
values ('0d35b143-607e-4768-ad43-f3bf3d445111', '93b35ec7-ce46-5444-ec49-a6e563dedc45',
        'fc1f671f-876f-1163-6da1-d9ab14f649f3', '16211934-cb14-8dba-fb66-a3f8007ae0af', 10, 1),
       ('0d35b143-607e-4768-ad43-f3bf3d445222', '973494a6-d1aa-c915-de3f-6788f2884232',
        'fc1f671f-876f-1163-6da1-d9ab14f649f3', '16211934-cb14-8dba-fb66-a3f8007ae0af', 100, 1);

insert into product_balance_change (id, "date", company_id, product_id, storage_id, amount)
values (gen_random_uuid(), '2022-01-01 00:00:00', '16211934-cb14-8dba-fb66-a3f8007ae0af',
        '93b35ec7-ce46-5444-ec49-a6e563dedc45', 'fc1f671f-876f-1163-6da1-d9ab14f649f3', -6),
        (gen_random_uuid(), '2022-01-01 00:00:00', '16211934-cb14-8dba-fb66-a3f8007ae0af',
        '93b35ec7-ce46-5444-ec49-a6e563dedc45', 'fc1f671f-876f-1163-6da1-d9ab14f649f3', -4),
        (gen_random_uuid(), '2022-01-01 00:00:00', '16211934-cb14-8dba-fb66-a3f8007ae0af',
        '973494a6-d1aa-c915-de3f-6788f2884232', 'fc1f671f-876f-1163-6da1-d9ab14f649f3', 30),
        (gen_random_uuid(), '2022-01-01 00:00:00', '16211934-cb14-8dba-fb66-a3f8007ae0af',
        '973494a6-d1aa-c915-de3f-6788f2884232', 'fc1f671f-876f-1163-6da1-d9ab14f649f3', 70);
