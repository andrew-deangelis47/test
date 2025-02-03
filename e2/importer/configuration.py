class CustomerImportConfig:
    def __init__(self, **kwargs):
        self.should_import_sold_to_address = kwargs.get('should_import_sold_to_address')
        self.should_import_billing_address = kwargs.get('should_import_billing_address')
        self.should_import_shipping_addresses = kwargs.get('should_import_shipping_addresses')
        self.should_import_contacts = kwargs.get('should_import_contacts')
        self.should_import_salesperson_for_account = kwargs.get('should_import_salesperson_for_account')
        self.should_skip_incomplete_addresses = kwargs.get('should_skip_incomplete_addresses')
        self.tax_exempt_code = kwargs.get('tax_exempt_code')


class E2RepeatWorkConfig:
    def __init__(self, config_yaml):
        rw_yaml = config_yaml.get("Importers", {}).get("repeat_part", {})
        self.raw_material_prod_codes = rw_yaml.get("raw_material_prod_codes", [])
