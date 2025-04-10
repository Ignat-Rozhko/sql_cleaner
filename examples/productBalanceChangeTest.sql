INSERT INTO public.product (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id, parent_id, is_directory, type_, product_unit_id, article_number, code)
VALUES ('94101cd0-5952-d3a7-0bef-138314c1fbd8', 'сыр', '00', 2, '01', '2023-03-08 14:50:41.131000', '01', '2023-03-08 15:12:59.972000', null, null, false, 'PRODUCT', null, null, 2),
       ('5230feef-00c0-efda-083e-35fca78f599a', 'молоко', '00', 3, '01', '2023-03-08 14:49:08.700000', '01', '2023-03-08 15:12:49.428000', null, null, false, 'PRODUCT', null, null, 1);

INSERT INTO public.storage (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id)
VALUES ('a3f96013-5203-5222-6b51-59afc423f9e5', 'Sunt ipsum nesciunt', '00', 1, 'admin', '2023-03-08 14:43:58.078000', null, '2023-03-08 14:43:58.078000', null),
       ('9612473b-ba30-6e45-81a2-db376cc601b2', 'Quia molestiae vel', '00', 1, 'admin', '2023-03-08 14:43:58.127000', null, '2023-03-08 14:43:58.127000', null),
       ('9967ff6a-0a18-e31d-1bd8-ab3705f2fd2c', 'In atque qui', '00', 1, 'admin', '2023-03-08 14:47:54.357000', null, '2023-03-08 14:47:54.357000', null),
       ('f831669b-5b81-3294-013c-3b5f07cf5bcf', 'скад1', '00', 2, 'admin', '2023-03-08 14:47:54.373000', '01', '2023-03-08 15:15:50.008000', null);

INSERT INTO public.receipt (id, number, date, document_state, document_type, user_id, currency_id, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id, company_id, client_id, client_contract_id, storage_id, sum_, vat_sum, note, price_type_id)
VALUES ('b398e367-47b0-5971-51ed-2d071573e698', '1', '2023-03-08 15:16:29.008000', 'APPLIED', 'GOODS_RECEIPT', null, null, '00', 1, '01', '2023-03-08 15:16:29.626000', null, '2023-03-08 15:16:29.626000', null, null, null, null, 'f831669b-5b81-3294-013c-3b5f07cf5bcf', 13400.00, 1307.14, null, null);

INSERT INTO public.sale (id, number, date, document_state, document_type, user_id, currency_id, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id, company_id, client_id, client_contract_id, storage_id, employee_id, sum_, vat_sum, note, price_type_id, mobile_order_id)
VALUES ('0714d58c-490c-60d3-1990-10b1d484d04e', '1', '2023-03-09 16:36:31.554000', 'APPLIED', 'SALE', null, null, '00', 1, '01', '2023-03-09 16:36:32.067000', null, '2023-03-09 16:36:32.067000', null, null, null, null, 'f831669b-5b81-3294-013c-3b5f07cf5bcf', null, 50.00, 5.36, null, null, null);

insert into "public".company (id, name, tenant_id, version)
values ('c0001111-0000-0000-0000-111122223333', 'company', '00', 1);

INSERT INTO public.product_balance_change (id, date, company_id, storage_id, product_id, amount, receipt_id, sale_id, surplus_id, transfer_id, write_off_id, return_to_supplier_id, return_from_customer_id)
VALUES ('cce7ef7c-b0de-64d8-3e84-5ed9e569facf', '2023-03-08 15:17:59.250000', 'c0001111-0000-0000-0000-111122223333', 'f831669b-5b81-3294-013c-3b5f07cf5bcf', '94101cd0-5952-d3a7-0bef-138314c1fbd8', 10.000, 'b398e367-47b0-5971-51ed-2d071573e698', null, null, null, null, null, null),
       ('f9107f51-5255-867b-4422-e9f3c58e69f0', '2023-03-09 16:36:31.554000', 'c0001111-0000-0000-0000-111122223333', 'f831669b-5b81-3294-013c-3b5f07cf5bcf', '5230feef-00c0-efda-083e-35fca78f599a', -5.000, null, '0714d58c-490c-60d3-1990-10b1d484d04e', null, null, null, null, null);
