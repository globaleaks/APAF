from setuptools import setup, find_packages
import os.path

# import py2exe

APP = [os.path.join('apaf', 'run.py')]

DATA_FILES = []

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
