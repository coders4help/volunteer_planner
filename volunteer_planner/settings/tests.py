from .base import *
from datetime import timedelta

# Settings for running our tests

DEBUG = False

# Needed for letting Selenium access our server.
ALLOWED_HOSTS = ['localhost']

# TODO: Should run against MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Intentionally out of repository so that git clean doesn't delete the file.
        'NAME': 'db.sqlite3',
    }
}

SECRET_KEY = 'Kitten like fish'

DEFAULT_SHIFT_CONFLICT_GRACE = timedelta(hours=1)
