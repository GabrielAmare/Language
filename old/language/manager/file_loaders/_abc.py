import abc
import dataclasses
import functools
import typing

__all__ = [
    'Loader'
]


@dataclasses.dataclass(frozen=True)
class Loader(abc.ABC):
    root: str
    src: typing.Union[str, list[str]]

    @functools.cached_property
    def names(self) -> list[str]:
        if isinstance(self.src, str):
            return [self.src]

        elif isinstance(self.src, list) and all(isinstance(name, str) for name in self.src):
            return self.src

        else:
            raise NotImplementedError

    @abc.abstractmethod
    def load(self):
        """"""
