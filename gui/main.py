#!/usr/bin/env python3

from PyQt5 import QtWidgets
import sys, inspect, os

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/../"))

from DetectorCalibration import DetectorCalibration
from DistributionFunctionUI import DistributionFunctionUI
from ImageWindow import ImageWindow
from MeqWindow import MeqWindow
from SingleEnergyPitchIJ import SingleEnergyPitchIJ
from BeamsizeMeasurement import BeamsizeMeasurement
from GreensFunctionR12 import GreensFunctionR12
from GreensFunctionIJ import GreensFunctionIJ

from GeriMap import registerGeriMap

app = None


def show_detcal(argv):
    global app

    dwindow = DetectorCalibration(argv)
    dwindow.show()
    return app.exec_()


def show_distfunc(argv):
    global app

    dwindow = DistributionFunctionUI(argv)
    dwindow.show()
    return app.exec_()

    
def show_image(argv):
    global app

    iwindow = ImageWindow(argv)
    iwindow.show()
    return app.exec_()


def show_greenij(argv):
    global app

    gijwindow = GreensFunctionIJ(argv)
    gijwindow.show()
    return app.exec_()


def show_meq(argv):
    global app

    meqwindow = MeqWindow(argv)
    meqwindow.show()
    return app.exec_()


def show_r12(argv):
    global app

    gwindow = GreensFunctionR12(argv)
    gwindow.show()
    return app.exec_()


def show_rij(argv):
    global app

    gwindow = BeamsizeMeasurement(argv)
    gwindow.show()
    return app.exec_()


def show_s12ij(argv):
    global app

    gwindow = SingleEnergyPitchIJ(argv)
    gwindow.show()
    return app.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    registerGeriMap(None)

    if len(sys.argv) < 2:
        sys.exit(1)

    if sys.argv[1] == 'detcal':
        sys.exit(show_detcal(sys.argv[2:]))
    elif sys.argv[1] == 'distfunc':
        sys.exit(show_distfunc(sys.argv[2:]))
    elif sys.argv[1] == 'image':
        sys.exit(show_image(sys.argv[2:]))
    elif sys.argv[1] == 'meq':
        sys.exit(show_meq(sys.argv[2:]))
    elif sys.argv[1] == 'greenij':
        sys.exit(show_greenij(sys.argv[2:]))
    elif sys.argv[1] == '12' or sys.argv[1] == 'r12':
        sys.exit(show_r12(sys.argv[2:]))
    elif sys.argv[1] == 'rij':
        sys.exit(show_rij(sys.argv[2:]))
    elif sys.argv[1] == 's12ij':
        sys.exit(show_s12ij(sys.argv[2:]))
    else:
        print("ERROR: Unrecognized app requested: '{0}'.".format(sys.argv[1]))
        sys.exit(2)


