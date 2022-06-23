
import numpy as np
from scipy.integrate import quad
from scipy.special import kv

def synchrotron(P, XI, wavelength, magneticField):
    """
    Calculates the synchrotron power at the given wavelength
    'wavelength' (which may be an array) on the given P/XI
    grid, with magnetic field strength 'magneticField'.

    P:             Momentum grid.
    XI:            Pitch grid.
    wavelength:    Wavelength(s) at which to evaluate the function.
    magneticField: Magnetic field strength.
    """
    c = 299792458
    e = 1.60217662e-19
    m = 9.10938356e-31
    eps0 = 8.854187817e-12
    B = magneticField

    gmm = np.sqrt(1 + P**2)
    gmmpar = np.divide(gmm, np.sqrt(1 + P**2 * (1 - XI**2)))

    lowerBound = 4*np.pi/3 * c*m*np.divide(gmmpar, e*B*gmm**2)
    pf = 1/np.sqrt(3) * c*e**2 * np.divide(1, eps0*gmm**2)

    try: wavelength[0]
    except: wavelength = np.array([wavelength])

    s = 0
    for i in range(0, len(wavelength)):
        intK53 = quad(lambda x : kv(5/3, x), lowerBound/wavelength[i], np.inf)[0]
        prefactor = pf / wavelength[i]**3
        s = s + prefactor * intK53

    return s


