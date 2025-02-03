import os
default_app_config = 'visualestitrack.apps.VisualEstiTrackConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visualestitrack.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
