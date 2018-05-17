# coding=utf-8
from .base import *
from datetime import timedelta

DEBUG = os.environ.get('BETA', False)

STATIC_ROOT = os.environ['STATIC_ROOT']


# Let this be done by frontend reverse proxy, if required!
PREPEND_WWW = False

ADMINS = (
    ('VP Admin', os.environ['ADMIN_EMAIL']),
)

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.mysql'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'NAME': os.environ['DATABASE_NAME'],
        'PASSWORD': os.environ['DATABASE_PW'],
        'USER': os.environ['DATABASE_USER']
    }
}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'volunteer-planner.org,www.volunteer-planner.org').split()
SECRET_KEY = os.environ['SECRET_KEY']
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
COMMUNICATION_SENDER_MAIL = os.environ['SENDER_EMAIL']
DEFAULT_FROM_EMAIL = os.environ['FROM_EMAIL']
CONTACT_MAIL = [os.environ['CONTACT_EMAIL']]
SERVER_EMAIL = os.environ['SERVER_EMAIL']
EMAIL_HOST = os.environ.get('SMTP_HOST', 'localhost')
EMAIL_PORT = os.environ.get('SMTP_PORT', 25)
EMAIL_USER = os.environ.get('SMTP_USER', None)
EMAIL_PASS = os.environ.get('SMTP_PASS', None)
EMAIL_USE_TLS = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DEFAULT_SHIFT_CONFLICT_GRACE = timedelta(hours=1)
