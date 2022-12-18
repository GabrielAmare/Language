from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Iterator

from language.base.abstract import Writable, indented, tok

__all__ = [
    'AbstractGR',
    'Add',
    'AltGR',
    'And',
    'ArgsParam',
    'ArgumentGR',
    'Assign',
    'Atom',
    'AwaitPrimary',
    'Awaited',
    'BREAK',
    'BitwiseAnd',
    'BitwiseAndGR',
    'BitwiseOr',
    'BitwiseOrGR',
    'BitwiseXor',
    'BitwiseXorGR',
    'Block',
    'CONTINUE',
    'Call',
    'Class',
    'Comparison',
    'Conjunction',
    'Decimal',
    'Decorator',
    'DecoratorGR',
    'Disjunction',
    'DoubleStarred',
    'ELLIPSIS',
    'EMPTY_LINE',
    'Elif',
    'Else',
    'Eq',
    'Expression',
    'FALSE',
    'Factor',
    'FloorDiv',
    'For',
    'Function',
    'Ge',
    'GetAttr',
    'GetItem',
    'Gt',
    'If',
    'Import',
    'ImportFrom',
    'ImportPath',
    'ImportStatement',
    'In',
    'IndentedList',
    'IndentedListBody',
    'Integer',
    'Inv',
    'Inversion',
    'Is',
    'IsNot',
    'Kwarg',
    'KwargsParam',
    'LShift',
    'Le',
    'List',
    'Lt',
    'MatMul',
    'Mod',
    'Module',
    'Mul',
    'NONE',
    'Ne',
    'Neg',
    'Not',
    'NotIn',
    'Or',
    'PASS',
    'Param',
    'ParamGR',
    'Pos',
    'Pow',
    'Power',
    'Primary',
    'RShift',
    'Raise',
    'Return',
    'ReturningStatement',
    'ShiftGR',
    'Slice',
    'SliceGR',
    'StarredExpression',
    'Statement',
    'StatementExpression',
    'String',
    'Sub',
    'Sum',
    'TRUE',
    'Term',
    'TrueDiv',
    'Tuple',
    'Variable',
    'Yield',
    'YieldFrom',
]


@dataclass
class AbstractGR(Writable, ABC):
    pass


@dataclass
class ArgumentGR(AbstractGR, ABC):
    pass


@dataclass
class SliceGR(AbstractGR, ABC):
    pass


@dataclass
class Statement(AbstractGR, ABC):
    pass


@dataclass
class Block(AbstractGR):
    statements: list[Statement]
    
    @indented
    def __tokens__(self) -> Iterator[str]:
        for e in self.statements:
            yield '\n'
            yield from tok(e)


@dataclass
class IndentedListBody(AbstractGR):
    items: list[Expression]
    
    @indented
    def __tokens__(self) -> Iterator[str]:
        for e in self.items:
            yield '\n'
            yield from tok(e)
            yield ','


@dataclass
class Module(AbstractGR):
    statements: list[Statement]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.statements):
            if i:
                yield '\n'
            yield from tok(e)


@dataclass
class AltGR(AbstractGR, ABC):
    block: Block


@dataclass
class ImportPath(AbstractGR):
    parts: list[Variable]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.parts):
            if i:
                yield '.'
            yield from tok(e)


@dataclass
class ParamGR(AbstractGR, ABC):
    name: Variable
    type: Expression | None = None


