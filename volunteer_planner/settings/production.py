# coding=utf-8
from .base import *
from datetime import timedelta

DEBUG = os.environ.get('BETA', False)

STATIC_ROOT = os.environ['STATIC_ROOT']


# Let this be done by frontend reverse proxy, if required!
PREPEND_WWW = False

ADMINS = (
    ('VP Admin', 'vp-admin@volunteer-planner.org'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DATABASE_NAME'],
        'PASSWORD': os.environ['DATABASE_PW'],
        'USER': os.environ['DATABASE_USER']
    }
}

ALLOWED_HOSTS = ['volunteer-planner.org', 'www.volunteer-planner.org']
SECRET_KEY = os.environ['SECRET_KEY']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
COMMUNICATION_SENDER_MAIL = 'noreply@volunteer-planner.org'
DEFAULT_FROM_EMAIL = 'noreply@volunteer-planner.org'
CONTACT_MAIL = ['noreply@volunteer-planner.org']
SERVER_EMAIL = 'noreply@volunteer-planner.org'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

GOOGLE_SITE_VERIFICATION = '-BN1vuSIqe1vJNe8hS5_6iLvtpJrefGpMIAA1ogCoLQ'
GOOGLE_ANALYTICS_TRACKING_ID = 'UA-66642441-1'

DEFAULT_SHIFT_CONFLICT_GRACE = timedelta(hours=1)
