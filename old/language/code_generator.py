from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from website.language import python as py
from website.langs import javascript as js


class Code(ABC):
    @abstractmethod
    def to_python(self):
        """"""

    @abstractmethod
    def to_javascript(self):
        """"""


@dataclass(frozen=True, order=True)
class Integer(Code):
    content: str

    def to_python(self):
        return py.Integer(content=self.content)

    def to_javascript(self):
        return js.Integer(content=self.content)


@dataclass(frozen=True, order=True)
class String(Code):
    content: str

    def to_python(self) -> py.String:
        return py.String(content=self.content)

    def to_javascript(self) -> js.String:
        return js.String(content=self.content)


@dataclass(frozen=True, order=True)
class Append(Code):
    obj: Code
    item: Code

    def to_python(self) -> py.Call:
        return py.Call(
            left=py.GetAttr(
                left=self.obj.to_python(),
                right=py.Variable("append")
            ),
            args=[self.item.to_python()]
        )

    def to_javascript(self) -> js.Call:
        return js.Call(
            left=js.GetAttr(
                left=self.obj.to_javascript(),
                right=js.Variable("push")
            ),
            args=js.CallArgs(items=[
                self.item.to_javascript()
            ])
        )


@dataclass(frozen=True, order=True)
class Dict(Code):
    data: typing.Dict[str, Code]

    def to_python(self) -> py.Dict:
        return py.Dict([
            py.DictItem(key=py.String(content=repr(key)), value=value.to_python())
            for key, value in self.data.items()
        ])

    def to_javascript(self) -> js.Dict:
        return js.Dict([
            js.DictItem(key=js.Variable(content=key), right=value.to_javascript())
            for key, value in self.data.items()
        ])


@dataclass(frozen=True, order=True)
class Add(Code):
    left: Code
    right: Code

    def to_python(self) -> py.Add:
        return py.Add(left=self.left.to_python(), right=self.right.to_python())

    def to_javascript(self) -> js.Add:
        return js.Add(left=self.left.to_javascript(), right=self.right.to_javascript())


@dataclass(frozen=True, order=True)
class Sub(Code):
    left: Code
    right: Code

    def to_python(self) -> py.Sub:
        return py.Sub(left=self.left.to_python(), right=self.right.to_python())

    def to_javascript(self) -> js.Sub:
        return js.Sub(left=self.left.to_javascript(), right=self.right.to_javascript())


@dataclass(frozen=True, order=True)
class Eq(Code):
    left: Code
    right: Code

    def to_python(self) -> py.Eq:
        return py.Eq(left=self.left.to_python(), right=self.right.to_python())

    def to_javascript(self) -> js.Eq:
        return js.Eq(left=self.left.to_javascript(), right=self.right.to_javascript())


@dataclass(frozen=True, order=True)
class In(Code):
    item: Code
    iterable: Code

    def to_python(self) -> py.In:
        return py.In(
            left=self.item.to_python(),
            right=self.iterable.to_python()
        )

    def to_javascript(self) -> js.Call:
        return js.Call(
            left=js.GetAttr(
                left=self.iterable.to_javascript(),
                right=js.Variable("includes")
            ),
            args=js.CallArgs([
                self.item.to_javascript()
            ])
        )


@dataclass(frozen=True, order=True)
class If(Code):
    condition: Code
    block: Block
    alt: Code = None

    def to_python(self) -> py.If:
        return py.If(
            condition=self.condition.to_python(),
            block=self.block.to_python(),
            alt=self.alt.to_python() if self.alt else None
        )

    def to_javascript(self) -> js.If:
        return js.If(
            condition=self.condition.to_javascript(),
            block=self.block.to_javascript(),
            alt=self.alt.to_javascript() if self.alt else None
        )


@dataclass(frozen=True, order=True)
class Length(Code):
    obj: Code

    def to_python(self) -> py.Call:
        return py.Call(
            left=py.Variable("len"),
            args=[self.obj.to_python()]
        )

    def to_javascript(self) -> js.GetAttr:
        return js.GetAttr(
            left=self.obj.to_javascript(),
            right=js.Variable("length")
        )


@dataclass(frozen=True, order=True)
class ReturnList(Code):
    items: list[Code]

    def to_python(self) -> py.Return:
        return py.Return(py.ExprEnum([item.to_python() for item in self.items]))

    def to_javascript(self) -> js.Return:
        return js.Return(right=js.List(items=[item.to_javascript() for item in self.items]))


@dataclass(frozen=True, order=True)
class Return(Code):
    expr: Code

    def to_python(self) -> py.Return:
        return py.Return(self.expr.to_python())

    def to_javascript(self) -> js.Return:
        return js.Return(right=self.expr.to_javascript())


