# coding=utf-8
"""
WSGI config for production setup.
"""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volunteer_planner.settings.production")

application = get_wsgi_application()
