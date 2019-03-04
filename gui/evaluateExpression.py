# Helper module for evaluating Python mathematical expressions

from numpy import *

def evaluateExpression(expr, x):
    """
    Evaluate the given string as a Python expression.

    expr: String containing expression to evaluate.
    x:    Numeric variable available for computations.
    """
    THETA  = lambda a : where(x > a, zeros(x.shape), ones(x.shape))
    iTHETA = lambda a : where(x < a, zeros(x.shape), ones(x.shape))

    f = eval(expr)
    if isinstance(f, int) or isinstance(f, float) or len(f) == 1:
        f = ones(x.shape) * f

    return f
    
