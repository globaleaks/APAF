"""
Services logic.
"""
import imp

from twisted.python import log
import txtorcon

import apaf
from apaf.config import config

class Service(object):
    """
    A Service class exposes callback methods and information to the apaf
    environment system, which takes care to load them.
    """

    @property
    def name(self):
        """
        Name of the hidden service Must be the same as the module name.
        """
        raise NotImplementedError('Name not defined.')

    @property
    def desc(self):
        """
        A brief description of the service.
        """
        raise NotImplementedError('Name not defined.')

    @property
    def author(self):
        """
        The author of the service.
        """
        raise NotImplementedError('Desc not defined.')

    @property
    def port(self):
        """
        The port on which the service wants to be exposed.
        """
        raise NotImplementedError('Author not defined.')

    def onStart(self):
        """
        Called before starting the hidden service.
        """
        pass

    def onStop(self):
        """
        Called in case of explicit stop from the user.
        """
        pass

    def onFailure(self, exception):
        """
        Called in case of exception.
        :param exception: The instance of the exception raised.
        :ret: None.
        """
        pass

def start_services(torconfig):
    """
    For each service active in the configuration xand avaible in the
    `services/` directory, launch it.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """
    for port, service in enumerate(config.services):
        # load service
        try:
            service_mod = imp.load_module(service,
                                        *imp.find_module(service, ['services']))
        except ImportError:
            log.err('Cannot import service %s' % service)
        except Exception as e:
            log.err('Error loading service %s -\n %s' % (service, e))

        # create hidden service

        service_hs = txtorcon.HiddenService(
                torconfig, join(config.tor_data, service),
                ['%d 127.0.0.1:%d' % (config.panel_port+port, )])
        apaf.hiddenservices[service]

