===========================================
Setting up the APAF build System on Windows
===========================================

This tutorial winn guide you through the installation of the apaf and its
dependencies in a Windows environment.

.. warning ::
    This tutorial has been tested only on Windows XP sp3 and Windows 7.

.. note ::
    This tutorial will start assuming you are on a clean environment. If you
    have already installed Python, you may consider start reading further.


Requirements
-------------
* Python 2.7.3
 * http://www.python.org/download/releases/2.7.3/
* Twisted 12.0
 * http://twistedmatrix.com/trac/
* Setuptools 0.6-c11 
 * TODO:URL
* Psutils 0.4.1
 * http://code.google.com/p/psutil/
* Py2exe 0.6.9
 * TODO:URL
* Six 1.1.0
 * TODO:URL
* PyGeoIP 0.2.3
 * TODO:URL
* Ipaddr 2.1.10
 * TODO:URL
* PyWin Build 20217
 * TODO:URL
* PyYAML 3.10
 * 
* 7zip 9.20
 * http://downloads.sourceforge.net/sevenzip/7z920.exe
* Gpg 4 win 2.1.1 
 * http://www.gpg4win.org/download.html
* Git 1.7.3+
 * http://git-scm.com/download/win

Install GnuPG
-------------
Install GnuPG as a tool to to verify the various software download:

http://files.gpg4win.org/Beta/gpg4win-2.1.1-34299-beta.exe

Install Python
--------------
Download Python 2.7 from http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi

Verify signature of application: http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi.asc

Install the software following the wizard.

Install Setuptools
------------------

Download http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20

Install Pip
-----------
    cd C:\Python27\Scripts
    C:\Python27\Scripts> easy_install.exe pip

Install psutil
--------------
Required for txtorconn

Download from http://psutil.googlecode.com/files/psutil-0.4.1.win32-py2.7.exe

Install Py2Exe
--------------
Url for py2exe: http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download

Install PyWin32
---------------
Url for pywin32: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/pywin32-217.win32-py2.7.exe/download

Install Twisted
---------------
Donwload from http://pypi.python.org/packages/2.7/T/Twisted/Twisted-12.0.0.win32-py2.7.msi

Install Zope.interface
----------------------
.. warning ::
    Installing zope.interface with pip may lead to ImportError in building the
    APAF with py2exe.

.. note ::
    Tests on windows 7 show that, since easy_install behaves differently from
    pip.exe, using one instead of another during the setup of the environment
    may lead to problems afterwards when building the executable.

Install `zope.interface` using setuptools: ::
    C:\Python27\Scripts> easy_install.exe zope.interface

Install Six
-----------
    cd C:\Python27\Scripts
    C:\Python27\Scripts> pip.exe install six

Install pygeoip
---------------
    cd C:\Python27\Scripts
    C:\Python27\Scripts> pip.exe install pygeoip

Install ipaddr
--------------
    cd C:\Python27\Scripts
    C:\Python27\Scripts> pip.exe install ipaddr

Install pyYAML
--------------
    cd C:\Python27\Scripts
    C:\Python27\Scripts> pip.exe install pyYAML

Install Git
-----------
Since github lets you download a simple `.zip`  of the latest revision of your
application, git is not indispensable. But certainly it will be comfortable to
stay up to date with the software development

http://git-scm.com/download/win

Then open a new Git shell from `Start>Git>Git Bash`.


Install Txtorcon
----------------
Txtorcon is not avaible on the Python Package Index, so you need to install it manually with git.

Additionally there are some bugs (https://github.com/meejah/txtorcon/pull/4) preventing builds, so we must use this fork of txtorcon ::

    $ git clone https://github.com/mmaker/txtorcon.git

Then install with pip: ::
    cd C:\Python27\Scripts
    C:\Python27\Scripts> pip.exe install C:\path\of\txtorcon\


Install Apaf
------------
Download Apaf from Github:

    $ git clone https://github.com/mmaker/APAF.git

Install 7zip
------------
Download http://downloads.sourceforge.net/sevenzip/7z920.exe and install following the wizard.

It will place 7z.exe in "c:\Program Files\7-Zip\7z.exe"

Extract Tor binary
------------------

Download the latest version of Tor binaries for Windows.

Go to download page https://www.torproject.org/download/download.html.en and download "Expert Bundle":
https://www.torproject.org/dist/win32/tor-0.2.2.35-win32-1.exe

Now decompress the tor binary with 7zip and move it to contrib/tor/ directory of APAF:

    c:\Program Files\7-Zip\7z.exe x tor-0.2.2.35-win32-1.exe tor.exe
    move tor.exe PATH_WHERE_IS_BUILD_ENVIRONMENT/contrib/tor 

Build Apaf Application
----------------------
Here you are ready to use the apaf. To build the single `.exe` file, run  ::

    C:\path\of\user\APAF> C:\Python27\python.exe setup.py py2exe



