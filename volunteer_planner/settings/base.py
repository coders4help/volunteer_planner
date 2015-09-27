# coding: utf-8

"""
Django settings for a boilerplate project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os

from django.utils.translation import ugettext_lazy as _

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
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Bootstrap for admin
    'django_admin_bootstrapped',
    # A prettier theme
    'djangocms_admin_style',
    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    # For markdown input in helptype description
    'django_bootstrap_markdown',
)

LOCAL_APPS = (
    'google_tools',
    'accounts',
    'common',
    'registration',
    'scheduler',
    'blueprint',
    'notifications',
    'ckeditor',
    'shiftmailer',
    'stats'
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.normpath(os.path.join(PROJECT_ROOT, 'static'))

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'google_tools.context_processors.google_tools_config'
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
            'propagate': True,
        },
    }
}
LOGIN_REDIRECT_URL = '/helpdesk/'
LOGIN_URL = '/auth/login/'

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'en'
USE_L10N = True
LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
    ('hu', _('Hungarian')),
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
