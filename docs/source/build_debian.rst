==========================================
Setting up the APAF build System on debian
==========================================

install debian build tools
http://ghantoos.org/2008/10/19/creating-a-deb-package-from-a-python-setuppy/
http://wiki.debian.org/Python/Packaging

# apt-get install build-essential dpkg-dev debhelper devscripts fakeroot

install apaf dependencies

$ apt-get install tor python-twisted python-pip
$ pip install pygeoip ipaddr pyYAML

checkout branch debian

build debian with

$ python setup.py sdist -d ..
update changelog (how?)

$ debuild


Updating relase
---------------

Use `debchange` to change your changelog with `debchange -a`, then make a new release `debchange -r`
Build apaf with `python setup.py sdist` and, after being sure to have set up you gpg configuration, make the debian package with `$ dpkg-buildpackage -i -Ifakeroot`.

Done!



