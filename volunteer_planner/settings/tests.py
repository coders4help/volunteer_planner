from .local import *
from datetime import timedelta

DEBUG = False

# Needed for letting Selenium access our server.
ALLOWED_HOSTS = ['localhost']

SECRET_KEY = 'Kitten like fish'
DEFAULT_SHIFT_CONFLICT_GRACE = timedelta(hours=1)
