#!/usr/bin/python3

from PIL import Image
import GeriMap
import os
import h5py
import numpy as np


def save(argv):
    inp = None
    otp = None

    if len(argv) == 1:
        inp = argv[0]
        otp = os.path.splitext(os.path.basename(inp))[0]+'.png'
    elif len(argv) == 2:
        inp = argv[0]
        otp = argv[1]
    else:
        print("ERROR: Expected exactly one or two command line arguments.")
        print("Syntax:")
        print("  png [input [output]]")
        return -1

    img = None
    with h5py.File(inp, 'r') as f:
        img = f['image'][:].T

    img /= np.amax(img)
    cmap = GeriMap.get()
    im = Image.fromarray(np.uint8(cmap(img)*255))
    im.save(otp)

    return 0


