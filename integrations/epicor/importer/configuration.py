class EpicorRawMaterialConfig:
    def __init__(self, config_yaml):
        material_yaml = config_yaml.get("Importers", {}).get("materials", {})
        self.include_raw_material_class_ids = material_yaml.get("include_raw_material_class_ids", None)
        self.should_include_null_dates = material_yaml.get("should_include_null_dates", False)
        self.should_update_null_dates = material_yaml.get("should_update_null_dates", False)
        self.returned_record_limit = material_yaml.get("returned_record_limit", 10000)
        self.company_name = config_yaml.get("Epicor", {}).get("company_name", "CONFIG:company_name")


class EpicorPurchasedComponentConfig:
    def __init__(self, config_yaml):
        pc_yaml = config_yaml.get("Importers", {}).get("purchased_components", {})
        self.should_include_purchased_component_class_ids = pc_yaml.get(
            "should_include_purchased_component_class_ids", None)
        self.should_include_null_dates = pc_yaml.get("should_include_null_dates", False)
        self.should_update_null_dates = pc_yaml.get("should_update_null_dates", False)
        self.custom_column_header_names = pc_yaml.get("custom_column_header_names", [])
        self.corresponding_column_header_type = pc_yaml.get("corresponding_column_header_type", None)
        self.default_numeric_value = pc_yaml.get("default_numeric_value", 0.01)
        self.default_string_value = pc_yaml.get("default_string_value", "None")
        self.default_boolean_value = pc_yaml.get("default_boolean_value", False)
        self.returned_record_limit = pc_yaml.get("returned_record_limit", 10000)
        self.custom_purchased_component_columns = None
        self.company_name = config_yaml.get("Epicor", {}).get("company_name", "CONFIG:company_name")
        self.get_pc_price_from_part_cost = pc_yaml.get("get_pc_price_from_last_cost", False)


class EpicorWorkCenterConfig:
    def __init__(self, config_yaml):
        wc_yaml = config_yaml.get("Importers", {}).get("work_centers", {})
        self.should_import_resource_groups = wc_yaml.get("should_import_resource_groups", True)
        self.should_import_resources = wc_yaml.get("should_import_resources", True)
        self.should_map_multi_resource_group = wc_yaml.get("should_map_multi_resource_group", False)
        self.returned_record_limit = wc_yaml.get("returned_record_limit", 1000)


class EpicorRepeatWorkConfig:
    def __init__(self, config_yaml):
        rw_yaml = config_yaml.get("Importers", {}).get("repeat_part", {})
        self.company_name = config_yaml.get("Epicor", {}).get("company_name", "CONFIG:company_name")
        self.import_objects_newer_than = rw_yaml.get("import_objects_newer_than", "1970-01-01T00:00:00Z")
        self.is_post_enabled = rw_yaml.get("is_post_enabled", False)
        self.page_size = rw_yaml.get("page_size", 26)
        self.job_id_count_filter_limit = rw_yaml.get("job_id_count_filter_limit", 25)
        self.quote_id_count_filter_limit = rw_yaml.get("quote_id_count_filter_limit", 25)
        self.ewb_id_count_filter_limit = rw_yaml.get("ewb_id_count_filter_limit", 25)
