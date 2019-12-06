# General SOFT distribution function


class DistributionFunction:
    
    def __init__(self):
        self.maxp = None
        self.nr = None
        self.nmom = None
        self.r = list()
        self.desc = ""


    def eval(self, r, P=None, XI=None):
        """
        Evaluate the distribution function at the given radius,
        on the given P/XI grid.
        """
        raise NotImplementedError("The method 'eval()' is not implemented in the base class 'DistributionFunction'.")


    def getDescription(self): return self.desc
    def getMaxP(self): return self.maxp
    def getMomentum(self, rindex=None):
        raise Exception("Not implemented for this kind of distribution function.")
    def getNr(self): return self.nr
    def getNmomentum(self): return self.nmom
    def getRadius(self, index): return self.r[index]

    def getAngleAveragedDistribution(self, r, p=None):
        """
        Returns the angle-averaged momentum distribution f(p)
        at the given radius. If no momentum coordinates p
        are given, the distribution function is returned on the
        default grid.
        """
        raise Exception("Not implemented for this kind of distribution function.")


    def getCurrentDensity(self, r=None):
        """
        Returns the current density for the distribution function
        on the given radial grid. The current density is the 
        vpar moment of the distribution function.
        """
        raise Exception("Not implemented for this kind of distribution function.")


    def getRadialDensity(self, r=None):
        """
        Returns the radial density for the distribution function.
        This corresponds to integrating the distribution function
        over all of momentum space.

        r: Radial grid to evaluate the distribution on. If 'None',
           uses the default radial grid.
        """
        raise Exception("Not implemented for this kind of distribution function.")


