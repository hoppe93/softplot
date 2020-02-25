# A combination of a set of momentum space distribution functions
# at a number of radii.

from bisect import bisect
import numpy as np

from Distribution.DistributionFunction import DistributionFunction


class PhaseSpaceDistribution(DistributionFunction):
    
    def __init__(self, r=None, distributions=None):
        super().__init__()
        self._distributions = list()
        self._radii = list()

        if r is not None and distributions is not None:
            self._distributions = distributions
            self._radii = r


    def insertMomentumDistribution(self, r, f):
        """
        Insert the MomentumDistribution object 'f' at the radii 'r'.

        r: Radius at which the distribution function applies.
        f: Momentum-space distribution function object.
        """
        i = bisect(self._radii, r)
        self._radii.insert(i, r)
        self._distributions.insert(i, f)


    def eval(self, r, P=None, XI=None):
        """
        Evaluate the distribution function at the given radius,
        on the given P/XI grid.

        r:  Radius at which to evaluate the distribution function.
        P:  Momentum grid on which to evaluate the distribution
            (meshgrid).
        XI: Pitch grid on which to evaluate the distribution function.
        """
        if r < 0:
            raise ValueError("Cannot evaluate distribution function at negative radii.")

        # Locate two closest distribution functions
        i = bisect(self._radii, r)

        # Exact match?
        if i > 0 and r == self._radii[i-1]:
            return self._distributions[i-1].eval_mom(P, XI)

        r0, r1 = 0, 0
        f0, f1 = 0, 0
        if i == 0:
            r0 = 0
            r1 = self._radii[0]
            r2 = self._radii[1]

            P, XI, f1 = self._distributions[0].eval_mom(P, XI)
            _, _,  f2 = self._distributions[1].eval_mom(P, XI)
            f0 = (r2*f1 - r1*f2) / (r2-r1)
        elif i == len(self._radii):     # r is outside grid => extrapolate
            r0 = self._radii[i-1]
            r1 = r0 + (2*r0 - self._radii[i-2])

            P, XI, f0 = self._distributions[i-1].eval_mom(P, XI)
            _, _,  f1 = 2*f0 - self._distributions[i-2].eval_mom(P, XI)
        else:
            r0 = self._radii[i-1]
            r1 = self._radii[i]

            P, XI, f0 = self._distributions[i-1].eval_mom(P, XI)
            _, _,  f1 = self._distributions[i].eval_mom(P, XI)

        return P, XI, ((r1-r)*f0 + (r-r0)*f1) / (r1-r0)


    def getAngleAveragedDistribution(self, r, p=None):
        """
        Returns the angle-averaged distribution function f(p)
        at the given radius r.

        r: Radius at which to evaluate the distribution function.
        p: Momentum grid on which to evaluate the distribution.
           If None is specified, the default momentum grid is used.
        """
        if r < 0:
            raise ValueError("Cannot evaluate distribution function at negative radii.")

        # Locate two closest distribution functions
        i = bisect(self._radii, r)

        # Exact match?
        #if i < len(self._radii) and r == self._radii[i]:
        if i > 0 and r == self._radii[i-1]:
            return p, self._distributions[i-1].eval_mom(p, 0)

        r0, r1 = 0, 0
        f0, f1 = 0, 0
        if i == 0:
            r0 = 0
            r1 = self._radii[0]
            r2 = self._radii[1]

            p, f1 = self._distributions[0].getAngleAveragedDistribution(0, p)
            _, f2 = self._distributions[1].getAngleAveragedDistribution(0, p)
            f0 = (r2*f1 - r1*f2) / (r2-r1)
        elif i == len(self._radii):     # r is outside grid => extrapolate
            r0 = self._radii[i-1]
            r1 = r0 + (2*r0 - self._radii[i-2])

            p, f0 = self._distributions[i-1].getAngleAveragedDistribution(0, p)
            _, f1 = 2*f0 - self._distributions[i-2].getAngleAveragedDistribution(0, p)
        else:
            r0 = self._radii[i-1]
            r1 = self._radii[i]

            p, f0 = self._distributions[i-1].getAngleAveragedDistribution(0, p)
            _, f1 = self._distributions[i].getAngleAveragedDistribution(0, p)

        return p, ((r1-r)*f0 + (r-r0)*f1) / (r1-r0)


    def getCurrentMoment(self, r, p=None):
        """
        Returns the current density moment of the distribution
        function at the given radius.

        r: Radius at which to evaluate the distribution function.
        p: Momentum grid on which to evaluate the distribution.
           If None is specified, the default momentum grid is used.
        """
        if r < 0:
            raise ValueError("Cannot evaluate distribution function at negative radii.")

        # Locate two closest distribution functions
        i = bisect(self._radii, r)

        # Exact match?
        #if i < len(self._radii) and r == self._radii[i]:
        if i > 0 and r == self._radii[i-1]:
            return self._distributions[i-1].getCurrentDensity(r, p)

        r0, r1 = 0, 0
        f0, f1 = 0, 0
        if i == 0:
            r0 = 0
            r1 = self._radii[0]
            r2 = self._radii[1]

            p, f1 = self._distributions[0].getCurrentDensity(r1, p)
            _, f2 = self._distributions[1].getCurrentDensity(r2, p)
            f0 = (r2*f1 - r1*f2) / (r2-r1)
        elif i == len(self._radii):     # r is outside grid => extrapolate
            r0 = self._radii[i-1]
            r1 = r0 + (2*r0 - self._radii[i-2])

            p, f0 = self._distributions[i-1].getCurrentDensity(r0, p)
            _, f1 = 2*f0 - self._distributions[i-2].getCurrentDensity(r1, p)
        else:
            r0 = self._radii[i-1]
            r1 = self._radii[i]

            p, f0 = self._distributions[i-1].getCurrentDensity(r0, p)
            _, f1 = self._distributions[i].getCurrentDensity(r1, p)

        return p, ((r1-r)*f0 + (r-r0)*f1) / (r1-r0)


    def getMomentum(self, rindex):
        """
        Returns the 'default' momentum grid for the
        distribution function at radial index 'rindex'.
        """
        return self._distributions[rindex].getMomentum()


    def getMomentumDistribution(self, rindex):
        """
        Returns the momentum-space distribution with index 'rindex'.
        """
        return self._distributions[rindex]


    def getCurrentDensity(self, r=None, p=None, cumulative=False):
        """
        Returns the radial current density for the distribution function.

        r:          Radial grid to evaluate the distribution on. If 'None',
                    uses the default radial grid.
        p:          Momentum grid on which to evaluate the current density.
                    If 'None', the default momentum grid of the first radius
                    is used.
        cumulative: If 'True', returns the "cumulative current density",
                    i.e. j(p), where j(p0) is the current density carried
                    by particles with momentum p <= p0.
        """
        mc = 9.10938356e-31 * 299792458.0

        if r is None:
            r = np.copy(self._radii)

        if not hasattr(r, '__iter__'):
            r = [r]

        P = None
        if p is not None:
            P = p

        n = list()
        for radius in r:
            # Evaluate current moment of distribution
            p, f = self.getCurrentMoment(radius, p=P)

            if P is None:
                P = p

            # Calculate dp
            dp = np.zeros(P.shape)
            dp[:-1] = np.diff(P)
            dp[-1] = dp[-2]

            if cumulative is False:
                # Integrate angle-averaged distribution (4*pi * p**2 is the Jacobian)
                n.append(4*np.pi*np.sum(f * P**2 * dp * mc**3))
            else:
                j = np.cumsum(4*np.pi*f * P**2 * dp * mc**3)
                n.append(j)

        if cumulative:
            return r, P, np.array(n)
        else:
            return r, np.array(n)


    def getRadialDensity(self, r=None):
        """
        Returns the radial density for the distribution function.
        This corresponds to integrating the distribution function
        over all of momentum space.

        r: Radial grid to evaluate the distribution on. If 'None',
           uses the default radial grid.
        """
        mc = 9.109e-31 * 299792458.0

        if r is None:
            r = np.copy(self._radii)

        n = list()
        for radius in r:
            # Evaluate angle-averaged distribution
            p, f = self.getAngleAveragedDistribution(radius)
            # Calculate dp
            dp = np.zeros(p.shape)
            dp[:-1] = np.diff(p)
            dp[-1] = dp[-2]
            # Integrate angle-averaged distribution (p**2 is the Jacobian)
            n.append(np.sum(f * p**2 * dp * mc**3))

        return r, np.array(n)


