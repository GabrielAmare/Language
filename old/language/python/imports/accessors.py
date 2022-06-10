import queries
from website.language.base.decorators import *
from website.language.python.lang.models import *


@__property__
def q_statements(self: Module) -> queries.QueryList[Statement]:
    """Return the module statements as a `QueryList` object."""
    return queries.QueryList(self.statements)


@__property__
def classes(self: Module) -> queries.Query[Class]:
    """Filter the module statements to keep only `Class` objects."""
    return self.q_statements.instanceof(Class)


@__property__
def functions(self: Module) -> queries.Query[Def]:
    """Filter the module statements to keep only `Def` objects."""
    return self.q_statements.instanceof(Def)


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
