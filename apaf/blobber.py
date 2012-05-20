#!/usr/bin/env python

import os
import tarfile
import base64
import sys

directory = os.path.expanduser(sys.argv[1])
tmp_tar = 'blobbone.tar.gz'

tar = tarfile.open(tmp_tar, 'w:gz')
tar.add(directory)
tar.close()

header_code = """import tarfile, base64, os
"""
uncompacting_code = """
f1 = open('blobbone.tmp', 'w')
f2 = open('blobbone.tar.gz', 'w')
f1.write(blob)
f1.close()
f1 = open('blobbone.tmp')
base64.decode(f1, f2)
f2.close()
f1.close()
tar = tarfile.open('blobbone.tar.gz', 'r:gz')
tar.extractall()
tar.close()
os.remove('blobbone.tmp')
os.remove('blobbone.tar.gz')
"""

f1 = open(tmp_tar)
f2 = open('blobbone.py', 'wb')
f2.write(header_code)
f2.write('blob = r"""')
base64.encode(f1, f2)
f2.write('"""\n')
f2.write(uncompacting_code)
f1.close()
f2.close()
os.remove(tmp_tar)

