import os
import socket
import sys

from baseintegration.utils import set_sql_env_variables


def lookup_port_for_instance(ip_address, instance_name):
    """Use SQL Browser service to get the port number for a SQL Server named
    instance."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    message = b'\x04' + instance_name.encode()
    sock.sendto(message, (ip_address, 1434))
    r = sock.recv(1024)
    # Example response:
    # b'\x05\x8c\x00ServerName;SERVER;InstanceName;SQLEXPRESS;IsClustered;No;Version;14.0.1000.169;tcp;50492;np;\\\\networkpath;;'
    words = r[3:].decode().split(';')
    port_str = words[words.index('tcp') + 1]
    return port_str


# Django boilerplate
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALLED_APPS = ['visualestitrack.apps.VisualEstiTrackConfig']
MIDDLEWARE = []

IS_TEST = any("test" in string for string in sys.argv) or os.environ.get('TEST')

# set up database for test or production
if IS_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'visualestitrack_test',
        }
    }
else:

    set_sql_env_variables()
    # database authentication from environment
    # on Windows, specify instance name as part of host (e.g., MYSERVER\SQLEXPRESS)
    # on Linux, use IP address and DB_INSTANCE
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_INSTANCE = os.environ.get('DB_INSTANCE')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    if DB_INSTANCE:
        DB_PORT = lookup_port_for_instance(DB_HOST, DB_INSTANCE)
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'NAME': DB_NAME,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD
        }
    }
    if sys.platform != 'win32':
        DATABASES['default']['OPTIONS'] = {
            'driver': 'ODBC Driver 17 for SQL Server'
        }


SECRET_KEY = '...'
