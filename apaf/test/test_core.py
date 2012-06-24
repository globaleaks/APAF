from twisted.trial import unittest

from apaf import core

class TestService(unittest.TestCase):
    def setUp(self):
        self.service = core.Service()

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

    def test_newport(self):
        """
        Assert new ports are not so trivial.
        """
        self.assertNotEqual(core.new_port(), core.new_port())
    test_newport.skip = 'Not implemented'



if __name__ == '__main__':
    from unittest import main
    main()
