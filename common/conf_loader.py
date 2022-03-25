# coding: utf-8
import os


# TODO: tests & docstring
class ConfLoader(object):
    class ConfigNotFound(Exception):
        def __init__(self, key):
            self.key = key

        @property
        def message(self):
            return "ConfigNotFound: {}".format(self.key)

    def __init__(
        self, settings=None, env_fmt=None, env=True, raise_missing=True, **defaults
    ):
        self._defaults = defaults or {}
        self.env = env
        self.env_fmt = env_fmt or "{}"
        self.raise_missing = raise_missing
        self.settings = settings

    def _get_from_env(self, key):
        env_key = self.env_fmt.format(key)
        return os.environ.get(env_key, None)

    # TODO: caching?
    def __getitem__(self, item):
        try:
            if self.settings and hasattr(self.settings, item):
                return getattr(self.settings, item)
            elif self.env:
                env_value = self._get_from_env(item)
                if env_value is not None:
                    return env_value
            return self._defaults[item]
        except KeyError:
            if self.raise_missing:
                raise ConfLoader.ConfigNotFound(item)
        return None

    def __getattr__(self, key):
        return self[key]
