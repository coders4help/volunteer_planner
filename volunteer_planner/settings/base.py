# coding: utf-8

"""
Django settings for a boilerplate project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os

from django.utils.translation import gettext_lazy as _

DEBUG = False
# PROJECT DIRECTORY AND GENERAL SETTINGS
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '..', '..'))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)
SITE_ID = 1
SITE_NAME = os.path.basename(PROJECT_ROOT)
ROOT_URLCONF = '%s.urls' % SITE_NAME
# END PROJECT DIRECTORY AND GENERAL SETTINGS


# SECURITY
ACCOUNT_ACTIVATION_DAYS = 3
# APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'djangocms_admin_style',
    # Admin panel and documentation:
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'ckeditor',
    # A prettier theme

    'accounts.apps.RegistrationConfig',
    'django_ajax',
    'django_extensions',
    'logentry_admin',
)

LOCAL_APPS = (
    'google_tools',
    'osm_tools',
    'accounts.apps.AccountsConfig',
    'organizations',
    'common',
    'scheduler',
    'blueprint',
    'shiftmailer',
    'places',
    'non_logged_in_area',
    'scheduletemplates',
    'news',
    'notifications',
    'content'
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATICFILES_DIRS = [
    os.path.join(SITE_ROOT, 'resources'),
]
STATICFILES_STORAGE = 'common.static_file_compressor.CompressedStaticFilesStorage'
MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates'),
                 os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'google_tools.context_processors.google_tools_config',
                'non_logged_in_area.context_processors.current_site',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            # if logging handlers above are added/edited, re-evaluate 'propagate'.
            # for now: don't propagate, because it sends every ERROR e-mail twice,
            # because 'django.request' and it's parent 'django' use 'mail_admins'.
            'propagate': False,
        },
    }
}
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'en'
USE_L10N = True
LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('fr', _('French')),
    ('el', _('Greek')),
    ('hu', _('Hungarian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('ru', _('Russian')),
    ('sv', _('Swedish')),
    ('tr', _('Turkish'))
)

LOCALE_PATHS = (
    SITE_ROOT + '/locale',
)

WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
)
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"

DATE_FORMAT = "l, d.m.Y"

INCLUDE_REGISTER_URL = True
INCLUDE_AUTH_URLS = True
REGISTRATION_FORM = "registration.forms.RegistrationFormUniqueEmail"
