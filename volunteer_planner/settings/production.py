# coding=utf-8
from .base import *
from datetime import timedelta

DEBUG = os.environ.get('BETA', False)

STATIC_ROOT = os.environ['STATIC_ROOT']


# Let this be done by frontend reverse proxy, if required!
PREPEND_WWW = False

ADMINS = (
    ('VP Admin', os.environ.get('ADMIN_EMAIL', None)),
)

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.mysql'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'NAME': os.environ.get('DATABASE_NAME', None),
        'PASSWORD': os.environ.get('DATABASE_PW', None),
        'USER': os.environ.get('DATABASE_USER', None)
    }
}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'volunteer-planner.org,www.volunteer-planner.org').split()
SECRET_KEY = os.environ['SECRET_KEY']
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
COMMUNICATION_SENDER_MAIL = os.environ.get('SENDER_EMAIL', None)
DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL', None),
CONTACT_MAIL = [os.environ.get('CONTACT_EMAIL', None)],
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', None)
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
