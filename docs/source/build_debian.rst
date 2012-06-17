==========================================
Setting up the APAF build System on debian
==========================================

install debian build tools
http://ghantoos.org/2008/10/19/creating-a-deb-package-from-a-python-setuppy/
http://wiki.debian.org/Python/Packaging

# apt-get install build-essential dpkg-dev debhelper devscripts fakeroot

install apaf dependencies

$ apt-get install tor python-twisted python-psutil python-pip
$ pip install pygeoip ipaddr pyYAML

checkout branch debian

build debian with

$ python setup.py sdist -d ..
update changelog (how?)

$ debuild


