#!/usr/bin/env python

import os
import tarfile
import base64
import sys
import StringIO

if len(sys.argv) < 2:
    print "Usage ./blobber.py <directory> <output (default=bloobone.py)>"
    sys.exit(1)

filename=None
if sys.argv[1].startswith("~"):
    directory = os.path.expanduser(sys.argv[1])
else:
    directory = sys.argv[1]

if len(sys.argv) > 2:
    filename = sys.argv[2]

def create_blobbone(directory, filename="blobbone.py"):
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

    f2 = open(filename, 'wb')
    f2.write(header_code)
    f2.write('blob = r"""')
    base64.encode(tar_obj, f2)
    f2.write('"""\n')
    f2.write(uncompacting_code)
    f2.close()
    print "Blobbone created. Run python %s to decompress it." % filename

if __name__ == "__main__":
    if filename:
        create_blobbone(directory, filename)
    else:
        create_blobbone(directory)

