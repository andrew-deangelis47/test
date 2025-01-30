import os

default_app_config = 'm2m.apps.M2MConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "m2m.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
