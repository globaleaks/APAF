============================================
Setting up the APAF build System on Mac OS X
===========================================

This tutorial winn guide you through the installation of the apaf and its
dependencies on a Mac Os X 10.6 environment

.. warning ::
    This tutorial has been tested only on Mac OS X 10.6 and 10.7 (by mogui) .

.. note ::
    This tutorial will start assuming you are on a clean environment. If you
    have already installed Python, you may consider start reading from `Download
    APAF`

Install GnuPG
*************
Install GnuPG as a tool to to verify the various software download:

https://github.com/downloads/GPGTools/GPGTools/GPGTools-20120318.dmg

Install Python
******************
Download Python 2.7 for Mac Os X from http://www.python.org/ftp/python/2.7.3/python-2.7.3-macosx10.6.dmg

Verify signature of application from http://www.python.org/ftp/python/2.7.3/python-2.7.3-macosx10.6.dmg.asc .

Install the software following the wizards.

Install Setuptools and pip
**************************

Download setup tools: ::

    wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
    tar xvzf setuptools-0.6c11.tar.gz
    cd setuptools-0.6c11
    python2.7 setup.py install

Install Pip: ::
    python2.7 /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install-2.7 pip


Install Git
***********
Since github lets you download a simple `.zip`  of the latest revision of your
application, git is not indispensable.
But certainly it will be comfortable to stay up to date with the software development

http://git-scm.com/download/mac

Extract Tor binary
******************
In order to extract the Mac OS X tor's binary we need to download TBB that's packaged as a zip file::
	cd APAF/datadir/contrib/
	wget --no-check-certificate https://www.torproject.org/dist/torbrowser/osx/TorBrowser-2.2.35-12-osx-i386-en-US.zip

Then extract the Tor binary with the following command line by using 7zip for OSX::
	$ unzip TorBrowser-2.2.35-12-osx-i386-en-US.zip

Then move the binary in the current directory::
	$mv TorBrowser_en-US.app/Contents/MacOS/tor .


Obtaining APAF
--------------
APAF has not stable versions yet. You can download the latest revision from git
at: ::

    $ git clone https://github.com/Globaleaks/APAF.git

Onnce downloaded, cd into ```apaf``` and install its dependencies. ::
    cd apaf
    pip -r requirements.txt


Build Apaf Application
**********************
::
	cd ../../
	python2.7 setup.py py2app


Now in dist/ you will find "apaf.app"



