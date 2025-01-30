

class MaterialImportConfig:
    def __init__(self, **kwargs):
        self.abc = kwargs.get('abc')


class AccountImportConfig:
    def __init__(self, config_yaml):
        accounts_yaml = config_yaml.get("Importers", {}).get("accounts", {})
        self.should_import_inactive_customers = accounts_yaml.get("should_import_inactive_customers", False)
        self.should_import_inactive_contacts = accounts_yaml.get("should_import_inactive_contacts", True)
        self.should_import_contacts = accounts_yaml.get('should_import_contacts', True)
        self.should_import_billing_addresses = accounts_yaml.get('should_import_billing_addresses', True)
        self.should_import_shipping_addresses = accounts_yaml.get('should_import_shipping_addresses', True)


class ContactImportConfig:
    def __init__(self, **kwargs):
        self.abc = kwargs.get('abc')


class PurchasedComponentImportConfig:
    def __init__(self, **kwargs):
        self.abc = kwargs.get('abc')
