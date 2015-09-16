# coding: utf-8

from django.conf import settings

from common.conf_loader import ConfLoader


def google_tools_config(request):
    config = ConfLoader(settings, raise_missing=False)

    google_tools = dict()

    if config.GOOGLE_SITE_VERIFICATION:  # and not settings.DEBUG:
        google_tools['site_verification'] = config.GOOGLE_SITE_VERIFICATION

    if config.GOOGLE_ANALYTICS_TRACKING_ID:  # and not settings.DEBUG:
        google_tools['analytics'] = {
            'tracking_id': config.GOOGLE_ANALYTICS_TRACKING_ID,
            'domain': config.GOOGLE_ANALYTICS_DOMAIN
        }

    return dict(google_tools=google_tools)
