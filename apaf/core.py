"""
Services logic.
"""
import imp
import os.path

from twisted.python import log
from twisted.internet import reactor, error
from zope.interface import Interface, Attribute, implements
import txtorcon

import apaf
from apaf import config

class IService(Interface):
    """
    A Service class exposes callback methods and information to the apaf
    environment system, which takes care to load them.
    """
    name = Attribute('Name of the hidden service')
    desc = Attribute('A brief description of the service.')
    author = Attribute('The author of the service')
    port = Attribute('the port og which the service wants to be exposed')
    icon = Attribute('The service logo')

    hs = Attribute('A txtorcon.HiddenService isntance automagically binded to'
                   ' the service class from the apaf.')
    tcp = Attribute('A twisted.internet.tcp.Port instance, reflecting the port'
                    ' on which the service is listening to')
    factory = Attribute('A twisted.internet.protocol.Factory instance running'
                         ' the service.')

    def get_factory(self):
        """
        Called before starting the hidden service.
        :ret : a twisted.internet.protocol.Factory instance,
               which will be usd for starting the service.
        """

    def start(self):
        """
        Callback: called after the hiddenservice starts/resumes.
        """

    def stop(self):
        """
        Callback: called in case of explicit stop from the user.
        """

    def failure(self, exception):
        """
        Callback: called in case of exception.
        :param exception: The instance of the exception raised.
        :ret: None.
        """


class Service(object):
    implements(IService)

    name = 'Unknown'
    desc = ''
    author = ''
    icon = None
    port = None
    tcp = None

    def __init__(self):
        self._factory = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Service class on hiddenservice %s>' % self.hs

    def __nonzero__(self):
        # XXX. return always True.
        return True

    @property
    def url(self):
        """
        Return the hidden service url on which the service can be reached.
        """
        return self.hs.hostname

    @property
    def factory(self):
        if self._factory is None:
            self._factory = self.get_factory()
        return self._factory

    def get_factory(self):
        raise NotImplementedError

    def failure(self, exc):
        log.err(str(exc))

    def stop(self):
        return self.tcp.stopListening()

    def start(self):
        self.upd.startListening()

def new_port():
    """
    Generates a new port.
    :ret : an integer between config.base_port and 9999.
    """
    from Crypto import Random
    n = sum(map(ord, Random.get_random_bytes(10))) % (
         9999 - config.custom['base_port'])

    return config.custom['base_port'] + n

def add_service(torconfig, service, port=None):
    """
    Create a new hiddenservice and adds it to the `hiddenservices` list.
    : param service : the service to be run.
    """
    # picks a random port until it finds one avaible.
    while not service.tcp:
        port = port or new_port()
        try:
            service.tcp = reactor.listenTCP(port, service.factory)
        except error.CannotListenError:
            pass

    service.hs = txtorcon.HiddenService(
        torconfig, os.path.join(config.tor_data, service.name),
        ['%d 127.0.0.1:%d' % (service.port, port)])
    apaf.hiddenservices.append(service)

def start_services(torconfig):
    """
    For each service active in the configuration xand avaible in the
    `services/` directory, launch it.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """
    for service in config.custom['services']:
        # load service
        try:
            service_mod = imp.load_module(
                    service, *imp.find_module(service, [config.services_dir]))
        except ImportError:
            return log.err('Cannot import service %s' % service)
        except Exception as e:
            return log.err('Error loading service %s -\n %s' % (service, e))

        service = getattr(service_mod, 'ServiceDescriptor', None)
        if not service:
            log.err('Unable to find class Service in ', repr(service_mod))
            continue

        # create hidden service
        add_service(torconfig, service())
