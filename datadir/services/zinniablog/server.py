import os
import sys

# Environment setup for your Django project files:
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'

from django.core.handlers.wsgi import WSGIHandler
from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor

import blog.settings

PORT = 8000



def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    # Allow Ctrl-C to get you out cleanly:
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource


class Root(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        print path, request.prepath, request.postpath
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource


class DjangoResource(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)

        pool = threadpool.ThreadPool()
        pool.start()
        # Allow Ctrl-C to get you out cleanly:
        reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
        self.wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())

        staticsrc = static.File(blog.settings.STATIC_ROOT, blog.settings.STATIC_URL)
        self.putChild('static', staticsrc)

    def getChild(self, path, request):
        print path, request.prepath, request.postpath
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource


# Twisted Application Framework setup:
application = service.Application('twisted-django')
# Serve it up:
main_site = server.Site(DjangoResource())
internet.TCPServer(PORT, main_site).setServiceParent(application)
