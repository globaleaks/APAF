"""
Panel Controllers:
    intermediates between APAF's internal logic and the html views.

    Controller classes are usually composed of two methods, enjoying ducktyping:
    #. ```set(self, name[s])``` => setting items, should return a boolean object.
    #. ```get(self, name[s])``` => retriving items, should return a
                                   dictionary-like object
"""
import apaf
from apaf import config

class TorCtl(object):
    allowed = (
            'version', 'ns/all', 'status/bootstrap-phase',
    )

    def get(self, sp_keyword):
        if not apaf.torctl:
            raise RuntimeError('Tor is not yet started')

        if sp_keyword not in self.allowed:
            raise ValueError
        try:
            apaf.torctl.get_info(sp_keyword)
        except torcontrolprotocol.TorProtocolError as err:
            if err.code == 552:
                raise ValueError
            else:
                raise KeyError('%s (code %d)' % (err.text, err.code))


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
            for key, value in args.iteritems():
                config.custom[key] = value
            return True
        except KeyError:
            return False
        except TypeError:
            return False


class ServicesCtl(object):
    keys = ['name', 'desc', 'url', 'active']

    @property
    def services(self):
        """
        Return a dictionary service-name:service-class of all instantiated
        services.
        """
        return dict((service.name, service) for service in apaf.hiddenservices)

   # cache decorator here.
    def _get_service(self, name):
        if not name in self.services:
            raise ValueError('Not found')
        else:
            return self.services[name]

    def get(self, service, _base=True):
        if not service:
            return [self.get(service) for service in self.services.keys()]
        else:
            service = self._get_service(service)
            return dict((name, getattr(service, name, None)) for name in self.keys)

    def set(self, service, state):
        service = self._get_service(service)
        if service.name == 'panel': ##panel.PanelService.name:
            return False

        if state is False:
            return service.stop()
        if state is True:
            return service.start()

