CONFIG_PATH = 'config.ini'
MIETRAK_PRO_CONFIG = None
CUSTOMER_IMPORT_CONFIG = None
from baseintegration.datamigration import logger
from types import SimpleNamespace
# Not needed, but creating local references to imported values
logger = logger


class MietrakProConfig:
    def __init__(self, **kwargs):
        self.tax_exempt_code = kwargs.get('tax_exempt_code')
        self.credit_card_terms_code = kwargs.get('credit_card_terms_code')
        self.company_division_pk = kwargs.get('company_division_pk')
        self.default_work_center_name = kwargs.get('default_work_center_name')
        self.default_work_center_code = kwargs.get('default_work_center_code')
        self.pp_work_center_pk_var = kwargs.get('pp_work_center_pk_var')
        self.pp_operation_pk_var = kwargs.get('pp_operation_pk_var')
        self.pp_revenue_account_num_var = kwargs.get('pp_revenue_account_num_var')
        self.pp_purchase_account_num_var = kwargs.get('pp_purchase_account_num_var')
        self.pp_outside_process_var = kwargs.get('pp_outside_process_var')
        self.default_outside_service_work_center_name = kwargs.get('default_outside_service_work_center_name')
        self.default_outside_service_work_center_code = kwargs.get('default_outside_service_work_center_code')
        self.default_outside_service_item_vendor_name = kwargs.get('default_outside_service_item_vendor_name')
        self.default_purchased_item_vendor_name = kwargs.get('default_purchased_item_vendor_name')
        self.default_terms = kwargs.get('default_terms')
        self.default_terms_period = kwargs.get('default_terms_period')
        self.default_assembly_operation_name = kwargs.get('default_assembly_operation_name')
        self.raw_material_part_number_variable_name = kwargs.get('raw_material_part_number_variable_name')
        self.raw_material_blank_width_variable_name = kwargs.get('raw_material_blank_width_variable_name')
        self.raw_material_blank_length_variable_name = kwargs.get('raw_material_blank_length_variable_name')
        self.raw_material_quantity_variable_name = kwargs.get('raw_material_quantity_variable_name')
        self.should_perform_assembly_conversion = kwargs.get('should_perform_assembly_conversion')
        self.should_create_mietrak_pro_billing_address = kwargs.get('should_create_mietrak_pro_billing_address')
        self.should_update_mietrak_pro_payment_terms = kwargs.get('should_update_mietrak_pro_payment_terms')
        self.should_create_mietrak_pro_shipping_address = kwargs.get('should_create_mietrak_pro_shipping_address')
        self.should_update_mietrak_pro_customer_notes = kwargs.get('should_update_mietrak_pro_customer_notes')
        self.should_update_mietrak_pro_contact_notes = kwargs.get('should_update_mietrak_pro_contact_notes')
        self.should_update_mietrak_pro_customer_misc_data = kwargs.get('should_update_mietrak_pro_customer_misc_data')
        self.should_update_mietrak_pro_contact_misc_data = kwargs.get('should_update_mietrak_pro_contact_misc_data')
        self.should_update_mietrak_pro_part_description = kwargs.get('should_update_mietrak_pro_part_description')
        self.should_update_mietrak_pro_purchased_components_data = kwargs.get(
            'should_update_mietrak_pro_purchased_components_data')
        self.should_create_mietrak_pro_raw_material_record = kwargs.get('should_create_mietrak_pro_raw_material_record')
        self.should_use_default_raw_material = kwargs.get('should_use_default_raw_material')
        self.should_rebuild_existing_mietrak_pro_routers = kwargs.get('should_rebuild_existing_mietrak_pro_routers')
        self.should_send_email_when_new_customer_is_created = kwargs.get(
            'should_send_email_when_new_customer_is_created')
        self.should_update_quote_erp_code_in_paperless_parts = kwargs.get(
            'should_update_quote_erp_code_in_paperless_parts')
        self.should_associate_purchased_components_with_assembly_operation = kwargs.get(
            'should_associate_purchased_components_with_assembly_operation')
        self.should_associate_subrouters_with_assembly_operation = kwargs.get(
            'should_associate_subrouters_with_assembly_operation')
        self.default_sales_order_fob = kwargs.get('default_sales_order_fob')
        self.parts_per_blank_variable_name = kwargs.get('parts_per_blank_variable_name')
        self.part_length_variable_name = kwargs.get('part_length_variable_name')
        self.part_width_variable_name = kwargs.get('part_width_variable_name')
        self.stock_length_variable_name = kwargs.get('stock_length_variable_name')
        self.stock_width_variable_name = kwargs.get('stock_width_variable_name')
        self.stock_thickness_variable_name = kwargs.get('stock_thickness_variable_name')
        self.density_variable_name = kwargs.get('density_variable_name')
        self.outside_service_item_vendor_variable = kwargs.get('outside_service_item_vendor_variable')
        self.should_export_assemblies_with_duplicate_components = kwargs.get(
            'should_export_assemblies_with_duplicate_components')
        self.division_map = self.dot_notation(kwargs.get('division_map'))
        self.pp_quote_reference_field = kwargs.get('pp_quote_reference_field')
        self.should_use_mietrak_salesperson = kwargs.get('should_use_mietrak_salesperson')
        self.overage_percentage_variable_name = kwargs.get('overage_percentage_variable_name')
        self.vendor_variable_name = kwargs.get('vendor_variable_name')
        self.leadtime_variable_name = kwargs.get('leadtime_variable_name')
        self.setup_charge_variable_name = kwargs.get('setup_charge_variable_name')
        self.quantity_per_inverse_variable_name = kwargs.get('quantity_per_inverse_variable_name')
        self.use_exact_material_calc_variable_name = kwargs.get('use_exact_material_calc_variable_name')
        self.osv_minimum_variable_name = kwargs.get('osv_minimum_variable_name')
        self.osv_piece_price_variable_name = kwargs.get('osv_piece_price_variable_name')

    def dot_notation(self, json_list):
        if not json_list:
            return None
        new_list = []
        for item in json_list:
            new_list.append(SimpleNamespace(**item))
        return new_list
