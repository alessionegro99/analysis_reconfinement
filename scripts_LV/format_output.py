import numpy as np

def format_uncertainty(value, dvalue, significance=2):
    """Creates a string of a value and its error in paranthesis notation, e.g., 13.02(45)"""
    if dvalue == 0.0 or (not np.isfinite(dvalue)):
        return str(value)
    if not isinstance(significance, int):
        raise TypeError("significance needs to be an integer.")
    if significance < 1:
        raise ValueError("significance needs to be larger than zero.")
    fexp = np.floor(np.log10(dvalue))
    if fexp < 0.0:
        return '{:{form}}({:1.0f})'.format(value, dvalue * 10 ** (-fexp + significance - 1), form='.' + str(-int(fexp) + significance - 1) + 'f')
    elif fexp == 0.0:
        return f"{value:.{significance - 1}f}({dvalue:1.{significance - 1}f})"
    else:
        return f"{value:.{max(0, int(significance - fexp - 1))}f}({dvalue:2.{max(0, int(significance - fexp - 1))}f})"

def format_uncertainty_vec(values, dvalues, significance=2):
    return [format_uncertainty(v, d, significance) for v, d in zip(values, dvalues)]