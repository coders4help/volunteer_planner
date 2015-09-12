from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions'
)

# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
# END CACHE CONFIGURATION

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = os.environ.get('EMAIL_ADDRESS', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    COMMUNICATION_SENDER_MAIL = 'noreply@noreply.de'
    DEFAULT_FROM_EMAIL = 'cantzen@googlemail.com'
    CONTACT_MAIL = os.environ['EMAIL_ADDRESS']
    SERVER_EMAIL = os.environ['EMAIL_ADDRESS']

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'local')
