import os
default_app_config = 'inforvisual.apps.InforVisualConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inforvisual.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
