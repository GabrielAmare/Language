from core.langs.bnf import Engine
from . import models
from .reader import reader

__all__ = [
    'engine'
]

engine = Engine(
    reader=reader,
    models=models,
    single_line_errors=False,
    max_repeat_iterations=100,
    custom_build=models.ParallelGR.parse
)
