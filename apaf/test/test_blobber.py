import imp
import unittest
import tempfile
import os.path
import shutil

from apaf import blobber
from apaf.config import config

class TestBlobber(unittest.TestCase):
    filename = 'burp'

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(suffix='apaf_blobbonetest')
        self.dest = os.path.join(self.tmpdir, self.filename + '.py')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_compacting(self):
        blobber.create_blobbone(config._data_dir, self.dest)

        self.assertTrue(os.path.exists(self.tmpdir))
        self.assertTrue(os.path.exists(self.dest))
        self.assertFalse(os.path.exists(
            os.path.join(self.tmpdir, os.path.split(config._data_dir)[1])))

    def test_uncompatting(self):
        blobber.create_blobbone(config._data_dir, self.dest)
        imp.load_module(self.filename,
                        *imp.find_module(self.filename, [self.tmpdir])
)
