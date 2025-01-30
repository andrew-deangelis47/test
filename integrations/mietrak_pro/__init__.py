import os

default_app_config = 'mietrak_pro.apps.MietrakProConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mietrak_pro.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
