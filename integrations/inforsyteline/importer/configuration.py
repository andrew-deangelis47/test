class RepeatPartImportConfig:
    def __init__(self, config_yaml):
        accounts_yaml = config_yaml.get("Importers", {}).get("repeat_part", {})
        self.material_product_codes = accounts_yaml.get("material_product_codes", [])
        self.purchased_component_product_codes = accounts_yaml.get("purchased_component_product_codes", [])
