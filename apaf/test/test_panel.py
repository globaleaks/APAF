from twisted.trial import unittest
from twisted.internet import reactor
from twisted.web import client
from twisted.internet import tcp
import txtorcon

from apaf.panel import panel
from apaf.core import add_service
from apaf import config

def page(path, **settings):
    url =  'http://127.0.0.1:%d/%s' % (6660, path)
    def inner(func):
        def wrap(self):
            d = client.getPage(url, **settings)
            d.addCallback(func, self)
            return d
        return wrap
    return inner

class TestPanel(unittest.TestCase):
    def setUp(self):
        """
        Set up an asyncronous get trasport.
        """
        torconfig = txtorcon.TorConfig()
        self.prot = add_service(torconfig, panel.PanelService(), 6660)
        self.addCleanup(self.prot.loseConnection)

    @page('services')
    def test_get_services(self, response):
        print response



if __name__ == '__main__':
    unittest.main()
