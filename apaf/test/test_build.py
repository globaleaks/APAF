import unittest

from apaf import build

class TestDownlaoder(unittest.TestCase):
    def test_torbuild(self):
        self.assertIsNotNone(getattr(build, 'tor', None))


