from twisted.internet import reactor
from twisted.web import server, resource, static
from twisted.python import log
import os

from handlers import TorHandler, AppHandler, StatusHandler

LISTEN_PORT = 4242
STATIC_DIR = os.path.join('apaf', 'panel', 'static')

API = {
    'tor': TorHandler,
    'app': AppHandler,
    'status': StatusHandler
}

def run():
    root = static.File(STATIC_DIR)

    for path, handler in API.items():
        root.putChild(path, handler())
    print "Listening on port %s" % LISTEN_PORT
    reactor.listenTCP(LISTEN_PORT, server.Site(root))


if __name__ == '__main__':
    run()
    reactor.run()

