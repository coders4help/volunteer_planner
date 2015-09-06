"""
WSGI config for boilerplate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see

"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volunteer_planner.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
