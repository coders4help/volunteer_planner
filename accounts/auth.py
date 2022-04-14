import logging

from django.contrib.auth.backends import ModelBackend, UserModel

logger = logging.getLogger(__name__)


class EmailAsUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and "@" in username:
            try:
                user = UserModel._default_manager.get(email__iexact=username)
                return super().authenticate(request, user.username, password, **kwargs)
            except UserModel.DoesNotExist:
                logger.debug('No user with e-mail address "%s"', username)
            except UserModel.MultipleObjectsReturned:
                logger.warning(
                    'Found %s users with e-mail address "%s"',
                    UserModel._default_manager.filter(email=username).count(),
                    username,
                )
        return None
