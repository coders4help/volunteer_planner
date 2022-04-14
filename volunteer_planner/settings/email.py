import os
from datetime import timedelta
from distutils.util import strtobool

from django.core.mail import DNS_NAME


# The actual backend is defined in BACKENDS in POST_OFFICE.
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", "post_office.EmailBackend")


# Default e-mail address to use for various automated correspondence from the site
# manager(s). This doesn’t include error messages sent to ADMINS and MANAGERS; for that,
# see SERVER_EMAIL.
# Default: 'webmaster@localhost'
if "FROM_EMAIL" in os.environ or "DJANGO_FROM_EMAIL" in os.environ:
    DEFAULT_FROM_EMAIL = os.environ.get(
        "DJANGO_FROM_EMAIL", os.environ.get("FROM_EMAIL", "hallo@volunteer-planner.org")
    )


# The e-mail address that error messages come from, such as those sent to ADMINS and
# MANAGERS.
# Default: 'root@localhost'
if "SERVER_EMAIL" in os.environ or "DJANGO_SERVER_EMAIL" in os.environ:
    SERVER_EMAIL = os.environ.get(
        "DJANGO_SERVER_EMAIL",
        os.environ.get("SERVER_EMAIL", "admin@volunteer-planner.org"),
    )


# The host to use for sending email.
# Default: "localhost"
if "SMTP_HOST" in os.environ or "DJANGO_EMAIL_HOST" in os.environ:
    EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", os.environ.get("SMTP_HOST"))


# Port to use for the SMTP server defined in EMAIL_HOST.
# Default: 25
if "SMTP_PORT" in os.environ or "DJANGO_EMAIL_PORT" in os.environ:
    EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", os.environ.get("SMTP_PORT")))


# Username to use for the SMTP server defined in EMAIL_HOST. If empty, Django won’t
# attempt authentication.
# Default: "" (Empty string)
if "SMTP_USER" in os.environ or "DJANGO_EMAIL_HOST_USER" in os.environ:
    EMAIL_HOST_USER = os.environ.get(
        "DJANGO_EMAIL_HOST_USER", os.environ.get("SMTP_USER")
    )


# Password to use for the SMTP server defined in EMAIL_HOST. This setting is used in
# conjunction with EMAIL_HOST_USER when authenticating to the SMTP server. If either of
# these settings is empty, Django won’t attempt authentication.
# Default: "" (Empty string)
if "SMTP_PASS" in os.environ or "DJANGO_EMAIL_HOST_PASSWORD" in os.environ:
    EMAIL_HOST_PASSWORD = os.environ.get(
        "DJANGO_EMAIL_HOST_PASSWORD", os.environ.get("SMTP_PASS")
    )


# Whether to use a TLS (secure) connection when talking to the SMTP server. This is
# used for explicit TLS connections, generally on port 587. If you are experiencing
# hanging connections, see the implicit TLS setting EMAIL_USE_SSL.
# Default: False
if "DJANGO_EMAIL_USE_TLS" in os.environ:
    EMAIL_USE_TLS = strtobool(str(os.environ.get("DJANGO_EMAIL_USE_TLS")))


# The directory used by the file email backend to store output files.
# Default: Not defined
if "DJANGO_EMAIL_FILE_PATH" in os.environ:
    EMAIL_FILE_PATH = os.environ.get("DJANGO_EMAIL_FILE_PATH")


# Settings for django-post-office async email backend.
# see https://github.com/ui/django-post_office
POST_OFFICE = {
    "BACKENDS": {
        "default": os.environ.get(
            "POST_OFFICE_EMAIL_BACKEND",
            "django.core.mail.backends.console.EmailBackend",
        )
    },
    "BATCH_SIZE": int(os.environ.get("POST_OFFICE_BATCH_SIZE", 100)),
    "CELERY_ENABLED": False,
    "DEFAULT_PRIORITY": "medium",
    "LOG_LEVEL": int(os.environ.get("POST_OFFICE_LOG_LEVEL", 2)),
    "MAX_RETRIES": int(os.environ.get("POST_OFFICE_MAX_RETRIES", 0)),
    "MESSAGE_ID_ENABLED": False,
    "MESSAGE_ID_FQDN": DNS_NAME,
    "OVERRIDE_RECIPIENTS": None,
    "RETRY_INTERVAL": timedelta(
        minutes=int(os.environ.get("POST_OFFICE_RETRY_INTERVAL", 15))
    ),
    "SENDING_ORDER": ["-priority"],
    "TEMPLATE_ENGINE": "django",
    "THREADS_PER_PROCESS": int(os.environ.get("POST_OFFICE_THREADS_PER_PROCESS", 5)),
}
