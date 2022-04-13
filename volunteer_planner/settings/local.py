# coding=utf-8

from .base import *  # noqa: F401

DEBUG = True
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # Intentionally out of repository so that git clean doesn't delete the
        # file.
        "NAME": os.path.join(SITE_ROOT, "db.sqlite3"),
    }
}

INSTALLED_APPS += ("debug_toolbar",)

# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": os.environ.get(
            "CACHE_BACKEND", "django.core.cache.backends.locmem.LocMemCache"
        ),
    }
}
# END CACHE CONFIGURATION

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s",
        },
        "verbose": {
            "format": "%(asctime)s - %(name)s (%(filename)s:%(lineno)d) "
            "[%(levelname)s] (%(process)d/%(thread)d): %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "local.log",
            "mode": "a",
            "encoding": "utf8",
            "formatter": "verbose",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
        "django.db": {
            "level": "INFO",
        },
    },
}

SECRET_KEY = os.environ.get("SECRET_KEY", "local")

# for testing on mobile devices in local networks it's necessary to overwrite
# with a local ip
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]").split(
    sep=","
)
