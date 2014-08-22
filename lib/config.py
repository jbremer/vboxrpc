from ConfigParser import ConfigParser
import os

_config = None


class Config(object):
    def __init__(self, path):
        self._d = {}

        self._c = ConfigParser()
        self._c.read(path)
        self._parse()

    def _process_value(self, value):
        if isinstance(value, str) and value.startswith('~'):
            return os.getenv('HOME') + value[1:]

        if value.lower() in ('true', 'on', 'yes', 'enable'):
            return True

        if value.lower() in ('false', 'off', 'no', 'disable'):
            return False

        return value

    def _parse(self):
        for s in self._c.sections():
            r = {}

            for k in self._c.options(s):
                r[k] = self._process_value(self._c.get(s, k))

            self._d[s] = r

    def __getattr__(self, key):
        return self._d[key]

    def __getitem__(self, key):
        return self._d[key]


def load_config(path):
    global _config
    _config = Config(path)['vboxrpc']


def config(key):
    return _config[key]
