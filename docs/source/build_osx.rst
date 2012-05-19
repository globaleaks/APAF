============================================
Setting up the APAF build System on Windows
===========================================

This tutorial winn guide you through the installation of the apaf and its
dependencies on a Windows environment.

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
And then install pip.

cd C:\Python27\Scripts
C:\Python27\Scripts> easy_install.exe pip


.. note ::
    Tests on windows 7 show that, since easy_install behaves differently from
    pip.exe, using one instead of another during the setup of the environment
    may lead to problems afterwards when building the executable.




Twisted
-------

Install Twisted

http://twistedmatrix.com/trac/

http://pypi.python.org/packages/2.7/T/Twisted/Twisted-12.0.0.win32-py2.7.msi
