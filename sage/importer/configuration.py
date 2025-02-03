class SageWorkCenterConfig:
    def __init__(self, config_yaml):
        workcenter_yaml = config_yaml.get("Importers", {}).get("work_centers", {})
        self.interval_mins = workcenter_yaml.get("interval", None)


class SageRawMaterialConfig:
    def __init__(self, config_yaml):
        material_yaml = config_yaml.get("Importers", {}).get("materials", {})
        self.interval_mins = material_yaml.get("interval", None)


class SagePurchasedComponentConfig:
    def __init__(self, config_yaml):
        pc_yaml = config_yaml.get("Importers", {}).get("purchased_components", {})
        self.interval_mins = pc_yaml.get("interval", None)


class SageVendorConfig:
    def __init__(self, config_yaml):
        vendor_yaml = config_yaml.get("Importers", {}).get("vendors", {})
        self.interval_mins = vendor_yaml.get("interval", None)


class SageAccountConfig:
    def __init__(self, config_yaml):
        account_yaml = config_yaml.get("Importers", {}).get("accounts", {})
        self.interval_mins = account_yaml.get("interval", None)
