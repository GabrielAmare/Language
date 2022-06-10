from website.language.bnf.lang import models
from website.language.bnf.lang.reader import reader

__all__ = [
    'engine'
]


def engine(text: str):
    from website.language.core.make_engine import make_engine
    return make_engine(
        reader=reader.simplify(),
        models=models,
        single_line_errors=False,
        max_repeat_iterations=1000
    )(text)
