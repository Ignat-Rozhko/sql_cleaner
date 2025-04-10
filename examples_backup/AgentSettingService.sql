insert into mten_tenant (id, name, external_id, version, tenant_id, dtype)
values ('e7422469-324a-49a5-b798-dac05a0d1242', 'account1', 123, 1, 1, 'Account');

insert into position_ (id, name, tenant_id, version)
values ('04e4ad01-6565-48f4-8f2e-bd2fc7475e5b', 'Торговый представитель', 1, 1);

insert into employee (id, first_name, last_name, tenant_id, version, position_id, middle_name, name)
values ('132fb65c-14fb-38cc-557b-847c88867ed7', 'Петр', 'Петров', 1, 1, '04e4ad01-6565-48f4-8f2e-bd2fc7475e5b', 'Петрович', 'Петров Петр Петрович');

insert into employee (id, first_name, last_name, tenant_id, version, position_id, middle_name, name)
values ('ce1f38ba-4698-8d52-e1dc-f1e9813afdbe', 'Иван', 'Иванов', 1, 1, '04e4ad01-6565-48f4-8f2e-bd2fc7475e5b', 'Иванович', 'Иванов Иван Иванович');

insert into agent_setting (id, tenant_id, version, employee_id, can_create_partners, is_check_gps, set_price_type_from_order, can_change_price, add_article_to_product_name)
values ('4606001e-53be-bf72-7558-55b6499a2e07', 1, 1, '132fb65c-14fb-38cc-557b-847c88867ed7', false, false, false, false, false);
