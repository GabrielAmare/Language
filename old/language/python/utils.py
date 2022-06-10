import typing

from website.language.python.lang.models import *

__all__ = [
    'LIBS',
    'IMPORTS',
    'TYPES',
    'FUNCS',
    'TYPING',
    'FUNCTOOLS',
    'ITERTOOLS',
    'COLLECTIONS',
    'DATACLASSES',
    'ABC',
    'EXCEPTIONS',
    'DECORATORS',
]


class LIBS:
    FUNCTOOLS = Variable("functools")
    ITERTOOLS = Variable("itertools")
    TYPING = Variable("typing")
    COLLECTIONS = Variable("collections")
    DATACLASSES = Variable("dataclasses")
    ABC = Variable("abc")


def _single_import(*names: Variable, as_name: typing.Optional[Variable] = None):
    return Import(targets=[
        DottedAsName(names=list(names), as_name=as_name)
    ])


class IMPORTS:
    FUNCTOOLS = _single_import(LIBS.FUNCTOOLS)
    ITERTOOLS = _single_import(LIBS.ITERTOOLS)
    TYPING = _single_import(LIBS.TYPING)
    COLLECTIONS = _single_import(LIBS.COLLECTIONS)
    DATACLASSES = _single_import(LIBS.DATACLASSES)
    ABC = _single_import(LIBS.ABC)


class TYPES:
    STR = Variable("str")
    INT = Variable("int")
    FLOAT = Variable("float")
    TYPE = Variable("type")
    BOOL = Variable("bool")
    CALLABLE = Variable("callable")
    DICT = Variable("dict")
    LIST = Variable("list")
    SET = Variable("set")
    FROZENSET = Variable("frozenset")


class FUNCS:
    ENUMERATE = Variable("enumerate")
    MAP = Variable("map")
    FILTER = Variable("filter")
    ISINSTANCE = Variable("isinstance")
    ISSUBCLASS = Variable("issubclass")
    REPR = Variable("repr")
    EVAL = Variable("eval")


class TYPING:
    ITERATOR = GetAttr(LIBS.TYPING, Variable("Iterator"))
    ITERABLE = GetAttr(LIBS.TYPING, Variable("Iterable"))
    OPTIONAL = GetAttr(LIBS.TYPING, Variable("Optional"))
    UNION = GetAttr(LIBS.TYPING, Variable("Union"))
    ANY = GetAttr(LIBS.TYPING, Variable("Any"))
    TYPE = GetAttr(LIBS.TYPING, Variable("Type"))

    TUPLE = GetAttr(LIBS.TYPING, Variable("Tuple"))
    DICT = GetAttr(LIBS.TYPING, Variable("Dict"))
    LIST = GetAttr(LIBS.TYPING, Variable("List"))
    SET = GetAttr(LIBS.TYPING, Variable("Set"))
    FROZEN_SET = GetAttr(LIBS.TYPING, Variable("FrozenSet"))


class FUNCTOOLS:
    SINGLE_DISPATCH = GetAttr(LIBS.FUNCTOOLS, Variable("singledispatch"))
    SINGLE_DISPATCH_METHOD = GetAttr(LIBS.FUNCTOOLS, Variable("singledispatchmethod"))


class ITERTOOLS:
    ...


class COLLECTIONS:
    ...


class DATACLASSES:
    DATACLASS = GetAttr(LIBS.DATACLASSES, Variable("dataclass"))
    FIELD = GetAttr(LIBS.DATACLASSES, Variable("field"))
    REPLACE = GetAttr(LIBS.DATACLASSES, Variable("replace"))


class ABC:
    ABC = GetAttr(LIBS.ABC, Variable("ABC"))
    ABSTRACT_METHOD = GetAttr(LIBS.ABC, Variable("abstractmethod"))


class EXCEPTIONS:
    EXCEPTION = Variable("Exception")
    INDEX_ERROR = Variable("IndexError")
    KEY_ERROR = Variable("KeyError")
    NOT_IMPLEMENTED_ERROR = Variable("NotImplementedError")


class DECORATORS:
    PROPERTY = Decorator(Variable('property'))
    CLASSMETHOD = Decorator(Variable('classmethod'))
    ABSTRACTMETHOD = Decorator(ABC.ABSTRACT_METHOD)  # requires `abc`
    SINGLE_DISPATCH = Decorator(FUNCTOOLS.SINGLE_DISPATCH)  # requires `functools`
    SINGLE_DISPATCH_METHOD = Decorator(FUNCTOOLS.SINGLE_DISPATCH_METHOD)  # requires `functools`
