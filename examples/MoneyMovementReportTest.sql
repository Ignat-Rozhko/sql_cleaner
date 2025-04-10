SET
session_replication_role = replica;

INSERT INTO public.bank (id, name, tenant_id, version, created_by, created_date, last_modified_by, last_modified_date,
                         recycle_bin_id, bic)
VALUES ('7b271f7a-516c-da50-7832-83a0a6fe8527', 'банк1', '01', 1, 'evg', '2023-03-22 13:31:33.498000', null,
        '2023-03-22 13:31:33.498000', null, '11111111');

INSERT INTO public.bank_account (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                                 last_modified_date, recycle_bin_id, currency_id, account_number, bank_id,
                                 company_id, client_id)
VALUES ('c901742f-c256-440f-ca1c-e18a8bc54d70', 'счет1', '01', 1, 'evg', '2023-03-22 13:33:04.767000', null,
        '2023-03-22 13:33:04.767000', null, '7f04c215-4f0b-4725-9bea-ece89bb77e27', '11111111111111111111',
        '7b271f7a-516c-da50-7832-83a0a6fe8527', 'd87534ab-d610-2697-083d-ef9d59ac29f6', null);

INSERT INTO public.currency (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                             last_modified_date, recycle_bin_id, letter_code, digital_code)
VALUES ('7f04c215-4f0b-4725-9bea-ece89bb77e27', 'Тенге', '01', 1, 'admin', '2022-02-22 22:22:22.000000', null,
        '2022-02-22 22:22:22.000000', null, 'KZT', '398');

INSERT INTO public.company (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                            last_modified_date, recycle_bin_id, identification_number, legal_address,
                            real_address, email, contact_phone, beneficiary_code, vat_certificate_series,
                            vat_certificate_number, vat_certificate_date, storage_id, cashier_id, bank_account_id,
                            director_employee_id, accountant_general_employee_id)
VALUES ('d87534ab-d610-2697-083d-ef9d59ac29f6', 'CompanyOne', '01', 1, 'admin', '2023-03-07 10:28:14.399000',
        null, '2023-03-07 10:28:14.399000', null, '625477923723',
        '944938 Россия, Хабаровск, площадь Первомайская, 623', '000608 Россия, Владивосток, Полевая пл., 414',
        'cumque@gmail.com', '1582466315', '12', '68316', '9908274', '2022-06-20 09:02:13.788000',
        '7f62481a-4bf8-2349-0105-7208bf970661', 'c20c7d0c-4216-e8ad-2a8d-08c2cbab2997',
        'c901742f-c256-440f-ca1c-e18a8bc54d70', 'ba5ce5ee-111e-2e5b-acc5-67543d21f6bb',
        null);

INSERT INTO public.cash_flow_items (id, version, created_by, created_date, last_modified_by, last_modified_date,
                                    recycle_bin_id, tenant_id, code, name)
VALUES ('8ab6b632-205b-45f8-a6ce-806aa6dadac0', 2, '1', '2022-10-29 21:51:20.312000', '1', '2022-10-29 21:51:42.475000',
        null, '01', 3, 'GiveMoneyToMan'),
       ('a9cf0dfc-012b-4a34-8964-f2ffa9e51336', 2, '1', '2022-10-29 21:51:20.312000', '1', '2022-10-29 21:51:42.475000',
        null, '01', 10, 'PayAtOil');

INSERT INTO public.cashier (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                            last_modified_date, recycle_bin_id, company_id, currency_id, note)
VALUES ('c20c7d0c-4216-e8ad-2a8d-08c2cbab2997', 'Et et velit', '01', 1, 'admin', '2023-03-07 10:28:14.399000', null,
        '2023-03-07 10:28:14.399000', null, 'd87534ab-d610-2697-083d-ef9d59ac29f6',
        'bbda7495-09f6-4c17-8139-22faa2242956', 'I am the walrus');

