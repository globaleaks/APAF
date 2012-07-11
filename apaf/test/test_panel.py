from functools import partial, wraps
from hashlib import sha256

import txtorcon
from twisted.trial import unittest
from twisted.internet import reactor
from twisted.web import client
from twisted.internet import tcp
from twisted.python import log
from cyclone.escape import json_decode, json_encode

from apaf.panel import panel
from apaf.core import add_service
from apaf import config

def page(path, raises=False, **settings):
    """
    Decorator helper for unittest.
    Uses asyncronous callbacks from twisted to get the page referred with path,
    and then tests it with the given path.
    """
    url =  'http://127.0.0.1:%d%s' % (6660, path)

    def inner(func):
        @wraps(func)
        def wrap(self):
            d = client.getPage(url, **settings)
            if raises:
                d.addErrback(partial(func, self))
            else:
                d.addCallback(partial(func, self))
            return d
        return wrap
    return inner


class TestPanel(unittest.TestCase):
    def setUp(self):
        """
        Set up an asyncronous get trasport.
        """
        torconfig = txtorcon.TorConfig()
        self.service = panel.PanelService()
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
    def test_get_services(self, response):
        self.assertTrue(response)
        # response = json_decode(response)   ## Why return strings? T_T
        self.assertIn('panel', json_decode(response))

    @page('/services/panel')
    def test_get_services_panel(self, response):
        self.assertTrue(response)
        response = json_decode(response)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue(all(x in response for x in
                        ['name', 'url','desc']))

    @page('/services/panel/stop')
    def test_get_services_panel_stop(self, response):
        """
        Panel shall not be stoppped.
        """
        self.assertEquals(json_decode(response), {'result':False})

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
    def test_get_config(self, response):
        self.assertTrue(response)
        response = json_decode(response)
        self.assertTrue(all(config.custom[key] == value
                            for key, value in response.iteritems()))

    @page('/config', method='PUT',
          headers={'settings': json_encode(dict(base_port=6666))})
    def test_put_config(self, response):
        self.assertTrue(response)
        self.assertEqual(json_decode(response), {'result':True})

    @page('/config', method='PUT',
          headers={'settings': json_encode(dict(cheese='spam'))})
    def test_put_config_invalid_key(self, response):
        self.assertTrue(response)
        self.assertIn('error', response)

    @page('/config', method='PUT',
          headers={'settings': json_encode(dict(base_port='a string'))})
    def test_put_config_invalid_value(self, response):
        self.assertTrue(response)
        self.assertIn('error', response)


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
        print error.value

    @page('/auth/login', method='POST',
          postdata=json_encode({'passwd':sha256('None').hexdigest()}))
    def test_post_auth_login(self, response):
        self.assertEqual(json_decode(response), {'result':True})

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


if __name__ == '__main__':
    from unittest import main
    main()
