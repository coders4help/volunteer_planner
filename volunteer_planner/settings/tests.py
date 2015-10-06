from .base import *

# Settings for running our tests

# TODO: Should run with DEBUG = False
DEBUG = True

# TODO: Should run against MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Intentionally out of repository so that git clean doesn't delete the file.
        'NAME': 'db.sqlite3',
    }
}

SECRET_KEY = 'Kitten like fish'
