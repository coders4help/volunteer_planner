#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volunteer_planner.settings.local")
    os.environ.setdefault("DATABASE_PW", "")
    os.environ.setdefault("DB_USER", "")
    os.environ.setdefault("SECRET_KEY", "1")
    os.environ.setdefault("LANGUAGE", "de")

    # if you omit this values dummy email backend will be used
    os.environ.setdefault("EMAIL_ADDRESS", "")
    os.environ.setdefault("EMAIL_HOST_PASSWORD", "")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
