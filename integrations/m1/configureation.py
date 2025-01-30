from baseintegration.datamigration import logger


class M1Config:

    def __init__(self, **kwargs):
        self.material_type_op_variable_name = kwargs.get('material_type_op_variable_name', 'Material Type')
        self.workcenter_code_op_variable_name = kwargs.get('workcenter_code_op_variable_name', 'Operation Code')
        self.process_type_op_variable_name = kwargs.get('process_type_op_variable_name', 'Process Type')


class ERPConfigFactory:
    @staticmethod
    def create_config(integration) -> M1Config:
        logger.info("setting up erp config")

        config = M1Config()
        parser = integration.config_yaml.get("M1", {})
        for k, v in parser.items():
            # If the value is literally 'False' then convert to Bool
            if v == 'False':
                v = False
            if v == 'True':
                v = True
            logger.info(f"M1 config: {k} - {v}")
            setattr(config, k, v)

        return config