@dataclass(frozen=True, order=True)
class Variable(Code):
    name: str

    def to_python(self) -> py.Variable:
        return py.Variable(self.name)

    def to_javascript(self) -> js.Variable:
        return js.Variable(content=self.name)


@dataclass(frozen=True, order=True)
class AssignList(Code):
    vars: list[str]
    expr: Code

    def to_python(self) -> py.AssignTuple:
        return py.AssignTuple(
            args=[py.Variable(name) for name in self.vars],
            value=self.expr.to_python()
        )

    def to_javascript(self) -> js.Assign:
        return js.Assign(
            obj=js.VariableList(
                variables=[js.Variable(name) for name in self.vars]
            ),
            right=self.expr.to_javascript()
        )


@dataclass(frozen=True, order=True)
class Call(Code):
    obj: Code
    args: list[Code]

    def to_python(self) -> py.Call:
        return py.Call(
            left=self.obj.to_python(),
            args=[arg.to_python() for arg in self.args]
        )

    def to_javascript(self) -> js.Call:
        return js.Call(
            left=self.obj.to_javascript(),
            args=js.CallArgs(items=[arg.to_javascript() for arg in self.args])
        )


@dataclass(frozen=True, order=True)
class Block(Code):
    statements: list[Code]

    def to_python(self) -> py.Block:
        if self.statements:
            return py.Block([statement.to_python() for statement in self.statements])
        else:
            return py.Block([py.PassClass()])

    def to_javascript(self) -> js.Block:
        return js.Block([statement.to_javascript() for statement in self.statements])


@dataclass(frozen=True, order=True)
class Conditional(Code):
    cases: list[If]
    default: Block = None

    def to_python(self) -> py.If:
        if self.default:
            result = py.Else(block=self.default.to_python())
        else:
            result = None

        *items, last = reversed(self.cases)

        for item in items:
            assert item.alt is None
            result = py.Elif(condition=item.condition.to_python(), block=item.block.to_python(), alt=result)

        assert last.alt is None
        result = py.If(condition=last.condition.to_python(), block=last.block.to_python(), alt=result)

        return result

    def to_javascript(self) -> js.If:
        if self.default:
            result = js.Else(block=self.default.to_javascript())
        else:
            result = None

        *items, last = reversed(self.cases)

        for item in items:
            assert item.alt is None
            result = js.ElseIf(condition=item.condition.to_javascript(), block=item.block.to_javascript(), alt=result)

        assert last.alt is None
        result = js.If(condition=last.condition.to_javascript(), block=last.block.to_javascript(), alt=result)

        return result


@dataclass(frozen=True, order=True)
class Module(Code):
    statements: list[Code]

    def to_python(self) -> py.Module:
        return py.Module(
            # docstring=py.MultiLineString('""""""'),
            statements=[statement.to_python() for statement in self.statements]
        )

    def to_javascript(self) -> js.Module:
        return js.Module(statements=[
            statement.to_javascript() for statement in self.statements
        ])


@dataclass(frozen=True, order=True)
class Function(Code):
    name: str
    args: list[Code]
    block: Block

    def to_python(self) -> py.Def:
        return py.Def(
            name=py.Variable(self.name),
            args=[arg.to_python() for arg in self.args],
            rtype=None,
            block=self.block.to_python()
        )

    def to_javascript(self) -> js.Function:
        return js.Function(
            name=js.Variable(content=self.name),
            args=js.DefArgs(items=[arg.to_javascript() for arg in self.args]),
            block=self.block.to_javascript()
        )


@dataclass(frozen=True, order=True)
class Raise(Code):
    expr: Code

    def to_python(self) -> py.Raise:
        return py.Raise(expr=self.expr.to_python())

    def to_javascript(self) -> js.Throw:
        return js.Throw(right=self.expr.to_javascript())


@dataclass(frozen=True, order=True)
class VarAssign(Code):
    name: str
    value: Code

    def to_python(self) -> py.AnnAssign:
        return py.AnnAssign(
            target=py.Variable(self.name),
            value=self.value.to_python()
        )

    def to_javascript(self) -> js.Assign:
        return js.Assign(
            obj=js.Var(model=js.Variable(self.name)),
            right=self.value.to_javascript()
        )


@dataclass(frozen=True, order=True)
class ConstAssign(Code):
    name: str
    value: Code

    def to_python(self) -> py.AnnAssign:
        return py.AnnAssign(
            target=py.Variable(self.name),
            value=self.value.to_python()
        )

    def to_javascript(self) -> js.Assign:
        return js.Assign(
            obj=js.Const(model=js.Variable(self.name)),
            right=self.value.to_javascript()
        )


