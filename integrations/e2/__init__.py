import os

default_app_config = 'e2.apps.E2Config'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e2.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
