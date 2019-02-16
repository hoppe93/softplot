#!/usr/bin/env python3

from PyQt5 import QtWidgets
import sys, inspect, os

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/../"))

from ImageWindow import ImageWindow
from MeqWindow import MeqWindow

app = None


def show_image(argv):
    global app

    iwindow = ImageWindow(argv)
    iwindow.show()
    return app.exec_()


def show_meq(argv):
    global app

    meqwindow = MeqWindow(argv)
    meqwindow.show()
    return app.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    if len(sys.argv) < 2:
        sys.exit()

    if sys.argv[1] == 'image':
        sys.exit(show_image(sys.argv[2:]))
    elif sys.argv[1] == 'meq':
        sys.exit(show_meq(sys.argv[2:]))
    else:
        print("ERROR: Unrecognized app requested: '{0}'.".format(sys.argv[1]))

