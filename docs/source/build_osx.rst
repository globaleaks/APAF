============================================
Setting up the APAF build System on Mac OS X
===========================================

This tutorial winn guide you through the installation of the apaf and its
dependencies on a Mac Os X 10.6 environment

.. warning ::
    This tutorial has been tested only on Mac OS X 10.6 and 10.7 (by mogui) .

.. note ::
    This tutorial will start assuming you are on a clean environment. If you
    have already installed Python, you may consider start reading further.


Requirements
-------------
* Python 2.7.3
 * http://www.python.org/getit/mac/
* Twisted 12.0
 * http://twistedmatrix.com/trac/
* Setuptools 0.6-c11
 * http://pypi.python.org/pypi/setuptools
* Psutils 0.4.1
 * http://code.google.com/p/psutil/
* Py2app 0.6.4
 * http://pypi.python.org/pypi/py2app/
 * https://bitbucket.org/ronaldoussoren/py2app
* Six 1.1.0
 * http://pypi.python.org/pypi/six
* PyGeoIP 0.2.3
 * http://code.google.com/p/pygeoip/
* Ipaddr 2.1.10
 * http://code.google.com/p/ipaddr-py/
* PyYAML 3.10
 * http://pyyaml.org/wiki/PyYAML
* 7zip 9.20 (kekaosx)
 * http://www.kekaosx.com/en/
* GPGTools 2012-03-18
 * http://www.gpgtools.org/
* Git 1.7.3+
 * http://git-scm.com/download/mac

Install GnuPG
-------------
Install GnuPG as a tool to to verify the various software download:

https://github.com/downloads/GPGTools/GPGTools/GPGTools-20120318.dmg

Install Python
------------------
Download Python 2.7 for Mac Os X from http://www.python.org/ftp/python/2.7.3/python-2.7.3-macosx10.6.dmg

Verify signature of application from http://www.python.org/ftp/python/2.7.3/python-2.7.3-macosx10.6.dmg.asc .

Install the software following the wizards.

Install Setuptools
----------

Download setup tools:
wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
tar xvzf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
python2.7-32 setup.py install

Install Pip
----------
python2.7-32 /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install-2.7 pip

Install psutil
----------
python2.7-32 /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install-2.7  \
https://psutil.googlecode.com/files/psutil-0.4.1.tar.gz

Install py2app
----------
python2.7-32 /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install-2.7 py2app

Install Twisted
----------
python2.7-32 /Library/Frameworks/Python.framework//Versions/2.7/bin/pip-2.7 install twisted

Install Zope.interface
----------------------
python2.7-32 /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install-2.7 \
http://pypi.python.org/packages/source/z/zope.interface/zope.interface-4.0.0.tar.gz

Install Six
-----------
python2.7-32 /Library/Frameworks/Python.framework//Versions/2.7/bin/pip-2.7 install six

Install pygeoip
---------------
python2.7-32 /Library/Frameworks/Python.framework//Versions/2.7/bin/pip-2.7 install pygeoip

Install ipaddr
--------------
python2.7-32 /Library/Frameworks/Python.framework//Versions/2.7/bin/pip-2.7 install ipaddr

Install pyYAML
--------------
python2.7-32 /Library/Frameworks/Python.framework//Versions/2.7/bin/pip-2.7 install pyYAML

Install Git
-----------
Since github lets you download a simple `.zip`  of the latest revision of your
application, git is not indispensable. 
But certainly it will be comfortable to stay up to date with the software development

http://git-scm.com/download/mac

Install TxTorConn
-----------------
Txtorcon is not avaible on the Python Package Index, so you need to install it manually with git.

    $ git clone https://github.com/meejah/txtorcon.git

Then install with pip: ::
    python2.7-32 /Library/Frameworks/Python.framework//Versions/2.7/bin/pip-2.7 install ./txtorcon

Install Apaf
----------
Download Apaf from Github::

    $ git clone https://github.com/mmaker/APAF.git


Extract Tor binary
------------------
In order to extract the Mac OS X tor's binary we need to download TBB that's packaged as a zip file::
	cd APAF/datadir/contrib/
	wget --no-check-certificate https://www.torproject.org/dist/torbrowser/osx/TorBrowser-2.2.35-12-osx-i386-en-US.zip

Then extract the Tor binary with the following command line by using 7zip for OSX::
	$ unzip TorBrowser-2.2.35-12-osx-i386-en-US.zip

Then move the binary in the current directory::
	$mv TorBrowser_en-US.app/Contents/MacOS/tor .

Build Apaf Application
----------------------
::
	cd ../../
	python2.7-32 setup.py py2app
	

Now in dist/ you will find "apaf.app"



