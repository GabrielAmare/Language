from core.langs.bnf.base_engine.processor import Processor
from core.langs.bnf.base_engine.tokenizer import tokenizer
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
