import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "integrations"))
sys.path.append(os.path.join(os.path.dirname(__file__), "integrations/m2m"))
sys.path.append(os.path.join(os.path.dirname(__file__), "integrations/baseintegration"))
from baseintegration.utils import set_sql_env_variables, run_integration

set_sql_env_variables()

if __name__ == '__main__':
    run_integration()
