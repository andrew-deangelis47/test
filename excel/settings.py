import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = ['excel', ]
MIDDLEWARE = []
WSGI_APPLICATION = 'excel.application'

IS_TEST = any("test" in string for string in sys.argv) or os.environ.get('TEST')

SECRET_KEY = '...'
