from baseintegration.datamigration import logger
from plex.client import PlexClient

OP_INCREMENT = 100


class PlexConfig:

    def __init__(self, **kwargs):
        self.order_tier = kwargs.get('order_tier', '3')
        self.account_reactivation_enabled = kwargs.get('account_reactivation_enabled', False)
        self.account_reactivation_status = kwargs.get('account_reactivation_status', 'Active')
        self.default_part_type = kwargs.get('default_part_type')
        self.default_part_group = kwargs.get('default_part_group')
        self.default_part_status = kwargs.get('default_part_status')
        self.default_part_source = kwargs.get('default_part_source')
        self.default_product_type = kwargs.get('default_product_type')
        self.default_part_operation_type = kwargs.get('default_part_operation_type', 'Production')
        self.default_part_building_code = kwargs.get('default_part_building_code', '')
        self.part_information_op_def_name = kwargs.get('default_part_building_code', 'Part Information')
        self.part_info_costing_variable_part_type = kwargs.get('part_info_costing_variable_part_type', 'Part Type')
        self.part_info_costing_variable_part_group = kwargs.get('part_info_costing_variable_part_group', 'Part Group')
        self.part_info_costing_variable_part_status = kwargs.get('part_info_costing_variable_part_status', 'Part Status')
        self.part_info_costing_variable_part_source = kwargs.get('part_info_costing_variable_part_source', 'Part Source')
        self.part_info_costing_variable_product_type = kwargs.get('part_info_costing_variable_product_type', 'Production Type')
        self.part_info_costing_variable_building_code = kwargs.get('part_info_costing_variable_building_code', 'Building Code')
        self.default_bom_depletion_unit_type = kwargs.get('default_bom_depletion_unit_type', None)
        self.default_bom_depletion_conversion_factor = kwargs.get('default_bom_depletion_conversion_factor', None)
        self.default_operation_code = kwargs.get('default_operation_code')
        self.default_sales_order_type = kwargs.get('default_sales_order_type', 'Spot Buy')
        self.default_sales_order_status = kwargs.get('default_sales_order_status', 'Open')
        self.default_sales_order_release_type = kwargs.get('default_sales_order_release_type', 'Ship Schedule')
        self.default_sales_order_release_status = kwargs.get('default_sales_order_release_status', 'Open')
        self.default_sales_order_freight_terms = kwargs.get('default_sales_order_freight_terms', 'Collect')
        self.default_sales_order_carrier_code = kwargs.get('default_sales_order_carrier_code')
        self.default_sales_order_category = kwargs.get('default_sales_order_category')
        self.default_sales_order_line_unit_type = kwargs.get('default_sales_order_line_unit_type', 'Ea')
        self.sales_order_line_use_default_order_unit_id = kwargs.get('sales_order_line_use_default_order_unit_id', False)
        self.default_ship_from_building_code = kwargs.get('default_ship_from_building_code', 'Building 1')
        self.ship_date_time_offset = kwargs.get('ship_date_time_offset', 0)
        self.ship_date_due_date_offset = kwargs.get('ship_date_due_date_offset', 0)
        self.default_sales_person = kwargs.get('default_sales_person')
        self.datasources_tier_2_order = kwargs.get('datasources_tier_2_order', None)
        self.datasources_tier_2_line_item = kwargs.get('datasources_tier_2_line_item', None)
        self.datasources_work_center = kwargs.get('datasources_work_center', None)
        self.operation_code_map_table = kwargs.get('operation_code_map_table', 'Operations_Mapping')
        self.plex_operation_code_column_header = kwargs.get('plex_operation_code_column_header', 'Plex_Operation_Code')
        self.material_table_part_number_header = kwargs.get('material_table_part_number_header', 'PartNo')
        self.costing_variable_material_search = kwargs.get('costing_variable_material_search', 'Material Search')
        self.paperless_operation_name_column_header = kwargs.get('paperless_operation_name_column_header',
                                                                 'Paperless_Operation_Name')
        self.can_creat_new_customers = kwargs.get('can_creat_new_customers', True)
        self.default_customer_type = kwargs.get('default_customer_type', '')
        self.powder_op_sub_string = kwargs.get('powder_op_sub_string', 'POWDERCOAT')
        self.children_go_to_op = kwargs.get('children_go_to_op', ['ASSEMBLY'])
        self.use_plex_address_as_fallback = kwargs.get('use_plex_address_as_fallback', True)
        self.costing_variable_work_center_code = kwargs.get('costing_variable_work_center_code', "Workcenter Code")
        self.costing_variable_supplier_code = kwargs.get('costing_variable_supplier_code', "Supplier Code")
        self.costing_variable_work_center_crew_size = kwargs.get('costing_variable_work_center_crew_size',
                                                                 "Number Crew")
        self.costing_variable_operation_type = kwargs.get('costing_variable_operation_type', "Operation Type")
        self.import_customer_status_include_filter = kwargs.get('import_customer_status_include_filter', ['Active'])
        self.part_operation_increment_step = kwargs.get('part_operation_increment_step', OP_INCREMENT)


class ERPConfigFactory:
    @staticmethod
    def create_config(integration) -> [PlexConfig, PlexClient]:
        logger.info("setting up erp config")

        plex_config = PlexConfig()
        parser = integration.config_yaml.get("Plex", {})
        for k, v in parser.items():
            # If the value is literally 'False' then convert to Bool
            if v == 'False':
                v = False
            if v == 'True':
                v = True
            logger.info(f"Plex config: {k} - {v}")
            setattr(plex_config, k, v)

        # TODO: Putting here for now, maybe it should move to it's own method?
        plex_secrets = integration.secrets.get('Plex', {})
        plex_client = PlexClient(
            base_url=plex_secrets.get('base_url', 'https://test.connect.plex.com'),
            api_key=plex_secrets.get('api_key', 'bogusplexapikey'),
            base_url_data_source=plex_secrets.get('base_url_data_source', ''),
            username=plex_secrets.get('username', None),
            password=plex_secrets.get('password', None),
            pcn=plex_secrets.get('pcn', None)
        ).get_instance()

        return plex_config, plex_client
