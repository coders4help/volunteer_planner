from .local import *  # noqa: F401

DEBUG = False

# Needed for letting Selenium access our server.
ALLOWED_HOSTS += ["localhost"]

SECRET_KEY = "Kitten like fish"
