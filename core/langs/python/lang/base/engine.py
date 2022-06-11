from core.langs.bnf import tokenizer, Processor
from . import models
from .reader import reader

__all__ = [
    'engine'
]
_tokenize = tokenizer(lexer=reader.lexer, make_list=True, single_line_errors=False)
_process = Processor(reader=reader, max_repeat_iterations=100)
_build = models.Module.parse


def engine(text: str) -> models.Module:
    tok = _tokenize(text)
    ast = _process(tok)
    obj = _build(ast)
    return obj
