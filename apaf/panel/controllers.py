"""
Panel Controllers:
    intermediates between APAF's internal logic and the html views.

    Controller classes are usually composed of two methods, enjoying ducktyping:
    #. ```set(self, name[s])``` => setting items, should return a boolean object.
    #. ```get(self, name[s])``` => retriving items, should return a
                                   dictionary-like object
"""
from apaf import config

class TorCtlController(object):
    allowed = (
            'version', 'ns/all', 'status/bootstrap-phase',

    )

    def get(self, name):
        raise NotImplementedError


class ConfigCtl(object):
    hidden = ('cookie_secret', 'passwd')

    def get(self):
        return dict((key, value) for key, value in config.custom
                    if key not in self.hidden)

    def set(self, args):
        """
        Processes a dictionary key:value, and put it on the configuration file.
        :param cfg: A dictionary-like object with the configuration updates.
        """
        if not all(x in config.custom and x not in self.hidden for x in args):
            raise ValueError('Invalid configuration parameters')

        try:
            for key, value in settings.iteritems():
                config.custom[key] = value
            return True
        except KeyError or TypeError:
            return False

