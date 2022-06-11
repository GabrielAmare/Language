from base.decorators import *
from core.langs.python.lang.base.models import *


@__property__
def classes(self: Module) -> list[Class]:
    """Filter the module statements to keep only `Class` objects."""
    return [statement for statement in self.statements if isinstance(statement, Class)]


@__property__
def functions(self: Module) -> list[Def]:
    """Filter the module statements to keep only `Def` objects."""
    return [statement for statement in self.statements if isinstance(statement, Def)]


@__method__
def get_class(self: Module, name: Variable) -> Class:
    """Return the class with the given `name`."""
    for cls in self.classes:
        if cls.name == name:
            return cls
    else:
        raise KeyError(name)


@__method__
def get_function(self: Module, name: Variable) -> Def:
    """Return the function with the given `name`."""
    for cls in self.functions:
        if cls.name == name:
            return cls
    else:
        raise KeyError(name)