@dataclass
class ArgsParam(ParamGR):
    def __tokens__(self) -> Iterator[str]:
        yield '*'
        yield from tok(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield from tok(self.type)


@dataclass
class DecoratorGR(Statement, ABC):
    pass


@dataclass
class Else(AltGR):
    def __tokens__(self) -> Iterator[str]:
        yield '\n'
        yield 'else'
        yield ':'
        yield from tok(self.block)


@dataclass
class Expression(ArgumentGR, SliceGR, ABC):
    pass


@dataclass
class KwargsParam(ParamGR):
    def __tokens__(self) -> Iterator[str]:
        yield '**'
        yield from tok(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield from tok(self.type)


@dataclass
class ReturningStatement(Statement, ABC):
    pass


@dataclass
class _Break(Statement):
    def __tokens__(self) -> Iterator[str]:
        yield 'break'


BREAK: _Break = _Break()


@dataclass
class _Continue(Statement):
    def __tokens__(self) -> Iterator[str]:
        yield 'continue'


CONTINUE: _Continue = _Continue()


@dataclass
class _EmptyLine(Statement):
    def __tokens__(self) -> Iterator[str]:
        yield ''


EMPTY_LINE: _EmptyLine = _EmptyLine()


@dataclass
class _Pass(Statement):
    def __tokens__(self) -> Iterator[str]:
        yield 'pass'


PASS: _Pass = _Pass()


@dataclass
class Assign(Statement):
    target: Primary
    type: Expression | None = None
    value: Expression | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.target)
        if self.type:
            yield ':'
            yield ' '
            yield from tok(self.type)
        if self.value:
            yield ' '
            yield '='
            yield ' '
            yield from tok(self.value)


@dataclass
class DoubleStarred(ArgumentGR):
    value: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield '**'
        yield from tok(self.value)


@dataclass
class Param(ParamGR):
    default: Expression | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield from tok(self.type)
        if self.default:
            yield ' '
            yield '='
            yield ' '
            yield from tok(self.default)


@dataclass
class Slice(SliceGR):
    first: Expression | None = None
    second: Expression | None = None
    third: Expression | None = None
    
    def __tokens__(self) -> Iterator[str]:
        if self.first:
            yield from tok(self.first)
        yield ':'
        if self.second:
            yield from tok(self.second)
        if self.third:
            yield ':'
            yield from tok(self.third)


@dataclass
class StarredExpression(ArgumentGR):
    value: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield '*'
        yield from tok(self.value)


@dataclass
class StatementExpression(Statement):
    expr: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.expr)


@dataclass
class For(Statement):
    iter: Expression
    block: Block
    args: list[Variable]
    
    def __tokens__(self) -> Iterator[str]:
        yield 'for'
        yield ' '
        for i, e in enumerate(self.args):
            if i:
                yield ','
                yield ' '
            yield from tok(e)
        yield ' '
        yield 'in'
        yield ' '
        yield from tok(self.iter)
        yield ':'
        yield from tok(self.block)


@dataclass
class Kwarg(ArgumentGR):
    name: Variable
    value: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.name)
        yield '='
        yield from tok(self.value)


@dataclass
class Elif(AltGR):
    test: Expression
    alt: AltGR | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield '\n'
        yield 'elif'
        yield ' '
        yield from tok(self.test)
        yield ':'
        yield from tok(self.block)
        if self.alt:
            yield from tok(self.alt)


@dataclass
class If(Statement):
    test: Expression
    block: Block
    alt: AltGR | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield 'if'
        yield ' '
        yield from tok(self.test)
        yield ':'
        yield from tok(self.block)
        if self.alt:
            yield from tok(self.alt)


@dataclass
class ImportStatement(Statement, ABC):
    targets: list[ImportPath]


@dataclass
class Disjunction(Expression, ABC):
    pass


@dataclass
class Import(ImportStatement):
    def __tokens__(self) -> Iterator[str]:
        yield 'import'
        yield ' '
        for i, e in enumerate(self.targets):
            if i:
                yield ','
                yield ' '
            yield from tok(e)


@dataclass
class Decorator(DecoratorGR):
    expr: Expression
    target: DecoratorGR
    
    def __tokens__(self) -> Iterator[str]:
        yield '@'
        yield from tok(self.expr)
        yield '\n'
        yield from tok(self.target)


@dataclass
class Raise(ReturningStatement):
    exc: Expression | None = None
    cause: Expression | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield 'raise'
        if self.exc:
            yield ' '
            yield from tok(self.exc)
            if self.cause:
                yield ' '
                yield 'from'
                yield ' '
                yield from tok(self.cause)


@dataclass
class Return(ReturningStatement):
    expressions: list[Expression] | None = field(default_factory=list)
    
    def __tokens__(self) -> Iterator[str]:
        yield 'return'
        if self.expressions:
            yield ' '
            for i, e in enumerate(self.expressions):
                if i:
                    yield ','
                    yield ' '
                yield from tok(e)


@dataclass
class Yield(ReturningStatement):
    expressions: list[Expression] | None = field(default_factory=list)
    
    def __tokens__(self) -> Iterator[str]:
        yield 'yield'
        if self.expressions:
            yield ' '
            for i, e in enumerate(self.expressions):
                if i:
                    yield ','
                    yield ' '
                yield from tok(e)


