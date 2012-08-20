from hashlib import sha256
from functools import wraps
import sys

import txtorcon
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.python import log
from cyclone.escape import json_decode, json_encode

from apaf.panel import panel
from apaf.core import add_service
from apaf.testing import Page, json
from apaf import config

page = Page('127.0.0.1', 6660)
#log.startLogging(sys.stdout)   # debug information from the backend.


## monkeypatch standard login.
from apaf.panel import handlers
handlers.base.PanelHandler.get_current_user = lambda *args: True
##

class TestPanel(unittest.TestCase):

    def setUp(self):
        """
        Set up an asyncronous get trasport.
        """
        torconfig = txtorcon.TorConfig()
        self.service = panel.PanelService()

        # for simplicity, disable xrcf cookies
        self.service.factory.settings['xsrf_cookies'] = False

        add_service(torconfig, self.service, 6660)
        self.addCleanup(self.service.tcp.loseConnection)


class TestServices(TestPanel):
    """
    Test requests:
        * GET /services
        * GET /services/<name>/
        * GET /services/<name>/start
        * GET /services/<name>/stop
    """

    @page('/services/')
    @json
    def test_get_services(self, response):
        self.assertIn('panel', [x['name'] for x in response])

    @page('/services/panel')
    @json
    def test_get_services_panel(self, response):
        self.assertTrue(isinstance(response, dict))
        self.assertTrue(all(x in response for x in
                        ['name', 'url','desc']))

    @page('/services/panel/stop')
    @json
    def test_get_services_panel_stop(self, response):
        """
        Panel shall not be stoppped.
        """
        self.assertEquals(response, {'result':False})

    def test_get_services_mockpanel_stop(self):
        """
        Set up a mock service and tries to stop it.
        """

    @page('/services/almudena/start', raises=True)
    def test_get_services_notfound_stop(self, error):
        self.assertEquals(error.value.status, '404')



class TestConfig(TestPanel):
    """
    Test requests:
        * GET /config
        * PUT /config {settings:{something}}
    """
    @page('/config')
    @json
    def test_get_config(self, response):
        self.assertTrue(all(config.custom[key] == value
                            for key, value in response.iteritems()))

    @page('/config', method='PUT',
          headers={'settings': json_encode(dict(base_port=6666))})
    @json
    def test_put_config(self, response):
        self.assertEqual(response, {'result':True})

    @page('/config', method='PUT',
          headers={'settings': json_encode(dict(cheese='spam'))})
    @json
    def test_put_config_invalid_key(self, response):
        self.assertIn('error', response)

    @page('/config', method='PUT',
          headers={'settings': json_encode(dict(base_port='a string'))})
    @json
    def test_put_config_invalid_value(self, response):
        self.assertEqual(response, {'result':False})

class TestMiscellanous(TestPanel):
    """
    A collection of various tests concerning error handling in Panel.
    """
    @page('/foo/bar', raises=True)
    def test_notfound(self, error):
        self.assertEqual(error.value.status, '404')

    @page('/services/spamcheesefoobar', raises=True)
    def test_service_notfound(self, error):
        self.assertEqual(error.value.status, '404')

class TestAuth(TestPanel):
    """
    Tests requests:
        * POST /auth/login
        * GET /auth/logout
    """

    @page('/auth/login', raises=True)
    def test_get_auth_login(self, error):
        self.assertEqual(error.value.status, '404')

    @page('/auth/logout', raises=True, method='POST')
    def test_post_auth_logout(self, error):
        self.assertEqual(error.value.status, '404')

    @page('/auth/login', raises=True, method='POST',
          postdata=json_encode({'passwd':'1234'}))
    def test_post_auth_login_fail(self, error):
        self.assertEqual(error.value.status, '401')
    test_post_auth_login_fail.skip = ('Must test invalid password from the'
                                      'outside.')

    @page('/auth/login', method='POST',
          postdata=json_encode({'passwd':sha256('None').hexdigest()}))
    def test_post_auth_login(self, response):
        self.assertEqual(json_decode(response), {'result':True})



if __name__ == '__main__':
    from unittest import main
    main()
