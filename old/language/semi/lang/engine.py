from website.language.base.building import builder
from website.language.core.processor import Processor
from website.language.core.tokenizer import tokenizer
from . import models
from .reader import reader

__all__ = [
    'engine'
]
_tokenize = tokenizer(lexer=reader.lexer, make_list=True, single_line_errors=False)
_process = Processor(reader=reader, max_repeat_iterations=100)
_build = builder(models)


def engine(text: str) -> models.BranchSet:
    tok = _tokenize(text)
    ast = _process(tok)
    obj = _build(ast)
    return obj
