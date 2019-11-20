# Run SOFT

import os, sys
import subprocess
import tempfile
from Orbits import Orbits


# Locate SOFT
SOFTPATH = None
try:
    SOFTPATH = os.environ['SOFTPATH']

    # Make sure path does not end with a slash
    if SOFTPATH[-1] == '/':
        SOFTPATH = SOFTPATH[:-1]
except KeyError:
    print('WARNING: Unable to determine SOFT path')
    SOFTPATH = None


def runOrbit(minradius, maxradius, nradius, momentum, pitchangle, meqfile, particleOrbit=False, drifts=True, gc_position=True):
    """
    Simulates the given particle orbit (for an electron) with SOFT. If
    'particleOrbit' is True, then the full particle orbit is followed. The
    default (False) means that the guiding-center orbit is followed.
    """

    # First, we simulate the GC orbit
    pi, outfile = _generateOrbitPi(minradius, maxradius, nradius, momentum, pitchangle, meqfile, gc_position=(gc_position and not particleOrbit), drifts=(drifts or particleOrbit))
    runSOFT(pi)

    orbs = Orbits(outfile)
    os.remove(outfile)

    T, X, Y, Z = orbs.getTXYZ()

    # Simulate particle orbit
    if particleOrbit:
        pi, outfile = _generateOrbitPi(minradius, maxradius, nradius, momentum, pitchangle, meqfile, particleOrbit=particleOrbit, time=T[0,-1])
        runSOFT(pi)

        orbs = Orbits(outfile).getOrbitByIndex(0)
        os.remove(outfile)

        T, X, Y, Z = orbs.getTXYZ()

    return T, X, Y, Z

def _generateOrbitPi(minradius, maxradius, nradius, momentum, pitchangle, meqfile, particleOrbit=False, gc_position=False, drifts=True, time=-1.0):
    """
    radius: Radius at which to initialize particle
    momentum: Momentum with which to initialize particle
    pitchangle: Pitch angle with which to initialize particle
    particleOrbit: True = Follow full particle orbit, False = Follow guiding-center orbit
    gc_position: For GC orbit: The radius specifies GC position, not particle position
    drifts: For GC orbit: Include drift terms in GC equations of motion
    time: End time of the simulation (note: negative times only make sense for GC orbits)

    RETURNS
    The SOFT run script as well as the name of the output file.
    """
    pi = ""

    if drifts:
        pi += "include_drifts = yes;\n"
    else:
        pi += "include_drifts = no;\n"

    pi += "magnetic_field = \"num\";\n"
    pi += "@MagneticField num (numeric) {\n"
    pi += "    filename = "+str(meqfile)+";\n"
    pi += "}\n\n"

    pi += "particle_generator = PGen;\n"
    pi += "@ParticleGenerator PGen {\n"
    pi += "    rho         = {0},{1},{2};\n".format(minradius, maxradius, nradius)
    pi += "    p           = {0},{0},1;\n".format(momentum)
    pi += "    thetap      = {0},{0},1;\n".format(pitchangle)
    pi += "    gc_position = {0};\n".format('yes' if gc_position else 'no')
    pi += "}\n\n"

    pi += "particle_pusher = PPusher;\n"
    pi += "@ParticlePusher PPusher {\n"
    pi += "    equation = {0};\n".format('particle' if particleOrbit else 'guiding-center')

    if time <= 0:
        pi += "    timeunit = poloidal;\n"
        pi += "    time     = 1;\n"
    else:
        pi += "    timeunit = seconds;\n"
        pi += "    time     = {0};\n".format(time)

    pi += "    nt       = 1000;\n"
    pi += "}\n"

    outfile = next(tempfile._get_candidate_names())+'.h5'
    pi += "tools = orbits;\n"
    pi += "@Orbits orbits {\n"
    pi += "    output = \"{0}\";\n".format(outfile)
    pi += "}\n"

    return pi, outfile

def runSOFT(pifile):
    """
    Run SOFT, passing the given pifile on stdin.
    """
    global SOFTPATH

    if SOFTPATH is None:
        raise RuntimeError('The path to SOFT has not been specified')

    p = subprocess.Popen([SOFTPATH+'/soft'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    stderr_data = p.communicate(input=bytearray(pifile, 'ascii'))[1].decode('utf-8')

    if p.returncode != 0:
        print(stderr_data)
        raise RuntimeError('SOFT exited with a non-zero exit code.')

