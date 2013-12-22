#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test
from sys import exit

class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True
    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        exit(errno)

setup(
    name = 'arc-diagrams',
    version = '0.1',
    author = 'Oliver Mader',
    author_email = 'b52@reaktor42.de',
    url = 'https://github.com/b52/arc-diagrams',
    license = 'MIT',
    packages = ['arc_diagrams'],
    package_data = {
        '': ['LICENSE', 'README.md'],
        'arc_diagrams': ['pixmaps/*.png']
    },
    entry_points = {
        'gui_scripts': ['arc-diagrams = arc_diagrams:main'],
    },
    dependency_links = ['http://www.daimi.au.dk/~mailund/suffix_tree/suffix_tree-2.1.tar.gz'],
    tests_require = ['pytest', 'pytest-quickcheck'],
    cmdclass = {'test': PyTest}
)

