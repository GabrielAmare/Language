import abc
import typing

__all__ = [
    'Writable',
    'tok',
    'indented',
]


class Writable(abc.ABC):
    """
        Abstract representation of a class of objects that can be written as code.
        NOTE : this structure suppose that a Writable instance is language dependant.
    """
    
    @abc.abstractmethod
    def __tokens__(self) -> typing.Iterator[str]:
        """Returns an iterator of the tokens contents that represent this object."""
    
    def __str__(self):
        """Returns a string representation of the object in its class specific language."""
        return ''.join(self.__tokens__())


def tok(obj: Writable | str) -> typing.Iterator[str]:
    if isinstance(obj, Writable):
        yield from obj.__tokens__()
    elif isinstance(obj, str):
        yield from obj
    else:
        raise TypeError(f"Unable to extract tokens from {type(obj)!r} object.")


def indented(method: typing.Callable[[Writable], typing.Iterator[str]]):
    def wrapped(self) -> typing.Iterator[str]:
        for token in method(self):
            yield token
            if token == '\n':
                yield '    '
    
    return wrapped
