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
See `requirements.txt` file.

Installing Python
------------------
Download Python 2.7 at http://www.python.org/download/releases/2.7.3/ (direct
link at http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi )

Verify signature of application:

http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi.asc

Install the software.


Setuptools
----------

http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20
And then install pip. ::

    cd C:\Python27\Scripts
    C:\Python27\Scripts> easy_install.exe pip

Now use `pip` to install some extra dependencies. ::

    six geoip ipaddr psutil


.. note ::
    Tests on windows 7 show that, since easy_install behaves differently from
    pip.exe, using one instead of another during the setup of the environment
    may lead to problems afterwards when building the executable.




Twisted
-------
Install Twisted

http://twistedmatrix.com/trac/

http://pypi.python.org/packages/2.7/T/Twisted/Twisted-12.0.0.win32-py2.7.msi


Psutils
-------
Required for txtorconn

http://code.google.com/p/psutil/
http://psutil.googlecode.com/files/psutil-0.4.1.win32-py2.7.exe


Py2Exe
-------
Url for py2exe: http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download


PyWin32
-------
Url for pywin32: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/pywin32-217.win32-py2.7.exe/download


Zope
-----
Install `zope.interface` using setuptools: ::
    C:\Python27\Scripts> easy_install.exe zope.interface


.. warning ::
    Installing zope.interface with pip may lead to ImportError in building the
    APAF with py2exe.


Git
--
Since github lets you download a simple `.zip`  of the latest revision of your
application, git is not indispensable. But certainly it will be comfortable to
stay up to date with the software development

http://git-scm.com/download/win

Then open a new Git shell from `Start>Git>Git Bash`.


Txtorcon
--------
Txtorcon is not avaible on the Python Package Index, so you need to install it
manually with git. ::

    $ git clone https://github.com/mmaker/txtorcon.git

Then install with pip: ::
    C:\Python27\Scripts> pip.exe install C:\path\of\user\txtorcon\


APAF
----

And finally! ::

    $ git clone https://github.com/mmaker/APAF.git


here you are ready to use the apaf. To build the single `.exe` file, run  ::

    C:\path\of\user\APAF> C:\Python27\python.exe setup.py py2exe



