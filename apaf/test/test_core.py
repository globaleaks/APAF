import unittest

from apaf.core import Service

class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service()

    def test_attributes(self):
        attributes = ['port', 'name', 'desc', 'author', 'icon',
                      'onStart', 'onStop', 'onFailure']

        for attr in attributes:
            self.assertTrue(hasattr(self.service, attr),
                            msg='attribute "%s" not present' % attr)


if __name__ == '__main__':
    unittest.main()
