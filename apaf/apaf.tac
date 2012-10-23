from twisted.application import service, internet
from twisted.internet.endpoints import TCP4ClientEndpoint

import txtorcon
import sys

del sys.argv[1:]
# import main for correcting PYTHONPATH
import main
from apaf.run import base

port = 8888

application = service.Application("APAF Application")
torfactory = txtorcon.TorProtocolFactory()
connection_creator = TCP4ClientEndpoint(base.reactor, 'localhost', 9052).connect(torfactory)

service = internet.TCPServer(9051, torfactory)
service.setServiceParent(application)


base.main(connection_creator=connection_creator).addCallback(base.setup_complete)
