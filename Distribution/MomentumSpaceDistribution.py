# A general momentum-space distribution function

from Distribution.DistributionFunction import DistributionFunction


class MomentumSpaceDistribution(DistributionFunction):
    
    def __init__(self):
        super().__init__()

        self.nr = 1


    def eval(self, r, P=None, XI=None):
        """
        Evaluate the distribution function at the given radius,
        on the given P/XI grid.

        r:  Radius at which to evaluate the distribution function.
        P:  Momentum grid on which to evaluate the distribution
            (meshgrid).
        XI: Pitch grid on which to evaluate the distribution function.
        """
        return self.eval_mom(P, XI)

    def eval_mom(self, P, XI):
        """
        Evaluate the contained momentum-space distribution function.
        """
        raise NotImplementedError("The method 'eval()' is not implemented in the base class 'DistributionFunction'.")

