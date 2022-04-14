# coding=utf-8

from .base import *  # noqa: F401
from .sentry import *  # noqa: F401

DEBUG = os.environ.get("DEV", False)

STATIC_ROOT = os.environ["STATIC_ROOT"]

# Let this be done by frontend reverse proxy, if required!
PREPEND_WWW = False

ADMINS = (("VP Admin", os.environ.get("ADMIN_EMAIL")),)

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE", "django.db.backends.mysql"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "NAME": os.environ.get("DATABASE_NAME"),
        "PASSWORD": os.environ.get("DATABASE_PW"),
        "USER": os.environ.get("DATABASE_USER"),
    }
}

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS", "volunteer-planner.org,www.volunteer-planner.org"
).split(sep=",") + ["localhost"]

SECRET_KEY = os.environ["SECRET_KEY"]

POST_OFFICE.update(
    {
        "BACKENDS": {"default": "django.core.mail.backends.smtp.EmailBackend"},
    }
)

SESSION_COOKIE_AGE = 28 * 24 * 3600
SESSION_COOKIE_SECURE = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

INTERNAL_IPS = ["127.0.0.1", "172.20.0.1"]
