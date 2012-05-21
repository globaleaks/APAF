import unittest
import tempfile
import os.path
import shutil

from apaf import blobber
from apaf.config import config

class TestBlobber(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(suffix='apaf_blobbonetest')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_compacting(self):
        dest = os.path.join(self.tmpdir, 'burp.py')
        blobber.create_blobbone(config._data_dir, dest)

        self.assertTrue(os.path.exists(self.tmpdir))
        self.assertTrue(os.path.exists(dest))
        self.assertFalse(os.path.exists(
            os.path.join(self.tmpdir, os.path.split(config._data_dir)[1])))


    def test_uncompatting(self):
        pass

