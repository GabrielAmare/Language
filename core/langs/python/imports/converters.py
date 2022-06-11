import typing

from base.decorators import *
from core.langs.python.lang.base.models import *


@__method__
def to_str(self: String) -> str:
    return eval(self.content)


@__method__
def to_str(self: Variable) -> str:
    return self.content


@__class_method__
def from_str(cls: Variable.__class__, obj: typing.Optional[str]) -> typing.Optional[Variable]:
    if obj is None:
        return None

    return cls(content=obj)


@__class_method__
def from_str(cls: Comment.__class__, obj: typing.Optional[str]) -> typing.Optional[Comment]:
    if obj is None:
        return None

    return cls(content="# {}".format(obj))


@__class_method__
def from_str(cls: ImportPath.__class__, __value: str) -> ImportPath:
    """transform a path in """
    relatives = []

    while __value.startswith('...'):
        relatives.append(ImportEllipsis())
        __value = __value[3:]

    while __value.startswith('.'):
        relatives.append(ImportDot())
        __value = __value[1:]

    variables = []

    if __value:
        variables.extend(map(Variable, __value.split('.')))

    if relatives:
        return RelativeImportPath(relatives=relatives, variables=variables)

    elif variables:
        return AbsoluteImportPath(variables=variables)

    else:
        raise ValueError("Invalid empty path !")


@__class_method__
def from_value(cls: Constant.__class__, __value: object) -> Constant:
    if __value is None:
        return NONE
    elif __value is False:
        return FALSE
    elif __value is True:
        return TRUE
    elif isinstance(__value, int):
        return Integer(content=repr(__value))
    elif isinstance(__value, float):
        assert str(__value) not in ('inf', 'nan')
        return Float(content=repr(__value))
    elif isinstance(__value, str):
        return String(content=repr(__value))
    else:
        raise TypeError("Unsupported type to convert from.")
