import dataclasses
import functools
import typing

from base.building import builder
from base.processing import Element
from .base.models import Reader
from .processor import Processor
from .tokenizer import tokenizer

__all__ = [
    'Engine'
]

R = typing.TypeVar('R')


@dataclasses.dataclass
class Engine(typing.Generic[R]):
    reader: Reader
    models: object
    single_line_errors: bool = False
    max_repeat_iterations: int = 100
    custom_build: typing.Callable[[Element], R] | None = None

    @functools.cached_property
    def tokenize(self):
        return tokenizer(
            lexer=self.reader.lexer,
            make_list=True,
            single_line_errors=self.single_line_errors
        )

    @functools.cached_property
    def process(self) -> Processor:
        return Processor(
            reader=self.reader,
            max_repeat_iterations=self.max_repeat_iterations
        )

    @functools.cached_property
    def build(self) -> typing.Callable[[Element], R]:
        if self.custom_build:
            return self.custom_build
        else:
            return builder(self.models)

    def __call__(self, text: str) -> R:
        tok = self.tokenize(text)
        ast = self.process(tok)
        obj = self.build(ast)
        return obj
