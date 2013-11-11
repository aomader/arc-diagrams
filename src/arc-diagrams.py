#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

from PyQt4.QtGui import QApplication

from ui import Window

def run():
    app = QApplication(argv)
    win = Window()
    app.exec_()

if __name__ == '__main__':
    run()

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
