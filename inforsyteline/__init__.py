import os
default_app_config = 'inforsyteline.apps.InforVisualConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inforsyteline.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
