import json
import os
from baseintegration.datamigration import logger
from baseintegration.integration import Integration


class PurchaseToWorkCenterMap:

    def __init__(self, **kwargs):
        self.work_centers = kwargs.get('work_centers')
        self.search = kwargs.get('search')


class M2MConfiguration:
    purchase_work_center_maps = []
    excluded_operations = []
    expedite_part_number = None
    default_erp_code = None
    create_m2m_accounts = False
    default_country_alpha_3 = 'USA'
    enable_part_consolidation = True
    purchase_condition = None
    material_condition = None
    purchase_use_total_cost = False
    material_use_total_cost = False
    material_add_group_code = False
    material_add_product_class = False
    export_as_quote = False
    add_standard_parts_as_quote_items = False
    material_resync_enabled = False
    material_item_mater_number_costing_variable = 'Item Master Number'
    material_unit_of_measure_costing_variable = 'Unit of Measure'
    material_quantity_per_part_costing_variable = 'Unit Material Qty'


class ERPDBConfig:
    """Config specific to connecting to m2n Intermediary DB"""

    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.instance = kwargs.get('instance')
        self.port = kwargs.get('port')
        self.name = kwargs.get('name')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')


class ERPDBConfigFactory:
    @staticmethod
    def create_configs(integration: Integration) -> [ERPDBConfig, M2MConfiguration]:
        if not integration.test_mode:
            logger.info('M2MExporter: Reading config specific configuration file')
            DB_HOST = os.environ.get('DB_HOST')
            DB_INSTANCE = os.environ.get('DB_INSTANCE')
            DB_PORT = os.environ.get('DB_PORT', '1433')
            DB_NAME = os.environ.get('DB_NAME')
            DB_USERNAME = os.environ.get('DB_USERNAME', 'sa')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            sql = ERPDBConfig(
                host=DB_HOST,
                instance=DB_INSTANCE,
                port=DB_PORT,
                name=DB_NAME,
                user=DB_USERNAME,
                password=DB_PASSWORD,
            )

        else:
            os.environ.setdefault('TEST', '1')
            sql = ERPDBConfig(
                host="test",
                instance="test",
                port=0,
                name="test",
                user="test",
                password="test",
                paperless_user="test",
                email_password="test",
            )

        m2m_config = M2MConfiguration()
        m2m_settings: dict = integration.config_yaml.get('M2M', {})
        export_settings: dict = integration.config_yaml.get('Exporters', {})
        order_settings: dict = export_settings.get('orders', {})

        # populate the configuration object
        for attribute, value in (m2m_settings | order_settings).items():
            if hasattr(m2m_config, attribute):
                final_value = value
                # Convert boolean strings to booleans
                if value == 'True':
                    final_value = True
                elif value == 'False':
                    final_value = False
                setattr(m2m_config, attribute, final_value)

        # populate the item -> work center mapping in the config
        purchase_work_center_map: list = m2m_settings.get('purchase_work_center_map', [])
        for item in purchase_work_center_map:
            j_item = json.loads(item)
            o_item = PurchaseToWorkCenterMap(work_centers=j_item.get('workcenters', []),
                                             search=j_item.get('search'))
            m2m_config.purchase_work_center_maps.append(o_item)

        return sql, m2m_config
