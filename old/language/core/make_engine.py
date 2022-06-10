from website import console
from website.language.base.building import builder
from .processor import Processor
from .tokenizer import tokenizer

__all__ = [
    'make_engine'
]


def make_engine(
        reader,
        models,
        single_line_errors: bool = False,
        max_repeat_iterations: int = 100,
        debug: bool = False
):
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
        console.debug('~ tokenizing')
        tok = tokenize(text)

        console.debug('~ processing')
        ast = process(tok)

        console.debug('~ building')
        obj = build(ast)

        return obj

    return read
