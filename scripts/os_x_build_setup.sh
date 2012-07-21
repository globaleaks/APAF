#!/bin/bash
#
# APAF build system OS X install script
#

export VERSIONER_PYTHON_PREFER_32_BIT=yes

if ! which git; then
	#exit if we do not have git
	echo "Couldn't start without git please download it from: http://git-scm.com/download/mac"
	exit 1;
fi

if ! which pip &> /dev/null; then
    echo "Installing pip"
    python easy_install pip
fi

if ! which virtualenv &> /dev/null; then
    echo "Installing virtual env"
    python easy_install virtualenv
fi

# setup env
virtualenv apaf-env
. apaf-env/bin/activate
echo `which python`

easy_install pyobjc-core
easy_install pyobjc

pip install txtorcon py2app twisted pyYAML pyCrypto cyclone
easy_install http://pypi.python.org/packages/source/z/zope.interface/zope.interface-4.0.0.tar.gz

mkdir src
cd src

git clone https://github.com/meejah/txtorcon.git
pip install ./txtorcon

#download tor browser to extract executable
wget --no-check-certificate https://www.torproject.org/dist/torbrowser/osx/TorBrowser-2.2.35-12-osx-i386-en-US.zip
unzip TorBrowser-2*

# move up
cd ..
mv src/TorBrowser_en-US.app/Contents/MacOS/tor datadir/contrib/
rm -rf src/





