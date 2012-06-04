"""
Services logic.
"""
import imp
import os.path

from twisted.python import log
from zope.interface import Interface, Attribute, implements
import txtorcon

import apaf
from apaf.config import config

class IService(Interface):
    """
    A Service class exposes callback methods and information to the apaf
    environment system, which takes care to load them.
    """
    name = Attribute('Name of the hidden service')
    desc = Attribute('A brief description of the service.')
    author = Attribute('The author of the service')
    port = Attribute('the port og which the service wants to be exposed')
    hs = Attribute('A txtorcon.HiddenService isntance automagically binded to'
                   ' the service class from the apaf.')

    icon = Attribute('The service logo')

    def onStart(self):
        """
        Called before starting the hidden service.
        """

    def onStop(self):
        """
        Called in case of explicit stop from the user.
        """

    def onFailure(self, exception):
        """
        Called in case of exception.
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
    hs = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Service class on hiddenservice %s>' % self.hs

    def __nonzero__(self):
        # XXX. return always True.
        return True

def add_service(torconfig, service, port=None):
    """
    Create a new hiddenservice and adds it to the `hiddenservices` list.
    : param service : the service to be run.
    """
    port = port or config.base_port + len(apaf.hiddenservices)

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
    for port, service in enumerate(config.services):
        # load service
        try:
            service_mod = imp.load_module(
                    service, *imp.find_module(config.service_dir, ['services']))
        except ImportError:
            log.err('Cannot import service %s' % service)
        except Exception as e:
            log.err('Error loading service %s -\n %s' % (service, e))

        service = getattr(service_mod, 'ServiceDescriptor', None)
        if not service:
            log.err('Unable to find class Service in ', repr(service_mod))
            continue

        # create hidden service
        add_service(torconfig, service)