@dataclass
class YieldFrom(ReturningStatement):
    expr: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield 'yield'
        yield ' '
        yield 'from'
        yield ' '
        yield from tok(self.expr)


@dataclass
class Class(DecoratorGR):
    name: Variable
    block: Block
    mro: list[Expression] | None = field(default_factory=list)
    
    def __tokens__(self) -> Iterator[str]:
        yield 'class'
        yield ' '
        yield from tok(self.name)
        if self.mro:
            yield '('
            for i, e in enumerate(self.mro):
                if i:
                    yield ','
                    yield ' '
                yield from tok(e)
            yield ')'
        yield ':'
        yield from tok(self.block)


@dataclass
class Function(DecoratorGR):
    name: Variable
    block: Block
    args: list[ParamGR]
    returns: Expression | None = None
    
    def __tokens__(self) -> Iterator[str]:
        yield 'def'
        yield ' '
        yield from tok(self.name)
        yield '('
        for i, e in enumerate(self.args):
            if i:
                yield ','
                yield ' '
            yield from tok(e)
        yield ')'
        if self.returns:
            yield ' '
            yield '->'
            yield ' '
            yield from tok(self.returns)
        yield ':'
        yield from tok(self.block)


@dataclass
class ImportFrom(ImportStatement):
    origin: ImportPath
    
    def __tokens__(self) -> Iterator[str]:
        yield 'from'
        yield ' '
        yield from tok(self.origin)
        yield ' '
        yield 'import'
        yield ' '
        for i, e in enumerate(self.targets):
            if i:
                yield ','
                yield ' '
            yield from tok(e)


@dataclass
class Conjunction(Disjunction, ABC):
    pass


@dataclass
class Or(Disjunction):
    items: list[Conjunction]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.items):
            if i:
                yield ' '
                yield 'or'
                yield ' '
            yield from tok(e)


@dataclass
class Inversion(Conjunction, ABC):
    pass


@dataclass
class And(Conjunction):
    items: list[Inversion]
    
    def __tokens__(self) -> Iterator[str]:
        for i, e in enumerate(self.items):
            if i:
                yield ' '
                yield 'and'
                yield ' '
            yield from tok(e)


@dataclass
class Comparison(Inversion, ABC):
    pass


@dataclass
class Not(Inversion):
    right: Inversion
    
    def __tokens__(self) -> Iterator[str]:
        yield 'not'
        yield from tok(self.right)


@dataclass
class BitwiseOrGR(Comparison, ABC):
    pass


