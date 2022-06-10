from .scan import scan
from website import console

__all__ = [
    'help_'
]


def help_():
    console.info('scan [-d]', scan.__doc__)