INSERT INTO public.cash_receipt_order (id, number, date, document_state, document_type, user_id, currency_id, tenant_id,
                                       version, created_by, created_date, last_modified_by, last_modified_date,
                                       recycle_bin_id, company_id, cashier_id, transaction_type, employee_id,
                                       bank_account_id, sum_, note, cash_flow_item_id, reason, document_source_id,
                                       client_id)
VALUES ('0603d3cd-39b5-66f3-44b9-1f39df8cc773', null, '2022-07-31 19:26:04.193000', 'APPLIED', 'CASH_RECEIPT_ORDER',
        '4ad5cd15-1d79-4748-a12c-434ac73d134c', 'bbda7495-09f6-4c17-8139-22faa2242956', '01', 4, 'admin',
        '2023-03-07 10:31:58.881000', 'ev', '2023-03-07 22:13:10.274000', null,
        'd87534ab-d610-2697-083d-ef9d59ac29f6', 'c20c7d0c-4216-e8ad-2a8d-08c2cbab2997', 'CLIENT_PAYMENT', null, null,
        67.00, 'This aggression will not stand, man.', '8ab6b632-205b-45f8-a6ce-806aa6dadac0', 'Оплата от покупателя',
        null, null);

INSERT INTO public.cash_order (id, number, date, document_state, document_type, user_id, currency_id, tenant_id,
                               version, created_by, created_date, last_modified_by, last_modified_date, recycle_bin_id, company_id, cash_flow_item_id, reason, sum, cashier_id, operation_type,
                               employee_id, bank_account_id, note, document_source_id, client_id)
VALUES ('09efe515-63b5-897b-ba25-1431379ce120', null, '2022-12-24 07:48:46.624000', 'APPLIED', 'CASH_ORDER',
        '4ad5cd15-1d79-4748-a12c-434ac73d134c', 'bbda7495-09f6-4c17-8139-22faa2242956', '01', 3, 'admin',
        '2023-03-07 10:31:58.676000', 'ev', '2023-03-07 22:20:16.711000', null,
        'd87534ab-d610-2697-083d-ef9d59ac29f6', '6c62aaec-83ee-45aa-8eeb-1c19366c55c4', 'Оплата поставщику', 28.00,
        '35e823da-bd57-3a92-827b-dbd8bc8ee01a', 'PAYMENT_TO_THE_SUPPLIER', null, null,
        'So then you have no frame of reference here Donny. You''re like a child who wonders into the middle of a movie.',
        null, null),
       ('09efe515-63b5-897b-ba25-1431379ce121', null, '2022-12-24 07:48:46.624000', 'APPLIED', 'CASH_ORDER',
        '4ad5cd15-1d79-4748-a12c-434ac73d134c', 'bbda7495-09f6-4c17-8139-22faa2242956', '1', 3, 'admin',
        '2023-03-07 10:31:58.676000', 'ev', '2023-03-07 22:20:16.711000', null,
        'd87534ab-d610-2697-083d-ef9d59ac29f6', '6c62aaec-83ee-45aa-8eeb-1c19366c55c4', 'Оплата поставщику', 28.00,
        '35e823da-bd57-3a92-827b-dbd8bc8ee01a', 'PAYMENT_TO_THE_SUPPLIER', null, null,
        'So then you have no frame of reference here Donny. You''re like a child who wonders into the middle of a movie.',
        null, null);


INSERT INTO public.non_cash_receipt (id, sum_, date, number, beneficiary_account_id, sender_account_id,
                                     cash_flow_item_id, cashier_id, client_id, company_id, created_by, created_date,
                                     currency_id, recycle_bin_id, document_state, document_type,
                                     last_modified_by, last_modified_date, note, tenant_id, transaction_type, user_id,
                                     version, document_source_id)
