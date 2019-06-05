import os
from setuptools import find_packages, setup

from bore import __version__ as VERSION


NAME = 'bore'
DESCRIPTION = 'Bore down to your project root.'
URL = 'https://github.com/gucciferXCIV/bore'
EMAIL = 'suppalxciv@gmail.com'
AUTHOR = 'Garrett Jenkins'

REQUIRED = []

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as readme:
    README = '\n' + readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    py_modules=['bore'],
    include_package_data=True,
    license='MIT',
    description=DESCRIPTION,
    long_description=README,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    install_requires=REQUIRED,
    entry_points={
        'console_scripts': [
            'bore = bore:cli',
        ],
    },
    extras_require={
        'docs': ['Sphinx>=1.6.5'],
        'tests': ['pytest>=3.2.5'],
    },
    keywords=['directory', 'project', 'root', 'finder'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
