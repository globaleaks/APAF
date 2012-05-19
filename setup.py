from setuptools import setup, find_packages
from os.path import join
import os

from apaf.config import config
from apaf import __version__, __author__

if config.platform == 'win32':
    import py2exe
elif config.platform == 'darwin':
    import py2app


APP = [os.path.join('apaf', 'run.py')]

# static files
DATA_FILES = [(root, [join(root, file) for file in files])
              for root, _, files in os.walk(join('apaf', 'panel', 'static'))]
# binary files
DATA_FILES += [(root, [join(root, file) for file in files])
               for root, _, files in os.walk(join('contrib'))]


# warning: building a .app from OSX greater than 10.6 does not work!
OPTIONS_PY2APP = dict(
    argv_emulation = True,
    install_requires=['py2app>=0.6.4'],
)

OPTIONS_PY2EXE = dict(
   install_requires=['py2exe>=0.6.9', 'pywin32'],
)


setup(
    name='apaf',
    version=__version__,
    author=__author__,
    app=APP,
    console=APP,
    data_files=DATA_FILES,
    options=dict(py2app=OPTIONS_PY2APP,
                 py2exe=OPTIONS_PY2EXE,
    ),
    entry_points=dict(console_scripts=['apaf = apaf.run:main']),
    packages=find_packages(exclude=['test']),
)
