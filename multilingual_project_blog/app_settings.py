"""Settings for the ``multilingual_project_blog`` app."""
from django.conf import settings


ENVIRONMENT = getattr(settings, 'ENVIRONMENT', 'prod')
SITE_URL = getattr(settings, 'SITE_URL', 'http://www.example.com')
SITE_URL_NAME = getattr(settings, 'SITE_URL_NAME', 'www.example.com')
INFO_EMAIL = getattr(settings, 'INFO_EMAIL', 'info@example.com')
