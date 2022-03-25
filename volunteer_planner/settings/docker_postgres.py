# coding: utf-8

from .local import *  # noqa: F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "volunteer_planner",
        "HOST": "db",
        "USER": "vp",
        "PASSWORD": "volunteer_planner",
    }
}
