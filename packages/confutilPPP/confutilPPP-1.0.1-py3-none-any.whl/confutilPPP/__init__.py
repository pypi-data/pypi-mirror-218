from ._confutil import *

__all__ = ['__version__', 'check_config']
__version__ = '1.0.1'


def check_config(_object=None, filename='config'):
    return confutil.check_config(_object, filename)
