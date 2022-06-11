from core.langs.bnf.lang import models
from core.langs.bnf.lang.reader import reader

__all__ = [
    'engine'
]


def engine(text: str):
    from core.langs.bnf.base_engine import make_engine
    return make_engine(
        reader=reader.simplify(),
        models=models,
        single_line_errors=False,
        max_repeat_iterations=1000
    )(text)
