import dataclasses
import functools

from base.building import builder
from .base import Reader
from .processor import Processor
from .tokenizer import tokenizer

__all__ = [
    'Engine'
]


@dataclasses.dataclass
class Engine:
    reader: Reader
    models: object
    single_line_errors: bool = False
    max_repeat_iterations: int = 100

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
    def build(self):
        return builder(self.models)

    def __call__(self, text: str):
        tok = self.tokenize(text)
        ast = self.process(tok)
        obj = self.build(ast)
        return obj
