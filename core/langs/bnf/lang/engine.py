from .base import reader, models
from .maker import Engine

__all__ = [
    'engine'
]

engine = Engine(
    reader=reader.simplify(),
    models=models,
    single_line_errors=False,
    max_repeat_iterations=1000
)
