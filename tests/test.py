#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path, chdir
from os.path import join, dirname, basename, abspath
from sys import exit, path
from unittest import defaultTestLoader, TextTestRunner

test_root = dirname(abspath(__file__))
test_files = glob(join(test_root, 'test_*.py'))
test_names = [basename(name)[:-3] for name in test_files]

chdir(test_root)
path.insert(0, join(dirname(test_root), 'src'))
path.insert(0, test_root)

suite = defaultTestLoader.loadTestsFromNames(test_names)

def run():
    result = TextTestRunner(verbosity=1).run(suite)
    exit(1 if result.errors or result.failures else 0)

if __name__ == '__main__':
    run()

