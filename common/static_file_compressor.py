import contextlib
import gzip
import io
import re
import shutil
from importlib import import_module

from django.contrib.staticfiles.storage import StaticFilesStorage


class CompressedStaticFilesStorage(StaticFilesStorage):
    EXTENSIONS = ["js", "css"]
    EXT_LOOKUP = {}

    def __init__(self, location=None, base_url=None, *args, **kwargs):
        super().__init__(location, base_url, *args, **kwargs)
        for ext in self.EXTENSIONS:
            self.EXT_LOOKUP[ext] = re.compile(r".*\.{}\Z".format(ext))

    def post_process(self, paths, dry_run=False, **kwargs):
        processing_files = []
        for name in paths:
            ext = self.filename_matches(name)
            if ext:
                processing_files.append((name, self.path(name), ext))

        for name, path, ext in processing_files:
            yield self._post_process(name, path, ext, dry_run)

    def _post_process(self, name, path, ext, dry_run):
        processed = False
        if dry_run:
            return name, path, False
        try:
            func_name = "_minify_{}".format(ext)
            func = getattr(self, func_name)
            if func:
                processed = func(path)
        except AttributeError:
            processed = False
        except io.UnsupportedOperation:
            # raise explicitly
            raise

        return name, path, processed

    def filename_matches(self, name):
        for ext in self.EXT_LOOKUP:
            regexp = self.EXT_LOOKUP[ext]
            if regexp.match(name):
                return ext

        return None

    @staticmethod
    def _minify_js(path):
        return __class__._generic_minify(path, "rjsmin", "jsmin")

    @staticmethod
    def _minify_css(path):
        return __class__._generic_minify(path, "rcssmin", "cssmin")

    @staticmethod
    def _generic_minify(path, module, func):
        try:
            f = getattr(import_module(module), func)
            with open(path) as f_in:
                file_content = f_in.read()
            with open(path, "w") as f_out:
                f_out.write(f(file_content))
            __class__._gzip(path)

            return True
        except Exception:
            return False

    @staticmethod
    def _gzip(path):
        with contextlib.suppress(Exception):  # noqa: SIM117
            with open(path, "rb") as f_in:  # noqa: SIM117
                with gzip.open(f"{path}.gz", "wb") as f_out:  # noqa: SIM117
                    shutil.copyfileobj(f_in, f_out)
