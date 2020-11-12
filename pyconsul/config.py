import os

defaults = {
    'dry-run': False,
    'mount-point': None,
    'paths': ['.'],
    'token': None,
    'url': None,
    'verbosity': 2
}

class Base(object):
    def __init__(self):
        self._config = defaults

    def get_property(self, name):
        return self._config.get(name)

    def set_property(self, name, value):
        return self._config.setdefault(name, value)


class PyconsulConfig(Base):

    @property
    def dryrun(self):
        return self.get_property('dry-run')

    @dryrun.setter
    def dryrun(self, value):
        self.set_property('dry-run', value)

    @property
    def mount_point(self):
        return self.get_property('mount-point')

    @mount_point.setter
    def mount_point(self, value):
        if value is not None:
            self.set_property('mount-point', value)

    @property
    def paths(self):
        return self.get_property('paths')

    @paths.setter
    def paths(self, path_list):
        if path_list is not None:
            self.set_property('paths', path_list)

    @property
    def url(self):
        return self.get_property('url')

    @url.setter
    def url(self, url):
        if url is not None:
            self.set_property('url', url)

    @property
    def token(self):
        return self.get_property('token')
    
    @token.setter
    def token(self, value):
        if value is not None:
            self.set_property('token', value)
    
    @property
    def verbosity(self):
        return self.get_property('verbosity')

    @verbosity.setter
    def verbosity(self, value):
        if isinstance(value, int):
            self.set_property('verbosity', value)
