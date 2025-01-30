import os

default_app_config = 'm1.apps.M1Config'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "m1.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
