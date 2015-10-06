"""
WSGI config for running selenium tests only.

Sole difference is that it uses the lovely WhiteNoise to serve our static files.
"""

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
