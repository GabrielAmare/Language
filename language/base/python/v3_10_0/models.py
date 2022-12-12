from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Iterator

from language.base.abstract import Writable, tok

__all__ = [
    'AbstractGR',
    'Add',
    'And',
    'ArgumentGR',
    'Atom',
    'AwaitPrimary',
    'Awaited',
    'BitwiseAnd',
    'BitwiseAndGR',
    'BitwiseOr',
    'BitwiseOrGR',
    'BitwiseXor',
    'BitwiseXorGR',
    'Block',
    'Call',
    'Class',
    'Comparison',
    'Conjunction',
    'Decimal',
    'Decorator',
    'DecoratorGR',
    'Disjunction',
    'DoubleStarred',
    'Eq',
    'Expression',
    'FALSE',
    'Factor',
    'FloorDiv',
    'Function',
    'Ge',
    'GetAttr',
    'GetItem',
    'Gt',
    'In',
    'Integer',
    'Inv',
    'Inversion',
    'Is',
    'IsNot',
    'Kwarg',
    'LShift',
    'Le',
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
    'String',
    'Sub',
    'Sum',
    'TRUE',
    'Term',
    'TrueDiv',
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
    
    def __tokens__(self) -> Iterator[str]:
        for e in self.statements:
            yield '\n'
            yield from tok(e)


@dataclass
class Module(AbstractGR):
    statements: list[Statement]
    
    def __tokens__(self) -> Iterator[str]:
        if self.statements:
            for i, e in enumerate(self.statements):
                if i:
                    yield '\n'
                yield from tok(e)


@dataclass
class DecoratorGR(Statement, ABC):
    pass


@dataclass
class Expression(SliceGR, ArgumentGR, ABC):
    pass


@dataclass
class ReturningStatement(Statement, ABC):
    pass


@dataclass
class DoubleStarred(ArgumentGR):
    value: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield '**'
        yield from tok(self.value)


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
class Kwarg(ArgumentGR):
    name: Variable
    value: Expression
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.name)
        yield '='
        yield from tok(self.value)


@dataclass
class Disjunction(Expression, ABC):
    pass


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
    args: list[Expression]
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
class Conjunction(Disjunction, ABC):
    pass


@dataclass
class Or(Disjunction):
    left: Disjunction
    right: Conjunction
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield 'or'
        yield ' '
        yield from tok(self.right)


@dataclass
class Inversion(Conjunction, ABC):
    pass


@dataclass
class And(Conjunction):
    left: Conjunction
    right: Inversion
    
    def __tokens__(self) -> Iterator[str]:
        yield from tok(self.left)
        yield ' '
        yield 'and'
        yield ' '
        yield from tok(self.right)


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
class String(Atom):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)


@dataclass
class Variable(Atom):
    content: str
    
    def __tokens__(self) -> Iterator[str]:
        yield str(self.content)
