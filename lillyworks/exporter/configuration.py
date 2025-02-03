class LillyWorksConfig:
    """Config specific to connecting to InforVisual"""
    def __init__(self, **kwargs):
        self.email_address = kwargs.get('email_address')
        self.password = kwargs.get('password')
        self.which = kwargs.get('which')
        self.company_name = kwargs.get('company_name')
        self.default_quote_name = kwargs.get('default_quote_name')
        self.lookup_customers_by_id = kwargs.get('lookup_customers_by_id')
