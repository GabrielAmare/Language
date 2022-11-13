import abc
import typing

__all__ = [
    'Writable',
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
