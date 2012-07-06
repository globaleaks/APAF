import unittest
import tempfile
import os

from apaf import config

## change default configutation file


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
        config.custom.commit()
        self.assertTrue(os.path.exists(config.config_file))
        config.custom['services'] = []
        config.custom.commit()
        self.assertTrue(os.path.exists(config.config_file))
        self.assertEqual(config.custom['services'], [])


    def test_setitem(self):
        def setitem(obj, key, value):
            obj[key] = value

        self.assertRaises(KeyError,  setitem, config.custom, 'foobar', None)
        self.assertRaises(TypeError, setitem, config.custom, 'services', '')

    def test_delattr(self):
        try:
            del config.custom.cheese_and_spam
        except AttributeError:
             pass  # as expected
        else:
            self.fail('Cannot delete items from config.')


if __name__ == '__main__':
    unittest.main()
