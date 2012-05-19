from setuptools import setup, find_packages
from os.path import join
import os

from apaf.config import config

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
)

OPTIONS_PY2EXE = dict(
)


setup(
    app=APP,
    console=APP,
    data_files=DATA_FILES,
    options=dict(py2app=OPTIONS_PY2APP,
                 py2exe=OPTIONS_PY2EXE,
    ),
    packages=find_packages(exclude=['test']),
)
