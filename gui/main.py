#!/usr/bin/env python3

from PyQt5 import QtWidgets
import sys, inspect, os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/../"))

from DetectorCalibration import DetectorCalibration
from ImageWindow import ImageWindow
from MeqWindow import MeqWindow
from SingleEnergyPitchIJ import SingleEnergyPitchIJ
from BeamsizeMeasurement import BeamsizeMeasurement

app = None


def registerGeriMap(transparencyThreshold=0.4):
    """
    Register the perceptually uniform colormap 'GeriMap' with matplotlib

    transparencyThreshold: All intensities below this threshold will have
                           a non-zero alpha value (making them more or
                           less transparent). The opacity varies linearly,
                           being 1 at this value, and 0 at zero.
    """
    gm = [(0, 0, 0), (.15, .15, .5), (.3, .15, .75),
          (.6, .2, .50), (1, .25, .15), (.9, .5, 0),
          (.9, .75, .1), (.9, .9, .5), (1, 1, 1)]
    gerimap = LinearSegmentedColormap.from_list('GeriMap', gm)
    gerimap_r = LinearSegmentedColormap.from_list('GeriMap_r', gm[::-1])

    if transparencyThreshold is not None:
        n = int(gerimap.N * transparencyThreshold)
        nn = gerimap.N - n

        if n < 0 or nn < 0:
            raise ValueError('Transparency threshold must be a value between 0 and 1.')

        a = np.linspace(0, 1, n)
        b = np.ones((nn,))

        gmap = gerimap(np.arange(gerimap.N))
        gmap[:,-1] = np.concatenate((a,b), axis=None)
        gerimap = LinearSegmentedColormap.from_list('GeriMap', gmap)

        gmap_r = gerimap_r(np.arange(gerimap.N))
        gmap_r[:,-1] = np.concatenate((a,b), axis=None)
        gerimap_r = LinearSegmentedColormap.from_list('GeriMap_r', gmap_r)

    plt.register_cmap(cmap=gerimap)
    plt.register_cmap(cmap=gerimap_r)


def show_detcal(argv):
    global app

    dwindow = DetectorCalibration(argv)
    dwindow.show()
    return app.exec_()

    
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
        sys.exit()

    if sys.argv[1] == 'detcal':
        sys.exit(show_detcal(sys.argv[2:]))
    elif sys.argv[1] == 'image':
        sys.exit(show_image(sys.argv[2:]))
    elif sys.argv[1] == 'meq':
        sys.exit(show_meq(sys.argv[2:]))
    elif sys.argv[1] == 'rij':
        sys.exit(show_rij(sys.argv[2:]))
    elif sys.argv[1] == 's12ij':
        sys.exit(show_s12ij(sys.argv[2:]))
    else:
        print("ERROR: Unrecognized app requested: '{0}'.".format(sys.argv[1]))

