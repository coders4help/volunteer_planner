from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'volunteer_planner',
        'PASSWORD': os.environ['DATABASE_PW'],
        'USER': os.environ['DB_USER']
    }
}

INSTALLED_APPS += ('debug_toolbar',
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
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
COMMUNICATION_SENDER_MAIL = 'noreply@noreply.de'
DEFAULT_FROM_EMAIL = 'cantzen@googlemail.com'

CONTACT_MAIL = os.environ['EMAIL_ADDRESS']
SERVER_EMAIL = os.environ['EMAIL_ADDRESS']
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_ADDRESS']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
SECRET_KEY = os.environ['SECRET_KEY']
