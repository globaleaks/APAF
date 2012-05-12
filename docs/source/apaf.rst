.. _apaf:

===========================================
The Anonymous Python Application Framework
===========================================

This sections explais the choices meade for these tasks:
*Define what the threat model for APAF is and what sort of properties it should provide*


The APAF project aims to be a static file server written in python, on the same
development idea behind the tor browser bundle: being a simple and
portable executable for non-technical users. [#]_

Basic properties of the APAF are well-described by Arturo Filastò on the tor-dev
mailing list. [#]_ The core model consists in a basic library which interfaces
with tor, and a basic application server.


Configuration
-------------

The application can be customized using the browser. By default the
configuration page shall be accessible only from localhost, after authenticating
with a standard login form.
The restricted access of only localhost to the configuration section shall be
unckecked.

Packaging system
----------------

A fine example of a packaging system is miro: https://github.com/pculture/miro.
In particular check out the content of the tv dir. There you will find a set of
build scripts for the various platforms.

They also are interesting in having mixed binary and python code be run on the machine.
What they do is have a set of "binary kits" (http://binarykits.pculture.org/), that are
fetched by the build script. Unfortunately they do not do any kind of verification on the
downloaded binary kit and fetch it over http!

I will base the analysis of the packaging system on this system as this is a moderately mature
project (existing since 2006) and it is geared towards the same kind of users we aim at reaching.
From their project description:

    It is targeted at average, unsophisticated Internet users with broadband connections.
    It can be built for Mac OS X, Microsoft Windows, or X Window-based platforms
    such as Linux, with a native look and feel on each platform.  There is
    a clean separation between the portable backend and the
    platform-specific frontend in the event that new ports are desired in
    the future


Mac OS X
........

For OSX they use py2app. The current version of Miro only supports >= 10.5.

The procedure for packaging an application is: ::

    ./setup_binarykit.sh
    ./setup_sandbox.sh
    ./build.sh

Unfortunately because of the fact that 10.7 does not include universal binary related stuff
it can only build on 10.5 and 10.6.


Inside of the `miro/tv/osx` directory there are a few interesting scripts:

`setup_binarykit.sh` - Is used to fetch the binaries to be included in the package

`setup_sandbox.sh` - Is used to create a "sandbox" (not in the security sense of the term but
in the sense of working directory) for applying patches to the to be built stuff.

`build.sh` - The actual build script to create the .app with py2app

`Miro.py` - The Mac OS X specific version of Miro to launch the application and provide all the
fancy UI to make it look pretty on OSX.

For making pretty OSXy UI they use import from Foundation *, that is PyObjC http://en.wikipedia.org/wiki/PyObjC.*

Size:
On Mac OS X the size of the .dmg is 39M.

The actual size of the .app is 105M and the major
contributions to the size are: ::

    30M    /Volumes/Miro/Miro.app/Contents/Helpers/ffmpeg
    27M    /Volumes/Miro/Miro.app/Contents/Resources/lib/python2.7/
    12M    /Volumes/Miro/Miro.app/Contents/Helpers/miro-segmenter
    10M    /Volumes/Miro/Miro.app/Contents/Helpers/ffmpeg2theora
    7.3M    /Volumes/Miro/Miro.app/Contents/Components/Perian.component
    3.9M    /Volumes/Miro/Miro.app/Contents/Components/XiphQT.component
    3.4M    /Volumes/Miro/Miro.app/Contents/Frameworks/Python.framework

For more on how they do builds on OSX: https://develop.participatoryculture.org/index.php/OSXBuildDocs

Windows
.......


Interesting scripts are `miro/tv/windows/setup.py` that uses py2exe to build a windows application. For the
UI part is uses pygtk.

The actual windows UI application is located inside of `miro/tv/windows/plat/frontends/widgets/application.py`.


Size:
The current version shipps an Installer, but previous versions used to be
`Miro-5.0.exe                                       01-May-2012 15:20   49M`

Linux
.....

I think we should make packages for linux based systems. I would start with just a `.deb`.

.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-March/003416.html
.. [#] : https://lists.torproject.org/pipermail/tor-dev/2012-April/003475.html



