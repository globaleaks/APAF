import functools
import sys

import txtorcon
from zope.interface import implements
from twisted.application import service, internet
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.scripts.twistd import run
from twisted.python import log


# import main for correcting PYTHONPATH
import main
from apaf.run import base

class TorService(service.Service):
    implements(service.IService)

    def __init__(self):
        self.torfactory = txtorcon.TorProtocolFactory()
        self.connection = TCP4ClientEndpoint(base.reactor, 'localhost', 9052)
        self._port = None

    def startService(self):
       service.Service.startService(self)
       if self._port is None:
           self._port = base.main(connection_creator=functools.partial(
               self.connection.connect, self.torfactory))

application = service.Application("APAF Application")
torservice = TorService()
torservice.setServiceParent(application)

