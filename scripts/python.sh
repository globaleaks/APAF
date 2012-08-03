#! /bin/sh
# XXX .P4A version 0r3 requires a different $PYTHONHOME, just edit that and
# should work.
export EXTERNAL_STORAGE=/mnt/sdcard/com.googlecode.pythonforandroid/
export PYTHONHOME=/data/data/com.googlecode.pythonforandroid/files
export PYTHONPATH=$EXTERNAL_STORAGE/extras/python:$PYTHONHOME/lib/python2.6/lib-dynload:$PYTHONHOME/python/lib/python2.6/lib-dynload
export PYTHON_EGG_CACHE=$EXTERNAL_STORAGE_P4A/cache
export LD_LIBRARY_PATH=$PYTHONHOME/lib
# add Orbot's bin directory to our path -- XXX. hack, I should use
# apaf.config.tor_binary
export PATH=/data/data/org.torproject.android/app_bin/


$PYTHONHOME/bin/python "$@"

