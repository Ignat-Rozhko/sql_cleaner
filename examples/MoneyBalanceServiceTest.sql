SET
    session_replication_role = replica;

INSERT INTO public.company (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                            last_modified_date, recycle_bin_id, identification_number, legal_address,
                            real_address, email, contact_phone, beneficiary_code, vat_certificate_series,
                            vat_certificate_number, vat_certificate_date, storage_id, cashier_id, bank_account_id,
                            director_employee_id, accountant_general_employee_id)
VALUES ('9cd7e09e-5e83-9f6e-98a9-fa34cdd2c43d', 'ОП СбытТоргПром', 'example', 1, 'admin', '2023-02-17 07:56:02.736',
        NULL, '2023-02-17 07:56:02.736', null, '670445507464', '838614 Россия, Тверь, Береговая ул., 087 кв. 310',
        '963804 Россия, Сочи, Рабочая проспект, 181', 'est@ya.ru', '3827986090', '19', '36802', '4028595',
        '2022-04-19 09:11:31.859', 'd89e124d-f664-b998-f10a-81d945ea169f', 'c9588391-b25c-090d-fb4b-58248c5b0793',
        'ce4ab898-4a59-3e38-d42a-fbfbd903abb8', '866d0644-ec3f-4157-4e09-beff5880dfef',
        '866d0644-ec3f-4157-4e09-beff5880dfef');

INSERT INTO public.bank_account(id, name, tenant_id, bank_id, currency_id, account_number, version)
VALUES ('b93ccdb9-716c-45bd-905e-051625f66b13', 'Счёт', 'example', 'a1a1a1a1-716c-45bd-905e-051625f66b13',
        '1de22493-3f2a-4417-8eb7-9abb39f28d86', 'aa12345676889', 1);

INSERT INTO public.bank_account (id, name, tenant_id, bank_id, currency_id, account_number, version)
VALUES ('d675b819-9ea8-d7bd-a4a6-5b25e84cdd75', 'Счёт', 'example', 'a1a1a1a1-716c-45bd-905e-051625f66b13',
        '1de22493-3f2a-4417-8eb7-9abb39f28d86', 'aa12345676889', 1);

INSERT INTO public.cash_flow_items (id, version, created_by, created_date, last_modified_by, last_modified_date,
                                    recycle_bin_id, tenant_id, code, name)
VALUES ('b93ccdb9-716c-45bd-905e-051625f55a01', 2, '1', '2022-10-29 21:51:20.312', '1', '2022-10-29 21:51:42.475', null, 'example', 7, '0000001');

INSERT INTO public.currency (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                             last_modified_date, recycle_bin_id, letter_code, digital_code)
VALUES ('1de22493-3f2a-4417-8eb7-9abb39f28d86', 'Тенге', 'example', 1, 'admin', '2022-02-22 22:22:22', NULL,
        '2022-02-22 22:22:22', null, 'KZT', '398');

INSERT INTO public.cashier (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                            last_modified_date, recycle_bin_id, company_id, currency_id, note)
VALUES ('c9588391-b25c-090d-fb4b-58248c5b0793', 'Aliquid', 'example', 1, 'admin', '2023-02-17 07:56:02.738', NULL,
        '2023-02-17 07:56:02.738', null, '9cd7e09e-5e83-9f6e-98a9-fa34cdd2c43d',
        '1de22493-3f2a-4417-8eb7-9abb39f28d86',
        'I''m the dude, so that''s what you call me. That or, uh His Dudeness, or uh Duder, or El Duderino, if you''re not into the whole brevity thing.');



INSERT INTO public.user_ (id, version, username, first_name, last_name, password, email, active, time_zone_id, tenant,
                          dtype)
VALUES ('8928b74a-80cb-402c-ab3c-27d5b8f16a2e', 1, 'example|admin', 'Exchange', 'Admin', NULL, NULL, true, NULL,
        'example', 'AccountUser');

INSERT INTO public.cash_order (id, number, date, document_state, document_type, user_id, currency_id, tenant_id,
                               version, created_by, created_date, last_modified_by, last_modified_date,
                               recycle_bin_id, company_id, cash_flow_item_id, reason, sum, cashier_id, operation_type,
                               employee_id, bank_account_id, note, document_source_id)
VALUES ('40774e02-e6c8-404d-d7f6-af8ebfe022ef', '1', '2022-03-09 04:12:24.842', 'APPLIED', 'CASH_ORDER',
        '8928b74a-80cb-402c-ab3c-27d5b8f16a2e', '1de22493-3f2a-4417-8eb7-9abb39f28d86', 'example', 1, 'admin',
        '2023-02-17 07:56:13.234', NULL, '2023-02-17 07:56:13.234', null, '9cd7e09e-5e83-9f6e-98a9-fa34cdd2c43d',
        'b93ccdb9-716c-45bd-905e-051625f55a01', NULL, 58.00, 'c9588391-b25c-090d-fb4b-58248c5b0793',
        'PAYMENT_TO_THE_SUPPLIER', NULL, 'b93ccdb9-716c-45bd-905e-051625f66b13',
        'That rug really tied the room together.', NULL);

