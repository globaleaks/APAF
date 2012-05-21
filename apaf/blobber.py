#!/usr/bin/env python
"""
The blobber module generates an autoextracting python file given the input
directory dir.
"""
from __future__ import with_statement

import os
import tarfile
import base64
import StringIO

def create_blobbone(directory, filename):
    tar_obj = StringIO.StringIO()
    tar = tarfile.open(mode='w:gz', fileobj=tar_obj)
    tar.add(directory)
    tar.close()
    tar_obj.seek(0)

    header_code = "import tarfile, base64, os, StringIO\n"
    uncompacting_code = (
    "encoded_obj = StringIO.StringIO()\n"
    "tar_obj = StringIO.StringIO()\n"
    "encoded_obj.write(blob)\n"
    "encoded_obj.seek(0)\n"
    "base64.decode(encoded_obj, tar_obj)\n"
    "tar_obj.seek(0)\n"
    "tar = tarfile.open('r:gz', fileobj=tar_obj)\n"
    "tar.extractall()\n"
    "tar.close()\n")

    with open(filename, 'wb') as f:
        f.write(header_code)
        f.write('blob = r"""')
        base64.encode(tar_obj, f)
        f.write('"""\n')
        f.write(uncompacting_code)

if __name__ == "__main__":
    import sys

    if len(sys.argv) not in (2, 3):
        print "Usage ./blobber.py <directory> <output (default=bloobone.py)>"
        sys.exit(1)

    directory = sys.argv[1]
    filename = 'blobbone.py' if len(sys.argv) == 2 else sys.argv[-1]
    create_blobbone(directory, filename)
    print "Blobbone created. Run python %s to decompress it." % filename
