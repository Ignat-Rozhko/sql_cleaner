SET session_replication_role = replica;

INSERT INTO public.position_ (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                              last_modified_date, recycle_bin_id)
VALUES ('ce74a37e-2ea4-4409-a724-ae8747d89e9b', 'Кассир', 'example', 1, 'admin', '2022-02-22 22:22:22', NULL,
        '2022-02-22 22:22:22', null);

INSERT INTO public.employee (id, first_name, last_name, tenant_id, version, created_by, created_date, last_modified_by,
                             last_modified_date, recycle_bin_id, position_id, middle_name, name, code)
VALUES ('1acd6d20-e1d8-2aef-6e55-96d80e9983f8', 'Максим', 'Лыткина', 'example', 1, 'admin', '2023-02-03 09:41:26.735',
        NULL, '2023-02-03 09:41:26.735', null, 'ce74a37e-2ea4-4409-a724-ae8747d89e9b', 'Игорь',
        'Даниил Борисова Щукин', false);

INSERT INTO public.user_ (id, version, username, first_name, last_name, password, email, active, time_zone_id, tenant,
                          dtype)
VALUES ('3acee397-d78a-4f29-96f2-20ffde5c6e41', 1, 'example|admin', 'Exchange', 'Admin', NULL, NULL, true, NULL,
        'example', 'AccountUser');

insert into agent_setting (id, tenant_id, version, employee_id, can_create_partners,
                           is_check_gps, set_price_type_from_order, can_change_price,
                           add_article_to_product_name)
values ('f3197866-05e1-256a-fea4-9c688685a409', 'example', 1, 'bc5dab98-5c11-121b-8a7e-883893a34a85', false, false,
        false, false, false);

insert into agent_team (id, version, tenant_id, name)
values ('5c4b83ae-e574-11ed-b5ea-0242ac120002', 1, 'example', 'Dragons'),
       ('e361f34a-e575-11ed-b5ea-0242ac120002', 1, 'example', 'OUTSIDERS');

insert into advance_agent_settings (id, tenant_id, version, username, password)
values ('f3197866-05e1-256a-fea4-9c688685a409', 'example', 1, 'username', 'password');


INSERT INTO public.company (id, name, tenant_id, version, created_by, created_date, last_modified_by,
                            last_modified_date, recycle_bin_id, identification_number, legal_address,
                            real_address, email, contact_phone, beneficiary_code, vat_certificate_series,
                            vat_certificate_number, vat_certificate_date, storage_id, cashier_id, bank_account_id,
                            director_employee_id, accountant_general_employee_id)
VALUES ('2253584d-ecad-68f5-f3e1-81a7398877de', 'ОП СочиТоргСнабПром', 'example', 1, 'admin', '2023-02-03 09:41:27.356',
        NULL, '2023-02-03 09:41:27.356', null, '333031757072', '141217 Россия, Тверь, Зеленая пр., 394',
        '006847 Россия, Ярославль, Лермонтова ул., 985 кв. 240', 'magnam@yahoo.com', '2058936676', '14', '34803',
        '7152565', '2022-02-18 01:02:56.052', 'b93c5b9c-919b-44b7-4110-b3ac2e624e3e',
        '39835d35-3d3b-48ed-da90-0cac335e75b1', '81ebc01d-b918-474b-534e-3fd309b9e23f',
        'bc5dab98-5c11-121b-8a7e-883893a34a85', 'bc5dab98-5c11-121b-8a7e-883893a34a85');

INSERT INTO public.mten_tenant (id, version, create_ts, created_by, update_ts, updated_by, delete_ts, deleted_by,
                                tenant_id,
                                name, base_currency_id, external_id, dtype)
VALUES ('e9f588aa-ab3b-b08b-d5e7-010b1fd19f42', 2, '2023-02-03 09:40:26.953', 'admin', '2023-02-03 09:40:27.868',
        'admin', NULL, NULL, 'example', 'example', 'cb31ee1d-62ae-41fd-a751-2f0fec3d7308', NULL, 'Account');

INSERT INTO public.sec_role_assignment(id, version, create_ts, created_by, update_ts, updated_by, delete_ts, deleted_by,
                                       username, role_code, role_type)
VALUES ('6c9e420a-2b7a-4c42-8654-a9027ee14083', 1, NULL, NULL, NULL, NULL, NULL, NULL, 'admin', 'system-full-access',
        'resource'),
       ('61a4f5dd-308a-4d75-983d-d6d007a9227c', 1, '2022-08-09 03:33:28.334', 'admin', NULL, NULL, NULL, NULL,
        'example|admin', 'account-admin', 'resource');

insert into plan_fact (id, plan_sum_month, plan_sum_day, plan_type, version, agent_id)
values ('f0ee4934-d8dc-187f-393f-19bf86595904', 20000, 12000, 'noplan', 1,
        '1acd6d20-e1d8-2aef-6e55-96d80e9983f8');

SET session_replication_role = default;
