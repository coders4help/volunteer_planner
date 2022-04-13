import brace_format_logging
import os
import uuid

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.base import BaseEmailBackend

logger = brace_format_logging.getLogger(__name__)


class FileEmailBackend(BaseEmailBackend):
    def __init__(self, *args, file_path=None, **kwargs):
        # This __init__ is the same as in
        # django.core.mail.backends.filebased.EmailBackend.__init__
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = getattr(settings, "EMAIL_FILE_PATH", None)
        self.file_path = os.path.abspath(self.file_path)
        try:
            os.makedirs(self.file_path, exist_ok=True)
        except FileExistsError:
            raise ImproperlyConfigured(
                "Path for saving email messages exists, but is not a directory: %s"
                % self.file_path
            )
        except OSError as err:
            raise ImproperlyConfigured(
                "Could not create directory for saving email messages: %s (%s)"
                % (self.file_path, err)
            )
        # Make sure that self.file_path is writable.
        if not os.access(self.file_path, os.W_OK):
            raise ImproperlyConfigured(
                "Could not write to directory: %s" % self.file_path
            )
        super().__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        for msg in email_messages:
            message = msg.message()
            msgid = str(message.get("Message-ID", uuid.uuid4())).strip("<>")
            path = os.path.join(self.file_path, f"{msgid}.eml")
            with open(path, "w") as f:
                f.write(message.as_string())
                logger.info("Saved email at {path}", path=path)
