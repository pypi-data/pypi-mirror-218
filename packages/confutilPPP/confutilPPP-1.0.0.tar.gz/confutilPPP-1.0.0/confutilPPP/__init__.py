from .confutil import *

__version__ = '1.0'
__all__ = []


def check_config(_object=None, filename='config'):
    return confutil.check_config(_object, filename)
