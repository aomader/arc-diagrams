#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit

from PyQt4.QtGui import QApplication

from .ui import Window

def main():
    app = QApplication(argv)
    win = Window()
    win.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()

# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
