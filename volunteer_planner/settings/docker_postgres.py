# coding: utf-8

from volunteer_planner.settings.local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'volunteer_planner',
        'HOST': 'db',
        'USER': 'vp',
        'PASSWORD': 'volunteer_planner',
    }
}