VALUES ('7fa391be-0519-50cd-fa96-552b8f51bdbd', 31.00, '2022-08-15 14:10:33.471000', null,
        'df569567-072e-0a98-2284-49f960e5f34f', 'b9c43948-759d-9a6e-3cef-8a50d0a5836a',
        'f0459a73-dd76-431f-82b6-7d04e2d71338', null, '9c622b84-7708-d732-76e9-e17c951c6119',
        'd87534ab-d610-2697-083d-ef9d59ac29f6', 'admin', '2023-03-07 10:29:26.539000',
        'bbda7495-09f6-4c17-8139-22faa2242956', null, 'APPLIED', 'NON_CASH_RECEIPT', null,
        '2023-03-07 10:29:26.539000', 'Mark it zero!', '01', 'CLIENT_PAYMENT', '4ad5cd15-1d79-4748-a12c-434ac73d134c', 1,
        null);


INSERT INTO public.non_cash_funds_expense (id, number, date, document_state, document_type, user_id, currency_id,
                                           tenant_id, version, created_by, created_date, last_modified_by,
                                           last_modified_date, recycle_bin_id, company_id,
                                           beneficiary_account_id, client_id, sender_account_id, transaction_type,
                                           cashier_id, sum_, note, cash_flow_item_id, document_source_id)
VALUES ('f6d74760-0fb7-3903-f720-4a9e7108c016', null, '2022-03-16 21:45:58.106000', 'APPLIED', 'NON_CASH_FUNDS_EXPENSE',
        '4ad5cd15-1d79-4748-a12c-434ac73d134c', 'bbda7495-09f6-4c17-8139-22faa2242956', '01', 1, 'admin',
        '2023-03-07 10:29:26.973000', null, '2023-03-07 10:29:26.973000', null,
        'd87534ab-d610-2697-083d-ef9d59ac29f6', 'b9c43948-759d-9a6e-3cef-8a50d0a5836a',
        '9c622b84-7708-d732-76e9-e17c951c6119', 'df569567-072e-0a98-2284-49f960e5f34f', 'SUPPLIER_PAYMENT', null, 93.00,
        'This is a very complicated case Maude. You know, a lotta ins, a lotta outs, lotta what-have-yous.',
        '9dec6681-a178-42b6-b96f-48a0c2af2818', null);


INSERT INTO public.cash_balance_change (id, date, sum_, company_id, client_id, cash_flow_item_id, cashier_id,
                                        cash_receipt_order_id, cash_order_id, currency_id, dtype)
VALUES ('7f804cdf-715e-0dd6-4d93-f76b1cb66e53', '2022-07-31 19:26:04.193000', 67.00,
        'd87534ab-d610-2697-083d-ef9d59ac29f6', null, '8ab6b632-205b-45f8-a6ce-806aa6dadac0',
        'c20c7d0c-4216-e8ad-2a8d-08c2cbab2997', '0603d3cd-39b5-66f3-44b9-1f39df8cc773',
        '09efe515-63b5-897b-ba25-1431379ce120',
        '7f04c215-4f0b-4725-9bea-ece89bb77e27', 'RECEIPT');

INSERT INTO public.non_cash_balance_change (id, date, sum_, company_id, client_id, cash_flow_item_id, bank_account_id,
                                            non_cash_receipt_id, non_cash_funds_expense_id, currency_id, dtype)
VALUES ('18abb334-ddc1-201c-c4e4-86efa7c3b3b4', '2022-08-15 14:10:33.471000', 31.00,
        'd87534ab-d610-2697-083d-ef9d59ac29f6', '9c622b84-7708-d732-76e9-e17c951c6119',
        '8ab6b632-205b-45f8-a6ce-806aa6dadac0', 'c901742f-c256-440f-ca1c-e18a8bc54d70',
        '7fa391be-0519-50cd-fa96-552b8f51bdbd', 'f6d74760-0fb7-3903-f720-4a9e7108c016',
        '7f04c215-4f0b-4725-9bea-ece89bb77e27', 'RECEIPT');

SET
session_replication_role = default;
