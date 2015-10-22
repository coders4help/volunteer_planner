# coding: utf-8

from volunteer_planner.settings.local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'volunteer',
        'HOST': '',
        'USER': 'postgres',
        'PASSWORD': '',
    }
}
