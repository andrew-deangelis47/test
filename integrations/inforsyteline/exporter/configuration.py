class InforSytelineConfig:
    """Config specific to connecting to InforSyteline"""
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.site_ref = kwargs.get('site_ref')
        self.pp_work_center_variable = kwargs.get('pp_work_center_variable')
        self.fail_if_new_customer = kwargs.get('fail_if_new_customer')
        self.default_product_code = kwargs.get('default_product_code')
        self.job_route_schedule_driver = kwargs.get('job_route_schedule_driver')
        self.job_route_backflush_type = kwargs.get('job_route_backflush_type')
