#  All Rights Reserved
#  Copyright (c) 2023 Nyria
#
#  This code, including all accompanying software, documentation, and related materials, is the exclusive property
#  of Nyria. All rights are reserved.
#
#  Any use, reproduction, distribution, or modification of the code without the express written
#  permission of Nyria is strictly prohibited.
#
#  No warranty is provided for the code, and Nyria shall not be liable for any claims, damages,
#  or other liability arising from the use or inability to use the code.

import io
import os

from setuptools import setup, find_packages

NAME = 'nyria-eldritha'
DESCRIPTION = 'A database handling library for python'
URL = 'https://gitlab.nyria.net/libs/eldritha'
AUTHOR = 'Redtronics, Seri'
REQUIRES_PYTHON = '>=3.10.0'

VERSION = '1.1.1'

LONG_DESCRIPTION = 'A database handling library for python'

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Setting up
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    license='All rights reserved.',
    keywords=['python', "database" "management", "tool", "eldritha", "nyria"],
    requires=['sqlalchemy', 'redis']
)
