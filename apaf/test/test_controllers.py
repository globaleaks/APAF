from twisted.trial import unittest

import apaf
from apaf.panel import controllers
from apaf import config, testing
from apaf.run.base import main

class TestTorCtl(unittest.TestCase):
    def setUp(self):
        self.controller = controllers.TorCtl()

    def test_get(self):
       self.assertTrue(self.controller.get('version'))
       self.assertRaises(ValueError, self.controller.get, 'foobar')
    test_get.skip = 'Must start tor first'


class TestConfigCtl(unittest.TestCase):
    def setUp(self):
        self.controller = controllers.ConfigCtl()

    def test_get(self):
        cfg = self.controller.get()

        self.assertTrue(cfg)
        self.assertIn(config.custom['base_port'], cfg.values())
        self.assertNotIn('passwd', cfg)
        self.assertNotIn('cookie_secret', cfg)

class TestSservicesCtl(unittest.TestCase):
    def setUp(self):
        self.controller = controllers.ServicesCtl()
        testing.start_mock_apaf(tor=False)
        for service in apaf.hiddenservices:
            self.addCleanup(service.tcp.loseConnection)

    def test_get(self):
        self.assertTrue(self.controller.get(None))
        self.assertIn('panel',
                      [x['name'] for x in self.controller.get(None)])

    def test_get_config(self):
        self.assertIn('config',
                      self.controller.get('panel'))

    def test_get_invalid(self):
        self.assertRaises(ValueError, self.controller.get, 'invalidnamefooo')

