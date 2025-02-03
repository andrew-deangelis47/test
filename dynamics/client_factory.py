from baseintegration.datamigration import logger
from dynamics.client import DynamicsClient


class ClientFactory:
    @staticmethod
    def build_client_from_config(secrets, test_mode):
        if not test_mode:
            secrets = secrets["Dynamics"]

            return DynamicsClient(
                tenant_id=secrets["tenant_id"],
                client_id=secrets["client_id"],
                client_secret=secrets["client_secret"],
                environment_name=secrets["environment_name"],
                company_name=secrets["company_name"]
            )
        else:
            return DynamicsClient(
                tenant_id='test',
                client_id='test',
                client_secret='test',
                environment_name='test',
                company_name='test'
            )


class DynamicsConfig:
    def __init__(self):
        pass


class ConfigFactory:
    @staticmethod
    def build_config(config_yaml):
        erp_config = DynamicsConfig()
        for k, v in config_yaml.items():
            # If the value is literally 'False' then convert to Bool
            if v == 'False':
                v = False
            logger.info(f"Dynamics config: {k} - {v}")
            setattr(erp_config, k, v)

        return erp_config