@dataclass
class Eq(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '=='
        yield ' '
        yield from tok(self.right)


@dataclass
class Ge(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '>='
        yield ' '
        yield from tok(self.right)


@dataclass
class Gt(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '>'
        yield ' '
        yield from tok(self.right)


@dataclass
class In(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield 'in'
        yield ' '
        yield from tok(self.right)


@dataclass
class Is(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield 'is'
        yield ' '
        yield from tok(self.right)


@dataclass
class IsNot(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield 'is'
        yield ' '
        yield 'not'
        yield ' '
        yield from tok(self.right)


@dataclass
class Le(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '<='
        yield ' '
        yield from tok(self.right)


@dataclass
class Lt(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '<'
        yield ' '
        yield from tok(self.right)


@dataclass
class Ne(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '!='
        yield ' '
        yield from tok(self.right)


@dataclass
class NotIn(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield 'not'
        yield ' '
        yield 'in'
        yield ' '
        yield from tok(self.right)


@dataclass
class BitwiseXorGR(BitwiseOrGR, ABC):
    pass


@dataclass
class BitwiseOr(BitwiseOrGR):
    left: BitwiseOrGR
    right: BitwiseXorGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '|'
        yield ' '
        yield from tok(self.right)


@dataclass
class BitwiseAndGR(BitwiseXorGR, ABC):
    pass


@dataclass
class BitwiseXor(BitwiseXorGR):
    left: BitwiseXorGR
    right: BitwiseAndGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '^'
        yield ' '
        yield from tok(self.right)


@dataclass
class ShiftGR(BitwiseAndGR, ABC):
    pass


@dataclass
class BitwiseAnd(BitwiseAndGR):
    left: BitwiseAndGR
    right: ShiftGR
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '&'
        yield ' '
        yield from tok(self.right)


@dataclass
class Sum(ShiftGR, ABC):
    pass


@dataclass
class LShift(ShiftGR):
    left: ShiftGR
    right: Sum
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '<<'
        yield ' '
        yield from tok(self.right)


@dataclass
class RShift(ShiftGR):
    left: ShiftGR
    right: Sum
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '>>'
        yield ' '
        yield from tok(self.right)


@dataclass
class Term(Sum, ABC):
    pass


@dataclass
class Add(Sum):
    left: Sum
    right: Term
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '+'
        yield ' '
        yield from tok(self.right)


@dataclass
class Sub(Sum):
    left: Sum
    right: Term
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '-'
        yield ' '
        yield from tok(self.right)


@dataclass
class Factor(Term, ABC):
    pass


@dataclass
class FloorDiv(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '//'
        yield ' '
        yield from tok(self.right)


@dataclass
class MatMul(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '@'
        yield ' '
        yield from tok(self.right)


@dataclass
class Mod(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '%'
        yield ' '
        yield from tok(self.right)


@dataclass
class Mul(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '*'
        yield ' '
        yield from tok(self.right)


@dataclass
class TrueDiv(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '/'
        yield ' '
        yield from tok(self.right)


@dataclass
class Power(Factor, ABC):
    pass


@dataclass
class Inv(Factor):
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield '~'
        yield from tok(self.right)


@dataclass
class Neg(Factor):
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield '-'
        yield from tok(self.right)


@dataclass
class Pos(Factor):
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield '+'
        yield from tok(self.right)


@dataclass
class AwaitPrimary(Power, ABC):
    pass


@dataclass
class Pow(Power):
    left: AwaitPrimary
    right: Factor
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield '**'
        yield ' '
        yield from tok(self.right)


@dataclass
class Primary(AwaitPrimary, ABC):
    pass


@dataclass
class Awaited(AwaitPrimary):
    right: Primary
    
    def __tokens__(self) -> Iterator[str]:
        yield 'await'
        yield ' '
        yield from tok(self.right)


@dataclass
class Atom(Primary, ABC):
    pass


@dataclass
class Call(Primary):
    left: Primary
    args: list[ArgumentGR]
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield '('
        for i, e in enumerate(self.args):
            if i:
                yield ','
                yield ' '
            yield from tok(e)
        yield ')'


@dataclass
class GetItem(Primary):
    left: Primary
    items: list[SliceGR]
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield '['
        for i, e in enumerate(self.items):
            if i:
                yield ','
                yield ' '
            yield from tok(e)
        yield ']'


@dataclass
class GetAttr(Primary):
    left: Primary
    right: Variable
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield '.'
        yield from tok(self.right)


@dataclass
class _Ellipsis(Atom):
    def __tokens__(self) -> Iterator[str]:
        yield '...'


ELLIPSIS: _Ellipsis = _Ellipsis()


@dataclass
class _False(Atom):
    def __tokens__(self) -> Iterator[str]:
        yield 'False'


FALSE: _False = _False()


@dataclass
class _None(Atom):
    def __tokens__(self) -> Iterator[str]:
        yield 'None'


NONE: _None = _None()


@dataclass
class _True(Atom):
    def __tokens__(self) -> Iterator[str]:
        yield 'True'


TRUE: _True = _True()


@dataclass
class Decimal(Atom):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass
class Integer(Atom):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass
class List(Atom):
    items: list[Expression] | None = field(default_factory=list)
    
    def __tokens__(self) -> Iterator[str]:
        yield '['
        if self.items:
            for i, e in enumerate(self.items):
                if i:
                    yield ','
                    yield ' '
                yield from tok(e)
        yield ']'


@dataclass
class String(Atom):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass
class Tuple(Atom):
    items: list[Expression]
    
    def __tokens__(self) -> Iterator[str]:
        yield '('
        for i, e in enumerate(self.items):
            if i:
                yield ','
                yield ' '
            yield from tok(e)
        yield ')'


@dataclass
class Variable(Atom):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass
class IndentedList(Atom):
    body: IndentedListBody
    
    def __tokens__(self) -> Iterator[str]:
        yield '['
        yield from tok(self.body)
        yield '\n'
        yield ']'
