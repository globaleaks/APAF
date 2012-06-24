import unittest

from apaf.core import Service

class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service()

    def test_metadata(self):
        attributes = ['port', 'name', 'desc', 'author', 'icon']

        for attr in attributes:
            self.assertTrue(hasattr(self.service, attr),
                            msg='attribute "%s" not present' % attr)

    def test_base(self):
        """
        Some fucntions MUST be reimplemented from the service.
        """
        self.assertRaises(NotImplementedError, self.service.get_factory)
        self.assertRaises(NotImplementedError, self.service.failure, None)


if __name__ == '__main__':
    unittest.main()
