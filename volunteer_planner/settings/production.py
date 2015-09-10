from .base import *

DEBUG = False

TEMPLATE_DEBUG = False

STATIC_ROOT = '/var/www/volunteer/static'

TEMPLATE_LOADERS = (
    (
        'django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    ),
)
PREPEND_WWW = True

ADMINS = (
    ('Dorian Cantzen', 'cantzen@googlemail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DATABASE_NAME'],
        'PASSWORD': os.environ['DATABASE_PW'],
        'USER': os.environ['DATABASE_NAME']
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
# ssd
