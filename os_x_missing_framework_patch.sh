#!/bin/bash
#
# patch the app bundle
#

if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` *.app"
  exit $E_BADARGS
fi
. apaf-env/bin/activate
systemFrameworkPath=`python-config --includes | awk -F'-I' '{print $2}' | sed 's/\/include.*$//'`
version=`echo $systemFrameworkPath | awk -F/ '{print $NF}'`

if [[ -ne "$1/Contents/Frameworks/Python.framework/Versions/$version" ]]; then
	#statements
	mkdir -p "$1/Contents/Frameworks/Python.framework/Versions/$version"
	cp $systemFrameworkPath/Python $1/Contents/Frameworks/Python.framework/Versions/$version
fi