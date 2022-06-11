import typing

from base.decorators import *
from core.langs.bnf.lang import *


@__property__
def value(self: String) -> str:
    return eval(self.content)


@__property__
def value(self: Integer) -> int:
    return int(self.content)


@__method__
def has(self: Lexer, var: Variable) -> bool:
    for toplevel in self.patterns:
        if toplevel.type == var:
            return True

    else:
        return False


@__method__
def get(self: Lexer, var: Variable) -> PatternGR:
    for toplevel in self.patterns:
        if toplevel.type == var:
            return toplevel

    else:
        raise KeyError(var)


@__method__
def has(self: Parser, var: Variable) -> bool:
    for toplevel in self.branches:
        if toplevel.type == var:
            return True
    else:
        return False


@__method__
def get(self: Parser, var: Variable) -> BranchGR:
    for toplevel in self.branches:
        if toplevel.type == var:
            return toplevel
    else:
        raise KeyError(var)


@__method__
def has(self: Reader, var: Variable) -> bool:
    if self.parser.has(var):
        return True

    elif self.lexer.has(var):
        return True

    else:
        return False


@__method__
def get(self: Reader, var: Variable) -> TopLevel:
    if self.parser.has(var):
        return self.parser.get(var)

    elif self.lexer.has(var):
        return self.lexer.get(var)

    else:
        raise KeyError(var)


@__method__
def get_classes(self: Parser) -> typing.Dict[Variable, BranchGR]:
    return {
        toplevel.type: toplevel
        for toplevel in self.branches
        if not isinstance(toplevel, Alias)
    }
