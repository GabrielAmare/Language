import typing

from .models import *

__all__ = [
    'pep8_e301',
    'pep8_e302',
]


def pep8_e301(statements: typing.Iterator[Statement]) -> typing.Iterator[Statement]:
    empty_count: int = 0
    prev: Statement | None = None
    
    for stmt in statements:
        if isinstance(prev, DecoratorGR) or (isinstance(stmt, DecoratorGR) and prev):
            while empty_count < 1:
                yield EMPTY_LINE
                empty_count += 1
        
        yield stmt
        
        # update prev
        if stmt is EMPTY_LINE:
            empty_count += 1
        else:
            prev = stmt
            empty_count = 0


def pep8_e302(statements: typing.Iterator[Statement]) -> typing.Iterator[Statement]:
    empty_count: int = 0
    prev: Statement | None = None
    
    for stmt in statements:
        if stmt is not EMPTY_LINE:
            if isinstance(prev, ImportFrom) and prev.origin == ImportPath([Variable('__future__')]) and stmt:
                while empty_count < 1:
                    yield EMPTY_LINE
                    empty_count += 1
            elif isinstance(prev, ImportStatement) and isinstance(stmt, Assign):
                while empty_count < 1:
                    yield EMPTY_LINE
                    empty_count += 1
            elif isinstance(prev, DecoratorGR) or (isinstance(stmt, DecoratorGR) and prev):
                while empty_count < 2:
                    yield EMPTY_LINE
                    empty_count += 1
        
        yield stmt
        
        # update prev
        if stmt is EMPTY_LINE:
            empty_count += 1
        else:
            prev = stmt
            empty_count = 0
    
    # Add one empty line at the end of a module.
    while empty_count < 1:
        yield EMPTY_LINE
        empty_count += 1
