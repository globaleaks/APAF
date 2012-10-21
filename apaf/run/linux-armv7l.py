"""
The main file of the apaf on Android.
"""
#import tempfile
import os

from twisted.internet import reactor

from apaf.run import base

def main():
    # XXX. test
    data_directory = './tmp_apaf' # tempfile.mktemp(dir='./')
    os.mkdir(data_directory)

    base.main(data_directory=data_directory)
    reactor.run()

