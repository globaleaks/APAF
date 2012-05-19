import unittest

from apaf.config import config

class TestConfig(unittest.TestCase):

    def fetch(self, name):
        """
        Return the value for name from the config class.
        """
        return getattr(config, name, None)

    def test_basic(self):
        """
        Assert that basic configuration bariables are present.
        """
        self.assertIsNotNone(self.fetch('platform'))
        self.assertIsNotNone(self.fetch('binary_kits'))
        self.assertIsNotNone(self.fetch('config_file'))

        self.assertIsNone(self.fetch('foobarbaz'))

if __name__ == '__main__':
    unittest.main()
