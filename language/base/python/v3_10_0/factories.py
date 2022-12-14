from .generated import *

__all__ = [
    'atom',
]


def atom(obj: None | bool | str | int | float):
    """
    Converts a given object to its corresponding Python atom.

    Args:
        obj (None | bool | str | int | float): The object to convert.

    Returns:
        A constant (NONE, TRUE, or FALSE) if `obj` is None, True, or False, respectively.
        An instance of the String, Integer, or Decimal class if `obj` is a str, int, or float, respectively.

    Raises:
        ValueError: If `obj` is not one of the supported types (None, bool, int, str, float).
    """
    if obj is None:
        return NONE
    elif obj is True:
        return TRUE
    elif obj is False:
        return FALSE
    elif isinstance(obj, str):
        return String(repr(obj))
    elif isinstance(obj, int):
        return Integer(repr(obj))
    elif isinstance(obj, float):
        return Decimal(repr(obj))
    else:
        raise ValueError(f"Unable to create the corresponding python atom for {obj!r}.")
