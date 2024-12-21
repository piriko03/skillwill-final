"""
WSGI config for book lending project.

This file exposes the WSGI callable as a module-level variable named 'application'.
For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Point to your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# Create the WSGI application
application = get_wsgi_application()