INSERT INTO public.cash_receipt_order (id, number, date, document_state, document_type, user_id, currency_id, tenant_id,
                                       version, created_by, created_date, last_modified_by, last_modified_date,
                                       recycle_bin_id, company_id, cashier_id, transaction_type, employee_id,
                                       bank_account_id, sum_, note, cash_flow_item_id, reason, document_source_id)
VALUES ('d3e68b68-1fcb-5c78-7210-046242333415', '1', '2022-02-26 01:13:44.051', 'APPLIED', 'CASH_RECEIPT_ORDER',
        '8928b74a-80cb-402c-ab3c-27d5b8f16a2e', '1de22493-3f2a-4417-8eb7-9abb39f28d86', 'example', 1, 'admin',
        '2023-02-17 07:56:13.529', NULL, '2023-02-17 07:56:13.529', null, '9cd7e09e-5e83-9f6e-98a9-fa34cdd2c43d',
        'c9588391-b25c-090d-fb4b-58248c5b0793', 'CLIENT_PAYMENT', NULL, 'b93ccdb9-716c-45bd-905e-051625f66b13', 78.00,
        'Mr. Treehorn treats objects like women, man.', 'b93ccdb9-716c-45bd-905e-051625f55a01', 'I am the walrus',
        NULL);

INSERT INTO public.client (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date,
                           recycle_bin_id, phone, debt, legal_address, real_address, email, contact_person,
                           contact_phone, beneficiary_code, vat_certificate_series, vat_certificate_number,
                           vat_certificate_date, default_price_type_id, default_contract_id, default_outlet_id,
                           default_agreements_id, bank_account_id, bin_pin, is_directory, parent_id, code)
VALUES ('61948b4e-f0e0-4d88-e4b8-284afa2a6ef3', 'НКО НовосибирскТоргСнабТрейд', 'example', 1, 'admin',
        '2023-02-17 07:56:09.911', NULL, '2023-02-17 07:56:09.911', null, '3844024968', 0,
        '104538 Россия, Новокузнецк, Пролетарская ул., 806',
        '671836 Россия, Ростов-на-Дону, Солнечная проспект, 859 кв. 721', 'sunt@mail.ru', 'Мария Мишин Козлов',
        '6568463657', '23', '92339', '9824839', '2022-05-17 03:28:55.658', '3bf3c247-dd43-44f5-9d89-aaeed5982453',
        '4c15ee8e-d932-3745-89f6-4f610100b048', 'ebdad24c-b35f-0808-3cf0-4e7d4a75500f',
        '534a2dd1-415d-8655-7df4-64dfe6f2f766', 'ad4be07c-9b23-9cc3-1cd2-d5666609e6ac', '169854105454', false, null,
        '001'),
       ('fa514bd7-3122-cb24-5d8d-5dafb935f005', 'ООО Илья', 'example', 1, 'admin', '2023-02-17 07:56:11.463', NULL,
        '2023-02-17 07:56:11.463', null, '3808178635', 0, '001874 Россия, Саратов, площадь Энергетиков, 056',
        '312104 Россия, Тольятти, пл. Северная, 438 кв. 096', 'autem@yahoo.com', 'Нина Осипов Носова', '7217091412',
        '16', '67249', '2136065', '2022-04-16 19:36:34.785', '3bf3c247-dd43-44f5-9d89-aaeed5982453',
        '7a5acd3a-f3f2-5c8d-efb5-c4c46239111c', '319ed023-4516-e443-5ba5-d1f697b3904f',
        'fdf6d8de-7182-198b-c613-d055c966f910', '060a4372-19e9-7494-209a-5312638be76b', '168473054544', false, null,
        '002');

INSERT INTO public.client_contract (id, version, created_by, created_date, last_modified_by, last_modified_date,
                                    recycle_bin_id, client_id, name, number, date, end_date, debt)
VALUES ('4c15ee8e-d932-3745-89f6-4f610100b048', 1, 'admin', '2023-02-17 07:56:09.911', NULL, '2023-02-17 07:56:09.911',
        null, '61948b4e-f0e0-4d88-e4b8-284afa2a6ef3', 'ЗАО Алёна', NULL, '2022-06-06 15:10:56.695',
        '2022-10-29 20:39:50.648', 0),
       ('27ff9db3-60c9-2037-16b7-f398ea8a4104', 1, 'admin', '2023-02-17 07:56:09.912', NULL, '2023-02-17 07:56:09.912',
        null, '61948b4e-f0e0-4d88-e4b8-284afa2a6ef3', 'ЗАО АстраханьТорг', NULL, '2022-05-03 21:33:51.82',
        '2022-11-02 12:56:55.461', 0),
       ('7a5acd3a-f3f2-5c8d-efb5-c4c46239111c', 1, 'admin', '2023-02-17 07:56:11.463', NULL, '2023-02-17 07:56:11.463',
        null, 'fa514bd7-3122-cb24-5d8d-5dafb935f005', 'ОАО УльяновскТорг', NULL, '2023-01-11 21:27:46.33',
        '2023-01-29 09:18:09.063', 0),
       ('0f4487b7-19e3-9a3d-4e34-82f7f01c6ddc', 1, 'admin', '2023-02-17 07:56:11.464', NULL, '2023-02-17 07:56:11.464',
        null, 'fa514bd7-3122-cb24-5d8d-5dafb935f005', 'ОАО ТоргТоргСнаб', NULL, '2022-03-08 09:32:40.61',
        '2023-01-06 22:27:24.432', 0);

