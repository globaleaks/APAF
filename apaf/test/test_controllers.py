from twisted.trial import unittest

from apaf.panel import controllers
from apaf import config
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
