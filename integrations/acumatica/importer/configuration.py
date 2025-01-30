class AcumaticaWorkCenterConfig:
    def __init__(self, config_yaml):
        workcenter_yaml = config_yaml.get("Importers", {}).get("work_centers", {})
        self.interval_mins = workcenter_yaml.get("interval", None)


class AcumaticaRawMaterialConfig:
    def __init__(self, config_yaml):
        material_yaml = config_yaml.get("Importers", {}).get("materials", {})
        self.interval_mins = material_yaml.get("interval", None)
        self.raw_material_item_class = material_yaml.get("raw_material_item_class", None)


class AcumaticaPurchasedComponentConfig:
    def __init__(self, config_yaml):
        pc_yaml = config_yaml.get("Importers", {}).get("purchased_components", {})
        self.interval_mins = pc_yaml.get("interval", None)
        self.pc_item_class = pc_yaml.get("pc_item_class", None)


class AcumaticaVendorConfig:
    def __init__(self, config_yaml):
        vendor_yaml = config_yaml.get("Importers", {}).get("vendors", {})
        self.interval_mins = vendor_yaml.get("interval", None)


class AcumaticaOutsideServiceConfig:
    def __init__(self, config_yaml):
        vendor_yaml = config_yaml.get("Importers", {}).get("outside_services", {})
        self.interval_mins = vendor_yaml.get("interval", None)
        self.outside_service_item_class = vendor_yaml.get("outside_service_item_class", None)


class AcumaticaAccountConfig:
    def __init__(self, config_yaml):
        account_yaml = config_yaml.get("Importers", {}).get("accounts", {})
        self.interval_mins = account_yaml.get("interval", None)
