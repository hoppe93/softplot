# Helper module for evaluating Python mathematical expressions

from numpy import *

def evaluateExpression(expr, x, lcls=None):
    """
    Evaluate the given string as a Python expression.

    expr: String containing expression to evaluate.
    x:    Numeric variable available for computations.
    pre:  Python code to evaluate first.
    """
    THETA  = lambda a : where(x > a, zeros(x.shape), ones(x.shape))
    iTHETA = lambda a : where(x < a, zeros(x.shape), ones(x.shape))

    lcls['x'] = x
    f = None
    if lcls is not None:
        f = eval(expr, globals(), lcls)
    else:
        f = eval(expr)

    if isinstance(f, int) or isinstance(f, float) or len(f) == 1:
        f = ones(x.shape) * f

    return f
    
