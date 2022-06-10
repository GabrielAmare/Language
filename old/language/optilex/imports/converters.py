from website.language.base.decorators import *
from ..lang.models import *


@__class_method__
def from_int(cls: Integer.__class__, __value: int) -> Integer:
    return cls(content=repr(__value))


@__class_method__
def from_str(cls: Variable.__class__, __value: str) -> Variable:
    return cls(content=__value)


@__class_method__
def from_str(cls: String.__class__, __value: str) -> String:
    return cls(content=repr(__value))


@__property__
def value(self: Integer) -> int:
    return int(self.content)


@__property__
def value(self: String) -> str:
    return eval(self.content)