@dataclass(frozen=True, order=True)
class LetAssign(Code):
    name: str
    value: Code

    def to_python(self) -> py.AnnAssign:
        return py.AnnAssign(
            target=py.Variable(self.name),
            value=self.value.to_python()
        )

    def to_javascript(self) -> js.Assign:
        return js.Assign(
            obj=js.Let(model=js.Variable(self.name)),
            right=self.value.to_javascript()
        )


@dataclass(frozen=True, order=True)
class Assign(Code):
    name: str
    value: Code

    def to_python(self) -> py.AnnAssign:
        return py.AnnAssign(
            target=py.Variable(self.name),
            value=self.value.to_python()
        )

    def to_javascript(self) -> js.Assign:
        return js.Assign(
            obj=js.Variable(self.name),
            right=self.value.to_javascript()
        )


@dataclass(frozen=True, order=True)
class List(Code):
    items: list[Code]

    def to_python(self) -> py.List:
        return py.List(items=[item.to_python() for item in self.items])

    def to_javascript(self) -> js.List:
        return js.List(items=[item.to_javascript() for item in self.items])


@dataclass(frozen=True, order=True)
class ForEnumerate(Code):
    index: str
    item: str
    iterable: Code
    block: Block

    def to_python(self) -> py.For:
        return py.For(
            target=py.StarTargets(elts=[py.Variable(self.index), py.Variable(self.item)]),
            iterator=py.Call(
                left=py.Variable("enumerate"),
                args=[self.iterable.to_python()]
            ),
            block=self.block.to_python()
        )

    def to_javascript(self) -> js.ForOf:
        return js.ForOf(
            key=js.Var(model=js.VariableList(variables=[js.Variable(self.index), js.Variable(self.item)])),
            right=self.iterable.to_javascript(),
            block=self.block.to_javascript()
        )


@dataclass(frozen=True, order=True)
class While(Code):
    condition: Code
    block: Block

    def to_python(self):
        return py.While(
            condition=self.condition.to_python(),
            block=self.block.to_python()
        )

    def to_javascript(self):
        return js.While(
            condition=self.condition.to_javascript(),
            block=self.block.to_javascript()
        )


@dataclass(frozen=True, order=True)
class Export(Code):
    names: list[str]

    def to_python(self):
        return py.AnnAssign(
            target=py.Variable("__all__"),
            value=py.IndentedList(py.IndentedExprEnum([py.String(content=repr(name)) for name in self.names]))
        )

    def to_javascript(self):
        return js.Export(items=[js.Variable(name) for name in self.names])


@dataclass(frozen=True, order=True)
class TryCatch(Code):
    try_block: Block
    excepts: typing.Dict[str, Block]
    error_name: str = "e"

    def to_python(self) -> py.Try:
        return py.Try(
            block=self.try_block.to_python(),
            excepts=[
                py.Except(
                    error=py.Variable(error_type),
                    block=error_block.to_python(),
                    as_=py.Variable(self.error_name)
                )
                for error_type, error_block in self.excepts.items()
            ]
        )

    def to_javascript(self) -> js.Try:
        return js.Try(
            block=self.try_block.to_javascript(),
            catches=[
                js.Catch(
                    name=js.Variable(self.error_name),
                    right=js.InstanceOf(
                        left=js.Variable(self.error_name),
                        right=js.Variable(error_type)
                    ),
                    block=error_block.to_javascript()
                )
                for error_type, error_block in self.excepts.items()
            ]
        )


@dataclass(frozen=True, order=True)
class Docstring(Code):
    lines: list[str]

    def to_python(self):
        ...

    def to_javascript(self):
        """/**
            * Reduces a sequence of names to initials.
            * @param  {String} name  Space Delimited sequence of names.
            * @param  {String} sep   A period separating the initials.
            * @param  {String} trail A period ending the initials.
            * @param  {String} hyph  A hypen separating double names.
            * @return {String}       Properly formatted initials.
            */"""


@dataclass(frozen=True, order=True)
class __True(Code):
    def to_python(self) -> py.TrueClass:
        return py.TrueClass()

    def to_javascript(self) -> js.TrueClass:
        return js.TrueClass()


@dataclass(frozen=True, order=True)
class __False(Code):
    def to_python(self) -> py.FalseClass:
        return py.FalseClass()

    def to_javascript(self) -> js.FalseClass:
        return js.FalseClass()


@dataclass(frozen=True, order=True)
class __None(Code):
    def to_python(self) -> py.NoneClass:
        return py.NoneClass()

    def to_javascript(self) -> js.NullClass:
        return js.NullClass()


TRUE = __True()
FALSE = __False()
NONE = __None()
