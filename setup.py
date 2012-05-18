from setuptools import setup, find_packages
from os.path import join
import os


# import py2exe

APP = [os.path.join('apaf', 'run.py')]

# static files
DATA_FILES = [(root, [join(root, file) for file in files])
              for root, _, files in os.walk(join('apaf', 'panel', 'static'))]
# binary files
DATA_FILES += [(root, [join(root, file) for file in files])
               for root, _, files in os.walk(join('contrib'))]


OPTIONS_PY2APP = dict(
    argv_emulation = True,
#    modules=['_psutil_osx'],
)

OPTIONS_PY2EXE = dict(
    packages = 'twisted.web'
)


setup(
    app=APP,
    data_files=DATA_FILES,
    options=dict(py2app=OPTIONS_PY2APP,
                 py2exe=OPTIONS_PY2EXE,
    ),
    packages=find_packages(),
)
