from baseintegration.utils import set_sql_env_variables, CONNECTION_FAILURE_STRING, CONNECTION_SUCCESS_STRING, \
    log_connection_error_for_icc
import os
import yaml
import importlib

####################################################################################################
# THIS IS NOT A RELIABLE WAY TO CHECK CONNECTION
# We have seen some buggy behavior when using this method to check connections
# If this is failing for you then try checking connection by running an import or export of some sort
#####################################################################################################

if os.path.exists(os.path.join(os.path.dirname(__file__), "../openssl_conf.cnf")):
    os.environ.setdefault('OPENSSL_CONF', 'openssl_conf.cnf')
elif os.path.exists(os.path.join(os.path.dirname(__file__), "../openssl_local.cnf")):
    os.environ.setdefault('OPENSSL_CONF', 'openssl_local.cnf')
try:
    with open(os.path.join(os.path.dirname(__file__), "../config.yaml")) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config_yaml = yaml.load(file, Loader=yaml.FullLoader)
except Exception:
    raise ValueError("Config.yaml was not read correctly")
erp_dir = config_yaml["Paperless"]["dir_to_preserve"]


def check_connection(erp_dir: str) -> None:
    if os.path.exists(os.path.join(os.path.dirname(__file__), f"{erp_dir}/check_connection.py")):
        mod = importlib.import_module(f'{erp_dir}.check_connection')
        check_connection = getattr(mod, 'check_connection')
        check_connection()
    else:
        set_sql_env_variables()
        importlib.import_module(erp_dir)
        from django.db import connections
        try:
            db_conn = connections['default']
            db_conn.cursor()
            print(CONNECTION_SUCCESS_STRING)
        except Exception as e:
            print(e)
            log_connection_error_for_icc(e)
            print(CONNECTION_FAILURE_STRING)
            raise ValueError(CONNECTION_FAILURE_STRING)


check_connection(erp_dir)
