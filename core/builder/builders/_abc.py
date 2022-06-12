import abc
import dataclasses

from core.builder.config import LangConfig

__all__ = [
    'AbstractBuilder',
    'TextBuilder',
    'JsonBuilder'
]


@dataclasses.dataclass
class AbstractBuilder(abc.ABC):
    config: LangConfig

    def option(self, __key: str, default: bool = False) -> bool:
        return self.config.option(__key, default)

    @abc.abstractmethod
    def build(self) -> object:
        """Return the file content."""


@dataclasses.dataclass
class TextBuilder(AbstractBuilder, abc.ABC):
    @abc.abstractmethod
    def build(self) -> str:
        """Return the text file content."""


@dataclasses.dataclass
class JsonBuilder(AbstractBuilder, abc.ABC):
    @abc.abstractmethod
    def build(self) -> dict:
        """Return the json file data."""
