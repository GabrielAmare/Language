import functools
import typing

from base.decorators import *
from core.langs.python.lang.base.models import *


@__method__
def relative_level(self: RelativeImportPath) -> int:
    count = 0
    for relative in self.relatives:
        if isinstance(relative, ImportDot):
            count += 1
        elif isinstance(relative, ImportEllipsis):
            count += 3
        else:
            raise NotImplementedError
    return count


@__method__
def is_method(self: Def):
    return self.args and self.args[0].name == Variable('self')


@__method__
def is_class_method(self: Def):
    return self.args and self.args[0].name == Variable('cls')


@__method__
def get_argument(self: Def, name: Variable) -> DefArgumentGR:
    for arg in self.args:
        if arg.name == name:
            return arg

    else:
        raise KeyError(name)


@__method__
def is_empty(self: Block) -> bool:
    if not self.statements:
        return True

    for statement in self.statements:
        if isinstance(statement, (PassClass, EllipsisClass, EmptyLine)):
            continue
        else:
            return False
    else:
        return True


@__method__
def append_method(self: Class, method: Def) -> None:
    if not method.is_method() and not method.is_class_method():
        raise ValueError()

    if self.block.is_empty():
        self.block.statements.clear()

    if self.block.statements:
        self.block.statements.append(EmptyLine())

    self.block.statements.append(method)


@__method__
def flatten(self: If) -> tuple[list[Expression], list[Block], typing.Optional[Block]]:
    tests: list[Expression] = []
    codes: list[Block] = []
    default: typing.Optional[Block] = None

    curr = self

    while curr:
        if isinstance(curr, (If, Elif)):
            tests.append(curr.condition)
            codes.append(curr.block)
            curr = curr.alt

        elif isinstance(curr, Else):
            default = curr.block
            curr = None

        else:
            raise NotImplementedError

    return tests, codes, default


@__method__
def is_type_switch(self: Statement) -> bool:
    """Return True if the statement is a type switch."""
    if not isinstance(self, If):
        return False

    tests, cases, default = self.flatten()

    arg: typing.Optional[Expression] = None
    types: list[Expression] = []

    for index, test in enumerate(tests):
        # TODO : implement the case where we test for values like None `self is None` or `self is True` ?
        if not isinstance(test, Call):
            return False

        if test.left != Variable('isinstance'):
            return False

        if len(test.args) != 2:
            return False

        arg1, arg2 = test.args

        if not isinstance(arg1, Expression):
            return False

        if index == 0:
            arg = arg1

        elif arg != arg1:
            return False

        types.append(arg2)

    if arg is None:
        return False

    return True


@__method__
def as_type_switch(self: Statement) -> tuple[
    Expression,
    list[Expression],
    list[Block],
    typing.Optional[Block]
]:
    """Return True if the statement is a type switch."""
    _error = ValueError("not a type switch -> " + repr(str(self)))

    if not isinstance(self, If):
        raise _error

    tests, cases, default = self.flatten()

    arg: typing.Optional[Expression] = None
    types: list[Expression] = []

    for index, test in enumerate(tests):
        # TODO : implement the case where we test for values like None `self is None` or `self is True` ?
        if not isinstance(test, Call):
            raise _error

        if test.left != Variable('isinstance'):
            raise _error

        if len(test.args) != 2:
            raise _error

        arg1, arg2 = test.args

        if not isinstance(arg1, Expression):
            raise _error

        if index == 0:
            arg = arg1

        elif arg != arg1:
            raise _error

        types.append(arg2)

    if arg is None:
        raise _error

    return arg, types, cases, default


########################################################################################################################
# FUNCTIONS TO SIMPLIFY USAGE
########################################################################################################################

@__property__
def as_return(self: Returnable) -> Return:
    return Return(expr=self)


@__property__
def as_raise(self: Expression) -> Raise:
    return Raise(expr=self)


@__property__
def as_yield(self: Expression) -> Yield:
    return Yield(expr=self)


@__property__
def as_yield_from(self: Expression) -> YieldFrom:
    return YieldFrom(expr=self)


@__property__
def as_decorator(self: Expression) -> Decorator:
    return Decorator(expr=self)


@__method__
def as_call_arg(self: Variable, __value: Expression) -> NamedArgument:
    return NamedArgument(name=self, expr=__value)


@__method__
def as_def_arg(self: Variable,
               default: typing.Optional[Expression] = None,
               type_: typing.Optional[Expression] = None
               ) -> DefArgumentGR:
    return Argument(name=self, type=type_, default=default)


@__method__
def call(self: Primary, *args: CallArgumentGR) -> Call:
    return Call(left=self, args=list(args))


@__method__
def subscript(self: Primary, __other: Expression) -> Subscript:
    return Subscript(left=self, right=__other)


@__method__
def getattr(self: Primary, __other: typing.Union[str, Variable]) -> GetAttr:
    if isinstance(__other, str):
        __other = Variable(content=__other)
    return GetAttr(left=self, right=__other)


@__method__
def do_if(self: Block, test: Expression) -> If:
    return If(
        block=self,
        condition=test,
        alt=None
    )


@__method__
def do_for(self: Block, args: list[Variable], iterator: Expression) -> For:
    if len(args) == 0:
        raise NotImplementedError("Cant do a for loop without arguments.")

    elif len(args) == 1:
        target = args[0]

    else:
        target = StarTargets(elts=args)

    return For(
        block=self,
        target=target,
        iterator=iterator,
        alt=None
    )


@__class_method__
def sl_docstring(cls: String.__class__, __value: str) -> String:
    """Create a single-line docstring from a str `__value`."""
    return cls(content='"""' + __value + '"""')


@__class_method__
def _i_ml_docstring(cls: String.__class__, __value: str, level: int = 0) -> typing.Iterator[str]:
    """Return the tokens to build a multi-line docstring from a str `__value`."""
    if not __value.startswith('\n'):
        yield '\n'
    indent = level * '    '
    for index, line in enumerate(__value.split('\n')):
        if index:
            yield '\n'
        yield indent
        if line and not line.startswith('    '):
            yield '    '
        yield line
    if not __value.endswith('\n'):
        yield '\n'
    yield indent


@__class_method__
def ml_docstring(cls: String.__class__, __value: str, level: int = 0) -> String:
    """Create a multi-line docstring from a str `__value`."""
    return cls(content='"""' + ''.join(cls._i_ml_docstring(__value, level)) + '"""')


@__class_method__
def switch(cls: If.__class__, if_list: list[If], default: typing.Optional[Block]) -> If:
    if not if_list:
        raise ValueError("Can't build a switch without If instances.")

    if isinstance(default, Block):
        result = Else(block=default)
    else:
        result = None

    first_if = if_list[0]
    if_list = if_list[1:]

    for if_stmt in reversed(if_list):
        assert if_stmt.alt is None, "cannot make a switch with an if statement which already has an alt block."
        result = Elif(condition=if_stmt.condition, block=if_stmt.block, alt=result)

    return cls(condition=first_if.condition, block=first_if.block, alt=result)


@__class_method__
def from_list(cls: BitwiseOr.__class__, args: list[BitwiseXorGR]) -> BitwiseOrGR:
    if len(args) == 0:
        raise NotImplementedError

    if len(args) == 1:
        return args[0]

    return functools.reduce(cls, args)
