# coding: utf-8

from volunteer_planner.settings.local import *  # noqa: F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "NAME": os.environ.get("DATABASE_NAME", "volunteer_planner"),
        "PASSWORD": os.environ.get("DATABASE_PW", "volunteer_planner"),
        "USER": os.environ.get("DB_USER", "vp"),
    }
}
