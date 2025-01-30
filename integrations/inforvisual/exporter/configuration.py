class InforVisualConfig:
    """Config specific to connecting to InforVisual"""
    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.instance = kwargs.get('instance')
        self.port = kwargs.get('port')
        self.name = kwargs.get('name')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.paperless_user = kwargs.get('paperless_user')
        self.email_password = kwargs.get('email_password')
        self.update_customers = kwargs.get('update_customers')
        self.send_email_when_customer_not_found = kwargs.get('send_email_when_customer_not_found')
        self.vendor_variable = kwargs.get('vendor_variable')
        self.pp_mat_id_variable = kwargs.get('pp_mat_id_variable')
        self.pp_parts_per_material_unit_variable = kwargs.get('pp_parts_per_material_unit_variable')
        self.default_site_id = kwargs.get('default_site_id')
        self.create_purchased_component = kwargs.get('create_purchased_component')
        self.create_material = kwargs.get('create_material')
        self.leg_assembly = kwargs.get('leg_assembly')
        self.should_export_assemblies_with_duplicate_components = kwargs.get(
            "should_export_assemblies_with_duplicate_components"
        )

        self.vendor_id_var = kwargs.get('vendor_id_var')
        self.service_id_var = kwargs.get('service_id_var')
        self.service_min_chg_var = kwargs.get('service_min_chg_var')
        self.run_cost_per_unit_var = kwargs.get('run_cost_per_unit_var')
        self.transit_days_var = kwargs.get('transit_days_var')
        self.work_center_var = kwargs.get('work_center_var')