INSERT INTO public.cash_receipt_order_client_contract (id, sum_, client_id, client_contract_id, cash_receipt_order_id,
                                                       number, version)
VALUES ('a14f0c0c-aee1-aac9-aab7-069fcd9ea8e3', 78.00, '61948b4e-f0e0-4d88-e4b8-284afa2a6ef3',
        '27ff9db3-60c9-2037-16b7-f398ea8a4104', 'd3e68b68-1fcb-5c78-7210-046242333415', 1, 1);

INSERT INTO public.mten_tenant (id, version, create_ts, created_by, update_ts, updated_by, delete_ts, deleted_by,
                                tenant_id,
                                name, base_currency_id, external_id, dtype)
VALUES ('ea5f7a4f-8dd0-c44b-36be-b461723f6f3d', 2, '2023-02-17 07:55:07.302', 'admin', '2023-02-17 07:55:08.137',
        'admin', NULL, NULL, 'example', 'example', '1de22493-3f2a-4417-8eb7-9abb39f28d86', NULL, 'Account');

INSERT INTO public.supplier_payment (id, client_id, client_contract_id, sum_, cash_order_id, number, version)
VALUES ('d0d5fd44-dd73-32b2-5acc-22e8a99f5b3b', 'fa514bd7-3122-cb24-5d8d-5dafb935f005',
        '0f4487b7-19e3-9a3d-4e34-82f7f01c6ddc', 58.00, '40774e02-e6c8-404d-d7f6-af8ebfe022ef', 1, 1);


INSERT INTO public.non_cash_receipt (id, sum_, date, number, beneficiary_account_id, sender_account_id,
                                     cash_flow_item_id,
                                     cashier_id, client_id, company_id, created_by, created_date, currency_id,
                                     recycle_bin_id, document_state, document_type,
                                     note,
                                     tenant_id, transaction_type, user_id, version, document_source_id)
VALUES ('8942698b-71b1-d0c2-a1d7-1131b9dc7c40', 78.00, '2022-02-26 13:11:56.203000', '000000000000001',
        'd675b819-9ea8-d7bd-a4a6-5b25e84cdd75', 'b93ccdb9-716c-45bd-905e-051625f66b13',
        'b93ccdb9-716c-45bd-905e-051625f55a01', 'c9588391-b25c-090d-fb4b-58248c5b0793',
        '61948b4e-f0e0-4d88-e4b8-284afa2a6ef3', '9cd7e09e-5e83-9f6e-98a9-fa34cdd2c43d', 'evgen',
        '2023-02-23 13:11:56.203000', '1de22493-3f2a-4417-8eb7-9abb39f28d86', null, 'APPLIED', 'NON_CASH_RECEIPT',
        null, 'example', 'CASH_INCOME', '8928b74a-80cb-402c-ab3c-27d5b8f16a2e', 2,
        null);

INSERT INTO public.non_cash_funds_expense (id, number, date, document_state, document_type, user_id, currency_id,
                                           tenant_id, version, created_by, created_date, last_modified_by,
                                           last_modified_date, recycle_bin_id, company_id,
                                           beneficiary_account_id, client_id, sender_account_id, transaction_type,
                                           cashier_id, sum_, note, cash_flow_item_id, document_source_id)
VALUES ('fa201d16-2380-00f7-45bc-280195b330c3', '000000000000001', '2022-03-09 13:10:28.923000', 'APPLIED',
        'NON_CASH_FUNDS_EXPENSE', '8928b74a-80cb-402c-ab3c-27d5b8f16a2e', '1de22493-3f2a-4417-8eb7-9abb39f28d86',
        'example',
        2, 'evgen', '2023-02-23 13:10:28.923000', 'evgen', '2023-02-23 13:10:36.685000', null,
        '9cd7e09e-5e83-9f6e-98a9-fa34cdd2c43d', 'b93ccdb9-716c-45bd-905e-051625f66b13',
        '61948b4e-f0e0-4d88-e4b8-284afa2a6ef3', 'd675b819-9ea8-d7bd-a4a6-5b25e84cdd75', 'CASH_INCOME',
        'c9588391-b25c-090d-fb4b-58248c5b0793', 56.00, null, 'b93ccdb9-716c-45bd-905e-051625f55a01', null);



SET
    session_replication_role = default;