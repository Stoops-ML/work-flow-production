# dummy file required by versioneer
from setuptools import setup

import versioneer

raise NotImplementedError("setup.py is a dummy file required by versioneer")
setup(version=versioneer.get_version(), cmdclass=versioneer.get_cmdclass())
