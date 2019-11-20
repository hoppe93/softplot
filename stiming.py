# Simple timing interface

import time

_tictimer = time.time()
def tic():
    global _tictimer
    _tictimer = time.time()


def toc():
    global _tictimer
    print('Elapsed time: {:.6f}s'.format(time.time()-_tictimer))


