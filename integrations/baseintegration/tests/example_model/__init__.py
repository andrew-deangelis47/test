import os
default_app_config = 'example_model.apps.ExampleModelConfig'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baseintegration.tests.example_model.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
