import os

default_app_config = 'excel.apps.ExcelConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "excel.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
