class CetecConfig:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.preshared_token = kwargs.get('preshared_token')
        self.import_source_name = kwargs.get('import_source_name')
        self.internal_customer_id = kwargs.get('internal_customer_id')
        self.internal_vendor_id = kwargs.get('internal_vendor_id')
        self.place_order = kwargs.get('place_order')
        self.default_work_center = kwargs.get('default_work_center')
        self.default_trans_code = kwargs.get('default_trans_code')
