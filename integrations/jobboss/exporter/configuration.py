

class JobBOSSConfig:
    def __init__(self, **kwargs):
        self.sales_orders_active = kwargs.get('sales_orders_active')
        self.sales_order_default_status = kwargs.get('sales_order_default_status')
        self.should_link_addl_charge_to_sales_order_detail = kwargs.get(
            'should_link_addl_charge_to_sales_order_detail'
        )
        self.sales_code = kwargs.get('sales_code')
        self.import_material = kwargs.get('import_material')
        self.default_location = kwargs.get('default_location')
        self.import_operations = kwargs.get('import_operations')
        self.generate_material_ops = kwargs.get('generate_material_ops')
        self.assign_runtime_and_setup_time_from_standard_op_variables = kwargs.get(
            'assign_runtime_and_setup_time_from_standard_op_variables'
        )
        self.use_default_materials = kwargs.get('use_default_materials')
        self.default_raw_material = kwargs.get('default_raw_material')
        self.default_hardware_material = kwargs.get('default_hardware_material')
        self.pp_mat_id_variable = kwargs.get('pp_mat_id_variable')
        self.pp_material_code_ops = kwargs.get('pp_material_code_ops')
        self.material_req_default_pick_or_buy = kwargs.get('material_req_default_pick_or_buy')
        self.import_job_as = kwargs.get('import_job_as')
        self.op_ignore = kwargs.get('op_ignore')
        self.solo_mfg_comp_assembly = kwargs.get('solo_mfg_comp_assembly')
        self.assembly_conversion_should_adopt_top_level_part_number = kwargs.get(
            'assembly_conversion_should_adopt_top_level_part_number'
        )
        self.hardware_is_top_level_only = kwargs.get('hardware_is_top_level_only')
        self.should_create_new_hardware_materials = kwargs.get("should_create_new_hardware_materials")
        self.generate_finished_good_material = kwargs.get('generate_finished_good_material')
        self.should_assign_fg_to_parent = kwargs.get('should_assign_fg_to_parent')
        self.part_length_variable = kwargs.get('part_length_variable')
        self.part_width_variable = kwargs.get('part_width_variable')
        self.cutoff_variable = kwargs.get('cutoff_variable')
        self.facing_variable = kwargs.get('facing_variable')
        self.standard_bar_end_variable = kwargs.get('standard_bar_end_variable')
        self.parts_per_bar_variable = kwargs.get('parts_per_bar_variable')
        self.jb_calculator_qty = kwargs.get('jb_calculator_qty')
        self.is_rounded_variable = kwargs.get('is_rounded_variable')
        self.buy_item_description_variables = kwargs.get('buy_item_description_variables')
        self.buy_item_unit_cost = kwargs.get('buy_item_unit_cost')
        self.new_osv_method_enabled = kwargs.get('new_osv_method_enabled')  # note this has been deprecated
        self.osv_operations = kwargs.get('osv_operations')
        self.vendor_variable = kwargs.get('vendor_variable')
        self.service_variable = kwargs.get('service_variable')
        self.select_default_vendor = kwargs.get('select_default_vendor')
        self.custom_table_op_map_enabled = kwargs.get('custom_table_op_map_enabled')  # note this has been deprecated
        self.default_work_center_name = kwargs.get('default_work_center_name')
        self.standard_work_center_variable_name = kwargs.get('standard_work_center_variable_name')
        self.assembly_suffix_use_letters = kwargs.get('assembly_suffix_use_letters', "True")
        self.assembly_suffix_separator = kwargs.get('assembly_suffix_separator', "")
        self.template_job_matching_enabled = kwargs.get('template_job_matching_enabled')
        self.part_number_job_matching_enabled = kwargs.get('part_number_job_matching_enabled')
        self.revision_must_match = kwargs.get('revision_must_match')
        self.enable_estimator_mapping = kwargs.get('enable_estimator_mapping')
        self.default_estimator = kwargs.get("default_estimator")
        self.estimator_mapping_table_name = kwargs.get("estimator_mapping_table_name")
        self.estimator_email_column_name = kwargs.get("estimator_email_column_name")
        self.estimator_jb_id_column_name = kwargs.get("estimator_jb_id_column_name")
        self.should_email_when_job_created = kwargs.get("should_email_when_job_created")
        self.email_subject = kwargs.get("email_subject")
        self.email_body = kwargs.get("email_body")
        self.should_export_assemblies_with_duplicate_components = kwargs.get(
            "should_export_assemblies_with_duplicate_components"
        )
        self.should_update_quote_erp_code_in_paperless_parts = kwargs.get(
            "should_update_quote_erp_code_in_paperless_parts"
        )
        self.should_update_quote_line_status = kwargs.get("should_update_quote_line_status")
