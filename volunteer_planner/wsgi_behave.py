"""
WSGI config for running selenium tests only.

Main difference is that it uses the lovely WhiteNoise to serve our static files.
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volunteer_planner.settings.local")

application = DjangoWhiteNoise(get_wsgi_application())
