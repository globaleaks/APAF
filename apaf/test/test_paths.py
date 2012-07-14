import os
import os.path

from twisted.trial import unittest

from apaf import config

class TestPaths(unittest.TestCase):
    def is_path(self, path):
        """
        Return True if the argument appears as a path, False otherwise.
        """
        return isinstance(path, str) and os.sep in path

    def test_pathexists(self):
        for name, path in vars(config).items():
            if not self.is_path(path): continue
            if path.endswith('cfg') or path.endswith('log'): continue
            self.assertTrue(os.path.exists(path),
                            msg='config.%s : not found path %s' % (name, path))


