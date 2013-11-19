#!/usr/bin/env python

from setuptools import setup

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
    }
)

