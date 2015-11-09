# coding: utf-8

from volunteer_planner.settings.local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'volunteer_planner'),
        'PASSWORD': os.environ.get('DATABASE_PW', 'volunteer_planner'),
        'USER': os.environ.get('DB_USER', 'vp'),
    }
}
