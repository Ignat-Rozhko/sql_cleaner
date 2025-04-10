SELECT JSONB_BUILD_OBJECT(
               'type', 'AgentResponse',
               'agentId', agent.external_id,
               'licenseId', l.id,
               'organizationId', com.external_id,
               'firstName', agent.first_name,
               'lastName', agent.last_name,
               'middleName', agent.middle_name,
               'organization', com.name,
               'currency', c.letter_code,
               'mainPlanType', setting.plan_type,
               'mainStorage', JSONB_BUILD_OBJECT(
                       'type', 'StorageResponse',
                       'storageId', s.external_id,
                       'storageName', s.name
                              ),
               'mainCashBox', JSONB_BUILD_OBJECT(
                       'type', 'CashBoxResponse',
                       'cashBoxId', cb.external_id,
                       'name', cb.name
                              ),
               'mainPriceType', JSONB_BUILD_OBJECT(
                       'type', 'PriceTypeResponse',
                       'priceTypeId', pt.external_id,
                       'name', pt.name
                                ),
               'checkGPS', setting.is_check_gps,
               'hardRoute', setting.is_hard_route,
               'changePrice', setting.can_change_price,
               'useAgreements', setting.use_agreements,
               'checkOutletGPS', setting.check_outlet_gps,
               'canCreatePartner', setting.can_create_partners,
               'radiusGPS', setting.radius_gps,
               'defaultDeliveryDate', setting.default_delivery_date,
               'hasAutoExchange', setting.has_auto_exchange,
               'autoExchangePeriod', setting.auto_exchange_period,
               'workDayStartTime', setting.work_start_time,
               'workDayEndTime', setting.work_end_time
       )
FROM license l
         LEFT JOIN employee agent ON l.agent_uuid = agent.id AND agent.recycle_bin_id IS NULL
         LEFT JOIN company com ON l.company_id = com.id AND agent.recycle_bin_id IS NULL
         LEFT JOIN agent_setting setting ON agent.id = setting.employee_id AND setting.recycle_bin_id IS NULL
         LEFT JOIN currency c ON c.id = setting.currency_id AND c.recycle_bin_id IS NULL
         LEFT JOIN storage s ON setting.main_storage_id = s.id AND s.recycle_bin_id IS NULL
         LEFT JOIN cashier cb ON setting.main_cashier_id = cb.id AND cb.recycle_bin_id IS NULL
         LEFT JOIN price_type pt ON setting.main_price_type_id = pt.id AND pt.recycle_bin_id IS NULL
WHERE agent.id = :agentId
  AND ((agent.last_modified_date > :date OR agent.created_date > :date)
    OR (l.last_modified_date > :date OR l.created_date > :date)
    OR (setting.last_modified_date > :date OR setting.created_date > :date))
GROUP BY l.id, agent.external_id, agent.first_name, agent.last_name, agent.middle_name, s.external_id, s.name, cb.external_id, cb.name, pt.id, com.external_id,
         setting.id, c.id, com.name
ORDER BY l.id;