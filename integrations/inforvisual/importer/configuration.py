class InforVisualMaterialConfig:
    def __init__(self, config):
        self.filter = config.get('filter', {'product_code__in': ['RAW', 'HARDWARE', 'PAINT']})
        self.exclude = config.get('exclude', {})
        self.imported_columns = config.get('imported_columns', [
            {'column_name': 'material_id', 'source_column': 'id', 'default': 'N/A'},
            {'column_name': 'description', 'default': 'N/A'},
            {'column_name': 'user_1', 'default': 'N/A'},
            {'column_name': 'user_2', 'default': 'N/A'},
            {'column_name': 'user_3', 'default': 'N/A'},
            {'column_name': 'user_4', 'default': 'N/A'},
            {'column_name': 'user_5', 'default': 'N/A'},
            {'column_name': 'commodity_code', 'default': 'N/A'}
        ])


class InforVisualPurchasedComponentConfig:
    def __init__(self, config):
        self.import_from_purchase_orders = config.get('import_from_purchase_orders', False)
        self.filter = config.get('filter', {'product_code__in': ['RAW', 'HARDWARE', 'PAINT']})
        self.exclude = config.get('exclude', {})


class InforVisualWorkCenterConfig:
    def __init__(self, config):
        self.site_id = config.get('site_id')


class InforVisualVendorConfig:
    def __init__(self, config):
        pass


class InforVisualOutsideServiceConfig:
    def __init__(self, config):
        pass
