# required for SQL based integrations
# To run inspect_db, use the runner's "bash" command and then run something like
# python manage.py inspectdb --settings=‘mietrak_pro.settings’
import sys
from baseintegration.utils import set_sql_env_variables
set_sql_env_variables()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
