import unittest
import tempfile
import os

from apaf import config

class TestConfig(unittest.TestCase):

    def fetch(self, name):
        """
        Return the value for name from the config class.
        """
        return getattr(config, name, None)

    def test_basic(self):
        """
        Assert that basic configuration variables are there.
        """
        self.assertIsNotNone(self.fetch('platform'))
        self.assertIsNotNone(self.fetch('binary_kits'))
        self.assertIsNotNone(self.fetch('config_file'))

        self.assertIsNone(self.fetch('foobarbaz'))

    def test_commit(self):
        config.config_file = tempfile.mktemp(suffix='apaf_cfg')

        config.custom.commit()
        self.assertTrue(os.path.exists(config.config_file))


    def test_setattr(self):
        try:
            config.custom.__foo_bar = 'spam'
            config.custom._foo = 1
        except ValueError:
            pass # as expected
        else:
            self.fail('Cannot set items from config.')

    def test_delattr(self):
        try:
            del config.custom.cheese_and_spam
        except AttributeError:
             pass  # as expected
        else:
            self.fail('Cannot delete items from config.')


if __name__ == '__main__':
    unittest.main()
