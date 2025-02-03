from baseintegration.datamigration import logger
from plex_v2.client import PlexClient
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException

DEFAULT_OP_INCREMENT = 100


class PlexConfig:

    def __init__(self, **kwargs):
        self.order_tier = kwargs.get('order_tier', '3')
        self.default_part_type = kwargs.get('default_part_type')
        self.default_part_group = kwargs.get('default_part_group')
        self.default_part_status = kwargs.get('default_part_status')
        self.default_part_source = kwargs.get('default_part_source')
        self.default_product_type = kwargs.get('default_product_type')
        self.default_part_operation_type = kwargs.get('default_part_operation_type', 'Production')
        self.default_part_building_code = kwargs.get('default_part_building_code', '')
        self.part_information_op_def_name = kwargs.get('default_part_building_code', 'Part Information')
        self.part_type_var = kwargs.get('part_type_var', 'Part Type')
        self.part_group_var = kwargs.get('part_group_var', 'Part Group')
        self.part_status_var = kwargs.get('part_status_var', 'Part Status')
        self.part_source_var = kwargs.get('part_source_var', 'Part Source')
        self.part_product_type_var = kwargs.get('part_product_type_var', 'Production Type')
        self.part_building_code_var = kwargs.get('part_building_code_var', 'Building Code')
        self.default_operation_code = kwargs.get('default_operation_code')
        self.default_sales_order_type = kwargs.get('default_sales_order_type', 'Spot Buy')
        self.default_sales_order_status = kwargs.get('default_sales_order_status', 'Open')
        self.default_sales_order_release_type = kwargs.get('default_sales_order_release_type', 'Ship Schedule')
        self.default_sales_order_release_status = kwargs.get('default_sales_order_release_status', 'Open')
        self.default_sales_order_freight_terms = kwargs.get('default_sales_order_freight_terms', 'Collect')
        self.default_sales_order_carrier_code = kwargs.get('default_sales_order_carrier_code')
        self.default_sales_order_category = kwargs.get('default_sales_order_category')
        self.default_sales_order_line_unit_type = kwargs.get('default_sales_order_line_unit_type', 'Ea')
        self.default_ship_from_building_code = kwargs.get('default_ship_from_building_code', 'Building 1')
        self.ship_date_time_offset = kwargs.get('ship_date_time_offset', 0)
        self.ship_date_due_date_offset = kwargs.get('ship_date_due_date_offset', 0)
        self.default_sales_person = kwargs.get('default_sales_person')
        self.datasources_tier_2_order = kwargs.get('datasources_tier_2_order', None)
        self.operation_code_map_table = kwargs.get('operation_code_map_table', 'Operations_Mapping')
        self.plex_operation_code_column_header = kwargs.get('plex_operation_code_column_header', 'Plex_Operation_Code')
        self.plex_approved_workcenters_column_header = kwargs.get('plex_approved_workcenters_column_header', 'Plex_Operation_Code')
        self.plex_approved_suppliers_column_header = kwargs.get('plex_approved_suppliers_column_header', 'Plex_Operation_Code')
        self.paperless_only_column_header = kwargs.get('paperless_only_column_header', 'Plex_Operation_Code')
        self.material_table_part_number_header = kwargs.get('material_table_part_number_header', 'PartNo')
        self.var_material_part_number = kwargs.get('var_material_part_number', 'Material Search')
        self.var_material_part_revision = kwargs.get('var_material_part_revision', 'Material Search')
        self.paperless_operation_name_column_header = kwargs.get('paperless_operation_name_column_header',
                                                                 'Paperless_Operation_Name')
        self.can_creat_new_customers = kwargs.get('can_creat_new_customers', True)
        self.default_customer_type = kwargs.get('default_customer_type', '')
        self.use_plex_address_as_fallback = kwargs.get('use_plex_address_as_fallback', True)
        self.costing_variable_supplier_code = kwargs.get('costing_variable_supplier_code', "Supplier Code")
        self.import_customer_status_include_filter = kwargs.get('import_customer_status_include_filter', ['Active'])
        self.part_operation_increment_step = kwargs.get('part_operation_increment_step', DEFAULT_OP_INCREMENT)
        self.default_sales_order_payment_terms = kwargs.get('default_sales_order_payment_terms', None)
        self.part_operation_type_var_name = kwargs.get('part_operation_type_var_name', None)
        self.should_create_approved_workcenters = kwargs.get('should_create_approved_workcenters', None)
        self.should_create_approved_suppliers = kwargs.get('should_create_approved_suppliers', None)
        self.default_customer_status = kwargs.get('default_customer_status', None)
        self.routing_operation_to_ignore = []  # we set this via the Operations_Mapping table - should not be coming from the config file
        self.raw_material_part_attributes = kwargs.get('raw_material_part_attributes', [])
        self.default_raw_material_attribute_value = kwargs.get('default_raw_material_attribute_value', 'N/A')
        self.default_raw_material_numeric_value = kwargs.get('default_raw_material_numeric_value', 999)
        self.should_export_part_grade = kwargs.get('should_export_part_grade', False)
        self.part_grade_op_def_name = kwargs.get('part_grade_op_def_name', None)
        self.part_grade_var = kwargs.get('part_grade_var', None)
        self.should_import_material_pricing = kwargs.get('should_import_material_pricing', None)
        self.material_quantity_var = kwargs.get('material_quantity_var', None)
        self.should_export_part_cycle_frequency = kwargs.get('should_export_part_cycle_frequency', None)
        self.default_part_cycle_frequency = kwargs.get('default_part_cycle_frequency', None)
        self.part_cycle_frequency_var = kwargs.get('part_cycle_frequency_var', None)
        self.default_part_grade = kwargs.get('default_part_grade', None)
        self.default_raw_material_part_status = kwargs.get('default_raw_material_part_status', None)
        self.default_purchased_component_part_status = kwargs.get('default_purchased_component_part_status', None)
        self.part_lead_time_var = kwargs.get('part_lead_time_var', None)
        self.default_raw_material_lead_time = kwargs.get('default_raw_material_lead_time', None)
        self.raw_material_part_type_var = kwargs.get('raw_material_part_type_var', None)
        self.default_raw_material_part_type = kwargs.get('default_raw_material_part_type', None)
        self.default_purchased_component_part_type = kwargs.get('default_purchased_component_part_type', None)
        self.raw_material_part_status_var = kwargs.get('raw_material_part_status_var', None)
        self.default_raw_material_part_source = kwargs.get('default_raw_material_part_source', None)
        self.default_purchased_component_part_source = kwargs.get('default_purchased_component_part_source', None)
        self.default_part_group_raw_material = kwargs.get('default_part_group_raw_material', None)
        self.default_part_group_purchased_component = kwargs.get('default_part_group_purchased_component', None)
        self.default_product_type_raw_material = kwargs.get('default_product_type_raw_material', None)
        self.default_product_type_purchased_components = kwargs.get('default_product_type_purchased_components', None)
        self.default_part_grade_raw_material = kwargs.get('default_product_type_purchased_components', None)
        self.default_part_grade_purchased_component = kwargs.get('default_product_type_purchased_components', None)
        self.default_part_cycle_frequency_raw_material = kwargs.get('default_product_type_purchased_components', None)
        self.default_part_cycle_frequency_purchased_component = kwargs.get('default_product_type_purchased_components', None)
        self.plex_op_code_var = kwargs.get('plex_op_code_var', None)
        self.supplier_code_var = kwargs.get('supplier_code_var', None)
        self.piece_price_var = kwargs.get('piece_price_var', None)
        self.supplier_status_blacklist = kwargs.get('supplier_status_blacklist', None)
        self.routing_datasource_properties_required = kwargs.get('routing_datasource_properties_required', None)
        self.routing_datasource_properties_required_material = kwargs.get('routing_datasource_properties_required_material', None)
        self.should_import_pc_pricing = kwargs.get('should_import_pc_pricing', None)
        self.default_material_price = kwargs.get('default_material_price', None)
        self.default_material_price_unit = kwargs.get('default_material_price_unit', None)
        self.default_pc_price_unit = kwargs.get('default_pc_price_unit', None)
        self.default_pc_piece_price = kwargs.get('default_pc_piece_price', None)
        self.default_approved_workcenter_crew_size = kwargs.get('default_approved_workcenter_crew_size', None)
        self.crew_size_var = kwargs.get('crew_size_var', None)
        self.part_statuses_active = kwargs.get('part_statuses_active', [])
        self.should_export_part_building_code = kwargs.get('should_export_part_building_code', None)
        self.part_building_code_var = kwargs.get('part_building_code_var', None)
        self.default_building_code = kwargs.get('default_building_code', None)
        self.default_part_building_code_raw_material = kwargs.get('default_part_building_code_raw_material', None)
        self.default_part_building_code_purchased_component = kwargs.get('default_part_building_code_purchased_component', None)
        self.should_export_internal_note = kwargs.get('should_export_internal_note', None)
        self.internal_note_var = kwargs.get('internal_note_var', None)
        self.default_internal_note = kwargs.get('default_internal_note', None)
        self.default_internal_note_raw_material = kwargs.get('default_internal_note_raw_material', None)
        self.default_internal_note_purchased_component = kwargs.get('default_internal_note_purchased_component', None)
        self.purchased_component_types = kwargs.get('purchased_component_types', None)
        self.should_audit_existing_pcs = kwargs.get('should_audit_existing_pcs', None)
        self.should_create_order_lines_on_existing_order = kwargs.get('should_create_order_lines_on_existing_order', True)
        self.should_export_part_weight = kwargs.get('should_export_part_weight', True)
        self.part_weight_var = kwargs.get('part_weight_var', True)
        self.default_part_weight = kwargs.get('default_part_weight', True)
        self.default_part_weight_raw_material = kwargs.get('default_part_weight_raw_material', True)
        self.default_part_weight_purchased_component = kwargs.get('default_part_weight_purchased_component', True)
        self.should_import_customer_terms = kwargs.get('should_import_customer_terms', False)
        self.payment_mapping_custom_table_name = kwargs.get('payment_mapping_custom_table_name', None)
        self.default_payment_terms = kwargs.get('default_payment_terms', None)
        self.default_payment_terms_period = kwargs.get('default_payment_terms_period', None)
        self.should_use_customer_terms = kwargs.get('should_use_customer_terms', False)
        self.should_import_material_inventory = kwargs.get('should_import_material_inventory', False)
        self.material_inventory_properties = kwargs.get('material_inventory_properties', [])
        self.should_import_pc_inventory = kwargs.get('should_import_pc_inventory', False)
        self.pc_inventory_properties = kwargs.get('pc_inventory_properties', [])


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

    @staticmethod
    def create_importer_config(integration, importer_key: str) -> [PlexConfig, PlexClient]:
        if importer_key is None:
            raise CancelledIntegrationActionException('No importer key passed to create_importer_config')
        logger.info("setting up erp config")

        plex_config = PlexConfig()
        parser = integration.config_yaml.get("Importers", {})
        # getting the correct config values based on the importer key
        parser = parser[importer_key]
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
