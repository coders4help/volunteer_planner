# coding: utf-8

from volunteer_planner.settings.local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'volunteer_planner',
        'PASSWORD': os.environ.get('DATABASE_PW', 'volunteer_planner'),
        'USER': os.environ.get('DB_USER', 'vp')
    }
}
