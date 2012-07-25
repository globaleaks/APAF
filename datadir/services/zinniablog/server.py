import os
import os.path
import sys

from django.core.handlers.wsgi import WSGIHandler
from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor

import blog.settings
import apaf
from apaf import config
from apaf.core import Service

# Environment setup for your Django project files:
sys.path.append(os.path.join(config.services_dir, 'zinniablog'))

PORT = 8000
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'

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
        """
        Forward everything to the relative wsgi resource,
        and re-build the request with previously processed url.
        """
        request.postpath.insert(0, *request.prepath)
        return self.wsgi_resource

class ServiceDescriptor(Service):
    name = 'zinniablog'
    desc = 'A simple django blog created using zinnia'
    author = apaf.__author__
    port = 80
    icon = os.path.join(blog.settings.STATIC_ROOT,
                        'zinnia', 'img', 'favicon.ico')

    config = config.Config(
            config_file='blog.cfg',
            defaults={}
    )

    def get_factory(self):
       self.resource = DjangoResource()
       return server.Site(self.resource)



# Twisted Application Framework setup:
application = service.Application('twisted-django')
# Serve it up:
main_site = server.Site(DjangoResource())
internet.TCPServer(PORT, main_site).setServiceParent(application)
