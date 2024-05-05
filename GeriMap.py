
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


def get(reverse=False):
    gm = [(0, 0, 0), (.15, .15, .5), (.3, .15, .75),
          (.6, .2, .50), (1, .25, .15), (.9, .5, 0),
          (.9, .75, .1), (.9, .9, .5), (1, 1, 1)]

    if reverse:
        return LinearSegmentedColormap.from_list('GeriMap_r', gm[::-1])
    else:
        return LinearSegmentedColormap.from_list('GeriMap', gm)


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

    cmaps = plt.colormaps()
    if gerimap.name not in cmaps:
        plt.register_cmap(cmap=gerimap)
        plt.register_cmap(cmap=gerimap_r)

    return gerimap, gerimap_r


