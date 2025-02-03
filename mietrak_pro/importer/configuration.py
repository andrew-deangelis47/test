

class CustomerImportConfig:
    def __init__(self, **kwargs):
        self.should_import_sold_to_address = kwargs.get('should_import_sold_to_address')
        self.should_import_billing_address = kwargs.get('should_import_billing_address')
        self.should_import_shipping_addresses = kwargs.get('should_import_shipping_addresses')
        self.should_import_contacts = kwargs.get('should_import_contacts')
        self.should_skip_incomplete_addresses = kwargs.get('should_skip_incomplete_addresses')
        self.should_use_customer_terms = kwargs.get('should_use_customer_terms')


class MaterialImportConfig:
    def __init__(self, **kwargs):
        self.should_skip_material_no_description = kwargs.get('should_skip_material_no_description')
        self.should_skip_inactive = kwargs.get('should_skip_inactive')
        self.should_import_category = kwargs.get('should_import_category')
        self.should_import_leadtime = kwargs.get("should_import_leadtime", False)
        self.should_import_vendor = kwargs.get("should_import_vendor", False)
        self.should_import_po_history = kwargs.get("should_import_po_history", False)


class PurchasedComponentImportConfig:
    def __init__(self, **kwargs):
        self.should_skip_non_inventory_items = kwargs.get('should_skip_non_inventory_items')
        self.should_skip_inactive = kwargs.get('should_skip_inactive')
        self.should_import_category = kwargs.get('should_import_category')
        self.should_import_leadtime = kwargs.get("should_import_leadtime", False)
        self.should_import_po_history = kwargs.get("should_import_po_history", False)


class OutsideServiceImportConfig:
    def __init__(self, **kwargs):
        self.part_number_exclusion_term = kwargs.get('part_number_exclusion_term')
        self.starting_year = kwargs.get('starting_year')
        self.should_import_category = kwargs.get('should_import_category')
        self.should_import_leadtime = kwargs.get('should_import_leadtime')
        self.should_import_costs = kwargs.get('should_import_costs')


class WorkCenterImportConfig:
    def __init__(self, **kwargs):
        self.should_import_operations = kwargs.get('should_import_operations')
        self.should_skip_inactive = kwargs.get('should_skip_inactive')
        self.should_import_division = kwargs.get('should_import_division')
