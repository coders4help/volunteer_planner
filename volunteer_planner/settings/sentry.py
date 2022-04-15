"""
Imports and initializes sentry for usage within this Django instance.

For successful initialization 'sentry-sdk' needs to be installed and some
environment variables need to be present/set:
- SENTRY_DSN: sentry data source name (https://docs.sentry.io/product/sentry-basics/dsn-explainer/)  # noqa: E501
              mandatory, without no initialization will be successfully finished.
- SENTRY_ENVIRON: string, used as 'environment' tag value
                  default: 'production'
- SENTRY_TRACE_RATE: float, (0..1), probability a transaction is performance monitored
                     default: 0.0
- SENTRY_SEND_PII: bool, (https://docs.sentry.io/platforms/python/configuration/options/#send-default-pii)  # noqa: 501
                   default: False
"""
import logging
import os
from distutils.util import strtobool

from .base import VERSION

logger = logging.getLogger(__name__)

try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    def before_send(event, hint):
        user_info = event.get("user")
        if user_info:
            user_info.pop("email", None)
            user_info.pop("username", None)
        return event

    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        environment=os.environ.get("SENTRY_ENVIRON", "production"),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
        traces_sample_rate=float(os.environ.get("SENTRY_TRACE_RATE", "0.0")),
        # TODO think - really, I'm serious! - about some good 'traces_sampler'
        #  implementation and replace 'traces_sample_rate'
        send_default_pii=strtobool(os.environ.get("SENTRY_SEND_PII", "False")),
        before_send=before_send,
        release=VERSION,
    )
except (ImportError):
    logger.warning("sentry not installed - skipping", exc_info=True)
except (KeyError, NameError, ValueError):
    logger.debug("sentry not initialized", exc_info=True)
