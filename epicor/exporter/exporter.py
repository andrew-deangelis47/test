from baseintegration.exporter.order_exporter import OrderExporter, logger
from epicor.client import EpicorClient
from epicor.exporter.v2_processors.part import PartProcessor
from epicor.exporter.v2_processors.customer import CustomerProcessor
from epicor.exporter.v2_processors.quote_header import QuoteHeaderProcessor
from epicor.exporter.v2_processors.quote_contact import QuoteContactProcessor
from epicor.exporter.v2_processors.quote_detail import QuoteDetailProcessor
from epicor.exporter.v2_processors.quote_quantity import QuoteQuantityProcessor
from epicor.exporter.v2_processors.quote_assembly import QuoteAssemblyProcessor
from epicor.exporter.v2_processors.quote_operation import QuoteOperationProcessor
from epicor.exporter.v2_processors.quote_material import QuoteMaterialProcessor
from epicor.exporter.v2_processors.add_on_charge import QuoteAddOnChargeProcessor
from epicor.customer import Customer
from epicor.part import Part
from epicor.quote import QuoteHeader, QuoteDetail, QuoteQuantity, QuoteAssembly, QuoteOperation, QuoteContact, QuoteMaterial
from epicor.miscellaneous_charges import QuoteMiscellaneousCharge
from paperless.objects.orders import Order
from epicor.utils import EpicorConfig


class EpicorOrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(Part, PartProcessor)
        self.register_processor(QuoteHeader, QuoteHeaderProcessor)
        self.register_processor(QuoteContact, QuoteContactProcessor)
        self.register_processor(QuoteDetail, QuoteDetailProcessor)
        self.register_processor(QuoteQuantity, QuoteQuantityProcessor)
        self.register_processor(QuoteAssembly, QuoteAssemblyProcessor)
        self.register_processor(QuoteMaterial, QuoteMaterialProcessor)
        self.register_processor(QuoteOperation, QuoteOperationProcessor)
        self.register_processor(QuoteMiscellaneousCharge, QuoteAddOnChargeProcessor)

    def _process_order(self, order: Order):
        logger.info(f"Processing order {order.number} to quote")
        try:
            with self.process_resource(Customer, order.contact, order.shipping_info) as customer:
                pass
            with self.process_resource(Part, order, customer) as quote_header_data:
                pass
            with self.process_resource(QuoteHeader, order, customer, quote_header_data) as quote_header:
                with self.process_resource(QuoteContact, order, customer, quote_header, quote_header_data):
                    pass
                with self.process_resource(QuoteDetail, order, customer, quote_header, quote_header_data) \
                        as quote_details_list:
                    with self.process_resource(QuoteQuantity, quote_header, quote_details_list,
                                               quote_header_data):
                        pass
                    with self.process_resource(QuoteMiscellaneousCharge, order, quote_header, quote_details_list,
                                               quote_header_data):
                        pass
                    with self.process_resource(QuoteAssembly, order, quote_header, quote_header_data):
                        pass
            with self.process_resource(QuoteOperation, order, quote_header, quote_header_data):
                pass
            with self.process_resource(QuoteMaterial, order, quote_header, quote_header_data):
                pass
            self.update_quote_line_item_engineered_statuses(quote_details_list)
            if self.integration_report is not None:
                self.integration_report.update_table()
        except Exception as e:
            # if we get a failure we still want to make sure we write to the integration report
            logger.info(f'Unexpected exception: {str(e)}')
            if self.integration_report is not None:
                self.integration_report.update_table()
            raise e

    def _setup_erp_client(self):
        if not self._integration.test_mode:
            epicor_yaml = self._integration.config_yaml["Epicor"]
            secrets = self._integration.secrets["Epicor"]
            if not self.erp_config:
                self.erp_config = EpicorConfig()
            self.erp_config.base_url = secrets["base_url"]
            self.erp_config.password = secrets["password"]
            self.erp_config.username = secrets["username"]
            self.erp_config.api_key = secrets["api_key"]
            self.erp_config.company_name = epicor_yaml["company_name"]
            self.erp_config.verify_ssl_cert = epicor_yaml["verify_ssl_cert"]
            self.erp_config.eco_group = epicor_yaml["eco_group"]
            self.erp_config.bearer_token = secrets.get("bearer_token", None)
            self.erp_config.plant_code = epicor_yaml.get("plant_code", None)

            # TODO: Putting here for now, maybe it should move to it's own method?
            self.epicor_client = EpicorClient(
                base_url=self.erp_config.base_url,
                password=self.erp_config.password,
                username=self.erp_config.username,
                api_key=self.erp_config.api_key,
                company_name=self.erp_config.company_name,
                verify_ssl_cert=self.erp_config.verify_ssl_cert,
                bearer_token=self.erp_config.bearer_token,
                plant_code=self.erp_config.plant_code
            )
        else:
            self.epicor_client = EpicorClient(
                base_url="https://localurl/EpicorERPTest/api/v2/odata/ABC",
                password="test",
                username="test",
                api_key="test",
                company_name="test",
                verify_ssl_cert=False,
                bearer_token="test"
            )

    def _setup_erp_config(self):
        if self._integration.test_mode:
            self._set_test_mode_config_defaults()
        else:
            self._set_production_erp_config()

    def _set_production_erp_config(self):
        """
        This function is responsible for assigning the Epicor 'erp_config' options from the config.yaml file.
        Add new config options here with reverse-compatible defaults specified.
        """
        order_export_yaml = self._integration.config_yaml["Exporters"]["orders"]
        if not self.erp_config:
            self.erp_config = EpicorConfig()
        self.erp_config.verify_ssl_cert = order_export_yaml.get("verify_ssl_cert", True)
        self.erp_config.search_for_existing_customer = order_export_yaml.get("search_for_existing_customer", True)
        self.erp_config.base_url = order_export_yaml.get("base_url")
        self.erp_config.password = order_export_yaml.get("password")
        self.erp_config.username = order_export_yaml.get("username")
        self.erp_config.api_key = order_export_yaml.get("api_key")
        self.erp_config.company_name = order_export_yaml.get("company_name")
        self.erp_config.eco_group = order_export_yaml.get("eco_group", "Paperless")
        self.erp_config.import_account_notes = order_export_yaml.get("import_account_notes", True)
        self.erp_config.new_customer_type = order_export_yaml.get('new_customer_type', 'PRO')
        self.erp_config.new_customer_check_duplicate_po = order_export_yaml.get('new_customer_check_duplicate_po',
                                                                                True)
        self.erp_config.default_payment_terms_code = order_export_yaml.get("default_payment_terms_code", 30)
        self.erp_config.should_mark_quotes_as_quoted = order_export_yaml.get("should_mark_quotes_as_quoted", False)
        self.erp_config.should_mark_quotes_as_engineered = \
            order_export_yaml.get("should_mark_quotes_as_engineered", False)
        self.erp_config.should_create_customer = order_export_yaml.get("should_create_customer", False)
        self.erp_config.default_customer_id = order_export_yaml.get("default_customer_id")
        self.erp_config.should_create_contact = order_export_yaml.get("should_create_contact", False)
        self.erp_config.default_contact_email = order_export_yaml.get("default_contact_email")
        self.erp_config.should_add_quote_contacts = order_export_yaml.get("should_add_quote_contacts", True)
        self.erp_config.should_create_shipping_address = order_export_yaml.get("should_create_shipping_address",
                                                                               False)
        self.erp_config.should_create_raw_materials = order_export_yaml.get("should_create_raw_materials", False)
        self.erp_config.pp_mat_id_variable = order_export_yaml.get("pp_mat_id_variable", "Material ID")
        self.erp_config.pp_mat_description_variable = order_export_yaml.get("pp_mat_description_variable",
                                                                            "Material Description")
        self.erp_config.pp_mat_cost_variable = order_export_yaml.get("pp_mat_cost_variable", "Cost")
        self.erp_config.pp_mat_UOMCode_variable = order_export_yaml.get("pp_mat_UOMCode_variable", "Cost UOM")
        self.erp_config.pp_op_id_variable = order_export_yaml.get("pp_op_id_variable", "Operation ID")
        self.erp_config.default_operation_id = order_export_yaml.get("default_operation_id",
                                                                     "CONFIG:default_operation_id")
        self.erp_config.pp_resource_group_id_variable = order_export_yaml.get("pp_resource_group_id_variable",
                                                                              "Resource Group ID")
        self.erp_config.pp_resource_id_variable = order_export_yaml.get("pp_resource_id_variable", "Resource ID")
        self.erp_config.default_hardware_class_id = order_export_yaml.get("default_hardware_class_id", "HDW")
        self.erp_config.default_non_root_mfg_class_id = order_export_yaml.get("default_non_root_mfg_class_id",
                                                                              "MFG")
        self.erp_config.default_raw_material_class_id = order_export_yaml.get('default_raw_material_class_id',
                                                                              "SHTS")
        self.erp_config.default_non_root_mfg_product_code = order_export_yaml.get("default_non_root_mfg_product_code",
                                                                                  "")
        self.erp_config.default_std_format = order_export_yaml.get("default_std_format", "HP")
        self.erp_config.default_std_basis = order_export_yaml.get("default_std_basis", "E")
        self.erp_config.default_raw_material_id = order_export_yaml.get("default_raw_material_id",
                                                                        "CONFIG:default_raw_material_id")
        self.erp_config.should_add_private_pp_notes_to_quote_detail = order_export_yaml.get(
            'should_add_private_pp_notes_to_quote_detail', False)
        self.erp_config.should_add_public_pp_notes_to_quote_detail = order_export_yaml.get(
            'should_add_public_pp_notes_to_quote_detail', True)
        self.erp_config.should_populate_reference_with_pp_quote_num = order_export_yaml.get(
            'should_populate_reference_with_pp_quote_num', False
        )
        self.erp_config.should_add_pp_part_viewer_link_to_quote_comments = order_export_yaml.get(
            'should_add_pp_part_viewer_link_to_quote_comments', False
        )
        self.erp_config.material_op_quantity_per_parent_var = order_export_yaml.get(
            'material_op_quantity_per_parent_var', 'CONFIG:material_op_quantity_per_parent_var')
        self.erp_config.pp_purchased_component_op_def_name = order_export_yaml.get(
            'pp_purchased_component_op_def_name', 'CONFIG:pp_purchased_component_op_def_name')
        self.erp_config.pp_purchased_component_op_piece_price_var = order_export_yaml.get(
            'pp_purchased_component_op_piece_price_var', 'CONFIG:pp_purchased_component_op_piece_price_var')
        self.erp_config.should_mark_quote_lines_as_template = order_export_yaml.get(
            'should_mark_quote_lines_as_template', False
        )
        self.erp_config.material_op_default_part_type = order_export_yaml.get(
            'material_op_default_part_type', "CONFIG:material_op_default_part_type"
        )
        self.erp_config.duplicate_part_number_append_character = order_export_yaml.get(
            'duplicate_part_number_append_character', 'CONFIG:duplicate_part_number_append_character'
        )
        self.erp_config.lead_time_unit_preference = self.validate_lead_time_units_config_options(
            order_export_yaml.get('lead_time_unit_preference', "calendar_days")
        )
        self.erp_config.default_manufactured_comp_cost_method = order_export_yaml.get(
            'default_manufactured_comp_cost_method', "S"
        )
        self.erp_config.default_purchased_comp_cost_method = order_export_yaml.get(
            'default_purchased_comp_cost_method', "L"
        )
        self.erp_config.default_material_op_cost_method = order_export_yaml.get(
            'default_material_op_cost_method', "L"
        )
        self.erp_config.set_mfg_components_as_non_stock = order_export_yaml.get(
            'set_mfg_components_as_non_stock', False
        )
        self.erp_config.set_hardware_components_as_non_stock = order_export_yaml.get(
            'set_hardware_components_as_non_stock', True
        )
        self.erp_config.default_salesperson_id = order_export_yaml.get('default_salesperson_id', None)
        self.erp_config.crew_size_variable = order_export_yaml.get('crew_size_variable', None)
        self.erp_config.crew_size_destination = self.validate_crew_size_destination_options(
            order_export_yaml.get('crew_size_destination', None)
        )
        self.erp_config.pp_vendor_id_variable = order_export_yaml.get('pp_vendor_id_variable',
                                                                      "CONFIG:pp_vendor_id_variable")
        self.erp_config.pp_vendor_unit_cost_variable = order_export_yaml.get('pp_vendor_unit_cost_variable',
                                                                             'CONFIG:pp_vendor_unit_cost_variable')
        self.erp_config.pp_vendor_lot_charge_variable = order_export_yaml.get('pp_vendor_lot_charge_variable',
                                                                              'CONFIG:pp_vendor_lot_charge_variable')
        self.erp_config.pp_mat_op_vendor_num = order_export_yaml.get('pp_mat_op_vendor_num',
                                                                     'CONFIG: pp_mat_op_vendor_num')
        self.erp_config.pp_mat_op_lead_time = order_export_yaml.get('pp_mat_op_lead_time', "CONFIG:pp_mat_op_lead_time")
        self.erp_config.disable_quote_operation_details = \
            order_export_yaml.get('disable_quote_operation_details', "CONFIG:disable_quote_operation_details")
        self.erp_config.add_ons_should_create_line_items = \
            order_export_yaml.get("add_ons_should_create_line_items", "CONFIG:add_ons_should_create_line_items")
        self.erp_config.add_ons_should_create_new_misc_charges = order_export_yaml.get(
            'add_ons_should_create_new_misc_charges', "CONFIG:add_ons_should_create_new_misc_charges")
        self.erp_config.default_misc_charge_code = order_export_yaml.get(
            "default_misc_charge_code", "CONFIG:default_misc_charge_code")
        self.erp_config.disable_part_creation = order_export_yaml.get('disable_part_creation', False)
        self.erp_config.set_auto_receive_into_inventory_on_last_operation = order_export_yaml.get(
            'set_auto_receive_into_inventory_on_last_operation', False)
        self.erp_config.set_final_operation_on_last_operation = order_export_yaml.get(
            'set_final_operation_on_last_operation', False)
        self.erp_config.default_root_component_class_id = order_export_yaml.get(
            'default_root_component_class_id', "CONFIG:default_root_component_class_id")
        self.erp_config.default_hardware_product_code = order_export_yaml.get(
            'default_hardware_product_code', "CONFIG:default_hardware_product_code"
        )
        self.erp_config.default_root_component_product_code = order_export_yaml.get(
            "default_root_component_product_code", "CONFIG:default_root_component_product_code"
        )
        self.erp_config.write_material_operation_notes_to_purchasing_comments = order_export_yaml.get(
            'write_material_operation_notes_to_purchasing_comments', True)
        self.erp_config.write_pc_part_description_to_purchasing_comments = order_export_yaml.get(
            'write_pc_part_description_to_purchasing_comments', True)
        self.erp_config.default_related_operation_num = order_export_yaml.get('default_related_operation_num', 0)
        self.erp_config.default_part_revision = order_export_yaml.get(
            'default_part_revision', '-')  # note that empty string or null are not valid options
        self.erp_config.default_line_item_add_on_part_number = order_export_yaml.get(
            'default_line_item_add_on_part_number', "CONFIG:default_line_item_add_on_part_number")
        self.erp_config.should_use_customer_part_numbers = order_export_yaml.get("should_use_customer_part_numbers",
                                                                                 False)
        self.erp_config.customer_part_number_auto_assignment_default = order_export_yaml.get(
            "customer_part_number_auto_assignment_default", "AutoAssign")
        self.erp_config.default_customer_part_number_part = order_export_yaml.get("default_customer_part_number_part",
                                                                                  "TEST")
        self.erp_config.set_quote_line_item_prod_code_from_first_pp_op = order_export_yaml.get(
            "set_quote_line_item_prod_code_from_first_pp_op", False)
        self.erp_config.set_quote_line_item_sales_code_from_first_pp_op = order_export_yaml.get(
            "set_quote_line_item_sales_code_from_first_pp_op", False)
        self.erp_config.custom_uom_class_dict = order_export_yaml.get('custom_uom_class_dict', False)

    @staticmethod
    def validate_lead_time_units_config_options(lead_time_units):
        if lead_time_units not in ("business_days", "calendar_days", "business_weeks", "calendar_weeks"):
            logger.info("Lead days will be defaulted to calendar days. Change the config if this is not correct.")
            return "calendar_days"
        return lead_time_units

    @staticmethod
    def validate_crew_size_destination_options(crew_size_destination):
        if crew_size_destination not in ("prod", "setup", "both", None):
            logger.info("Crew size destination is not valid. Change the config if this is not correct. "
                        "Crew size destination will be ignored by the integration until this corrected.")
            return None
        return crew_size_destination

    def _set_test_mode_config_defaults(self):
        """
        Use this class to set default values for test cases.
        """
        if not self.erp_config:
            self.erp_config = EpicorConfig()
        self.erp_config.pp_mat_id_variable = "JB Material ID"
        self.erp_config.company_name = "test"
        self.erp_config.default_contact_email = "qaemails+testing@paperlessparts.com"
        self.erp_config.pp_op_id_variable = "workcenter"
        self.erp_config.pp_resource_group_id_variable = "Resource Group ID"
        self.erp_config.pp_resource_id_variable = "Resource ID"
        self.erp_config.should_create_raw_materials = True
        self.erp_config.default_hardware_class_id = "HDW"
        self.erp_config.default_non_root_mfg_class_id = "MFG"
        self.erp_config.default_raw_material_class_id = "MTL"
        self.erp_config.should_create_customer = True
        self.erp_config.should_create_contact = True
        self.erp_config.should_add_quote_contacts = True
        self.erp_config.should_create_shipping_address = True
        self.erp_config.default_non_root_mfg_product_code = "HDW"
        self.erp_config.should_mark_quotes_as_quoted = True
        self.erp_config.should_mark_quotes_as_engineered = True
        self.erp_config.default_customer_id = "TEST"
        self.erp_config.pp_mat_description_variable = "TEST"
        self.erp_config.pp_mat_cost_variable = "Cost"
        self.erp_config.pp_mat_UOMCode_variable = "cost_unit_of_measure"
        self.erp_config.default_operation_id = "CONFIG:default_operation_id"
        self.erp_config.new_customer_type = 'PRO'
        self.erp_config.new_customer_check_duplicate_po = True
        self.erp_config.default_payment_terms_code = 30
        self.erp_config.default_std_format = "HP"
        self.erp_config.default_std_basis = "E"
        self.erp_config.default_raw_material_id = "JB Material ID"
        self.erp_config.should_add_public_pp_notes_to_quote_detail = True
        self.erp_config.should_add_private_pp_notes_to_quote_detail = True
        self.erp_config.should_populate_reference_with_pp_quote_num = True
        self.erp_config.should_add_pp_part_viewer_link_to_quote_comments = True
        self.erp_config.material_op_quantity_per_parent_var = "quantity_per_parent"
        self.erp_config.material_op_unit_cost_var = "unit_cost"
        self.erp_config.pp_purchased_component_op_def_name = "PC Piece Price"
        self.erp_config.pp_purchased_component_op_piece_price_var = "piece_price"
        self.erp_config.should_mark_quote_lines_as_template = False
        self.erp_config.material_op_default_part_type = "P"
        self.erp_config.duplicate_part_number_append_character = "CHILD"
        self.erp_config.lead_time_unit_preference = "calendar_days"
        self.erp_config.default_manufactured_comp_cost_method = "S"
        self.erp_config.default_purchased_comp_cost_method = "L"
        self.erp_config.default_material_op_cost_method = "L"
        self.erp_config.set_mfg_components_as_non_stock = True
        self.erp_config.set_hardware_components_as_non_stock = True
        self.erp_config.crew_size_variable = 'crew_size'
        self.erp_config.crew_size_destination = 'prod'
        self.erp_config.default_salesperson_id = "1"
        self.erp_config.pp_vendor_id_variable = "epicor_vendor_id"
        self.erp_config.pp_vendor_unit_cost_variable = "Piece Price"
        self.erp_config.pp_vendor_lot_charge_variable = "Lot Charge"
        self.erp_config.pp_mat_op_vendor_num = "epicor_vendor_num"
        self.erp_config.pp_mat_op_lead_time = "material_lead_days"
        self.erp_config.disable_quote_operation_details = False
        self.erp_config.add_ons_should_create_line_items = False
        self.erp_config.add_ons_should_create_new_misc_charges = False
        self.erp_config.default_misc_charge_code = "ABC"
        self.erp_config.disable_part_creation = False
        self.erp_config.set_auto_receive_into_inventory_on_last_operation = False
        self.erp_config.set_final_operation_on_last_operation = False
        self.erp_config.default_root_component_class_id = "ROOT"
        self.erp_config.default_hardware_product_code = "PURC"
        self.erp_config.default_root_component_product_code = "ASM1"
        self.erp_config.write_material_operation_notes_to_purchasing_comments = True
        self.erp_config.write_pc_part_description_to_purchasing_comments = True
        self.erp_config.default_related_operation_num = 0
        self.erp_config.default_part_revision = ' '
        self.erp_config.default_line_item_add_on_part_number = "PART-NUMBER"
        self.erp_config.should_use_customer_part_numbers = False
        self.erp_config.customer_part_number_auto_assignment_default = "AutoAssign"
        self.erp_config.default_customer_part_number_part = "TEST"
        self.erp_config.set_quote_line_item_prod_code_from_first_pp_op = False
        self.erp_config.set_quote_line_item_sales_code_from_first_pp_op = False
        self.erp_config.custom_uom_class_dict = False

    def update_quote_line_item_engineered_statuses(self, quote_details_list: [QuoteDetail]):
        if self.erp_config.should_mark_quotes_as_engineered:
            logger.info("Updating the 'Engineered' status on all quote line items to 'True'")
            for line_item in quote_details_list:
                line_item: QuoteDetail = line_item
                params = [f"'{self.erp_config.company_name}'", line_item.QuoteNum, line_item.QuoteLine]
                data = {"Engineer": True, "ReadyToQuote": True}
                line_item.update_resource(params, data)
