from base.building import builder
from core.langs.bnf.lang.models import Reader
from .processor import Processor
from .tokenizer import tokenizer

__all__ = [
    'make_engine'
]


def make_engine(reader: Reader, models: object, single_line_errors: bool = False, max_repeat_iterations: int = 100):
    tokenize = tokenizer(
        lexer=reader.lexer,
        make_list=True,
        single_line_errors=single_line_errors
    )
    process = Processor(
        reader=reader,
        max_repeat_iterations=max_repeat_iterations
    )
    build = builder(models)

    def read(text: str):
        tok = tokenize(text)
        ast = process(tok)
        obj = build(ast)

        return obj

    return read
