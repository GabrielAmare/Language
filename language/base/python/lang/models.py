from __future__ import annotations
import abc
import dataclasses
import typing

import language.base.abstract

__all__ = [
    'AbstractGR',
    'ArgumentGR',
    'SliceGR',
    'Statement',
    'Expression',
    'ReturningStatement',
    'Disjunction',
    'Conjunction',
    'Inversion',
    'Comparison',
    'BitwiseOrGR',
    'BitwiseXorGR',
    'BitwiseAndGR',
    'ShiftGR',
    'Sum',
    'Term',
    'Factor',
    'Power',
    'AwaitPrimary',
    'Primary',
    'Atom',
    'Module',
    'DoubleStarred',
    'Kwarg',
    'StarredExpression',
    'Slice',
    'Raise',
    'Return',
    'Yield',
    'YieldFrom',
    'Or',
    'And',
    'Not',
    'Eq',
    'Ge',
    'Gt',
    'In',
    'Is',
    'IsNot',
    'Le',
    'Lt',
    'Ne',
    'NotIn',
    'BitwiseOr',
    'BitwiseXor',
    'BitwiseAnd',
    'LShift',
    'RShift',
    'Add',
    'Sub',
    'FloorDiv',
    'MatMul',
    'Mod',
    'Mul',
    'TrueDiv',
    'Inv',
    'Neg',
    'Pos',
    'Pow',
    'Awaited',
    'Call',
    'GetAttr',
    'GetItem',
]


@dataclasses.dataclass
class AbstractGR(language.base.abstract.Writable, abc.ABC):
    pass


@dataclasses.dataclass
class ArgumentGR(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass
class SliceGR(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass
class Statement(AbstractGR, abc.ABC):
    pass


@dataclasses.dataclass
class Expression(SliceGR, ArgumentGR, abc.ABC):
    pass


@dataclasses.dataclass
class ReturningStatement(Statement, abc.ABC):
    pass


@dataclasses.dataclass
class Disjunction(Expression, abc.ABC):
    pass


@dataclasses.dataclass
class Conjunction(Disjunction, abc.ABC):
    pass


@dataclasses.dataclass
class Inversion(Conjunction, abc.ABC):
    pass


@dataclasses.dataclass
class Comparison(Inversion, abc.ABC):
    pass


@dataclasses.dataclass
class BitwiseOrGR(Comparison, abc.ABC):
    pass


@dataclasses.dataclass
class BitwiseXorGR(BitwiseOrGR, abc.ABC):
    pass


@dataclasses.dataclass
class BitwiseAndGR(BitwiseXorGR, abc.ABC):
    pass


@dataclasses.dataclass
class ShiftGR(BitwiseAndGR, abc.ABC):
    pass


@dataclasses.dataclass
class Sum(ShiftGR, abc.ABC):
    pass


@dataclasses.dataclass
class Term(Sum, abc.ABC):
    pass


@dataclasses.dataclass
class Factor(Term, abc.ABC):
    pass


@dataclasses.dataclass
class Power(Factor, abc.ABC):
    pass


@dataclasses.dataclass
class AwaitPrimary(Power, abc.ABC):
    pass


@dataclasses.dataclass
class Primary(AwaitPrimary, abc.ABC):
    pass


@dataclasses.dataclass
class Atom(Primary, abc.ABC):
    content: str


@dataclasses.dataclass
class Module(AbstractGR):
    statements: list[Statement]
    
    def __tokens__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.statements):
            if i:
                yield '\n'
            yield from e.__tokens__()


@dataclasses.dataclass
class DoubleStarred(ArgumentGR):
    value: Expression
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '**'
        yield from self.value.__tokens__()


@dataclasses.dataclass
class Kwarg(ArgumentGR):
    name: Variable
    value: Expression
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.name.__tokens__()
        yield '='
        yield from self.value.__tokens__()


@dataclasses.dataclass
class StarredExpression(ArgumentGR):
    value: Expression
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '*'
        yield from self.value.__tokens__()


@dataclasses.dataclass
class Slice(SliceGR):
    first: Expression | None = None
    second: Expression | None = None
    third: Expression | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        if self.first:
            yield from self.first.__tokens__()
        yield ':'
        if self.second:
            yield from self.second.__tokens__()
        if self.third:
            yield ':'
            yield from self.third.__tokens__()


@dataclasses.dataclass
class Raise(ReturningStatement):
    exc: Expression | None = None
    cause: Expression | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'raise'
        if self.exc and self.cause:
            yield ' '
            yield from self.exc.__tokens__()
            if self.cause:
                yield ' '
                yield 'from'
                yield ' '
                yield from self.cause.__tokens__()


@dataclasses.dataclass
class Return(ReturningStatement):
    expressions: list[Expression] | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'return'
        if self.expressions:
            yield ' '
            for i, e in enumerate(self.expressions):
                if i:
                    yield ','
                    yield ' '
                yield from e.__tokens__()


@dataclasses.dataclass
class Yield(ReturningStatement):
    expressions: list[Expression] | None = None
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'yield'
        if self.expressions:
            yield ' '
            for i, e in enumerate(self.expressions):
                if i:
                    yield ','
                    yield ' '
                yield from e.__tokens__()


@dataclasses.dataclass
class YieldFrom(ReturningStatement):
    expression: Expression
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'yield'
        yield ' '
        yield 'from'
        yield ' '
        yield from self.expression.__tokens__()


@dataclasses.dataclass
class Or(Disjunction):
    left: Disjunction
    right: Conjunction
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield 'or'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class And(Conjunction):
    left: Conjunction
    right: Inversion
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield 'and'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Not(Inversion):
    right: Inversion
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'not'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Eq(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '=='
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Ge(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '>='
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Gt(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '>'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class In(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield 'in'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Is(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield 'is'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class IsNot(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield 'is'
        yield ' '
        yield 'not'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Le(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '<='
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Lt(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '<'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Ne(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '!='
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class NotIn(Comparison):
    left: Comparison
    right: BitwiseOrGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield 'not'
        yield ' '
        yield 'in'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class BitwiseOr(BitwiseOrGR):
    left: BitwiseOrGR
    right: BitwiseXorGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '|'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class BitwiseXor(BitwiseXorGR):
    left: BitwiseXorGR
    right: BitwiseAndGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '^'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class BitwiseAnd(BitwiseAndGR):
    left: BitwiseAndGR
    right: ShiftGR
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '&'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class LShift(ShiftGR):
    left: ShiftGR
    right: Sum
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '<<'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class RShift(ShiftGR):
    left: ShiftGR
    right: Sum
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '>>'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Add(Sum):
    left: Sum
    right: Term
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '+'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Sub(Sum):
    left: Sum
    right: Term
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '-'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class FloorDiv(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '//'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class MatMul(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '@'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Mod(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '%'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Mul(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '*'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class TrueDiv(Term):
    left: Term
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '/'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Inv(Factor):
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '~'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Neg(Factor):
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '-'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Pos(Factor):
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield '+'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Pow(Power):
    left: AwaitPrimary
    right: Factor
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.left.__tokens__()
        yield ' '
        yield '**'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Awaited(AwaitPrimary):
    right: Primary
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield 'await'
        yield ' '
        yield from self.right.__tokens__()


@dataclasses.dataclass
class Call(Primary):
    obj: Primary
    args: list[ArgumentGR]
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.obj.__tokens__()
        yield '('
        for i, e in enumerate(self.args):
            if i:
                yield ','
                yield ' '
            yield from e.__tokens__()
        yield ')'


@dataclasses.dataclass
class GetAttr(Primary):
    obj: Primary
    name: Variable
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.obj.__tokens__()
        yield '.'
        yield from self.name.__tokens__()


@dataclasses.dataclass
class GetItem(Primary):
    obj: Primary
    items: list[SliceGR]
    
    def __tokens__(self) -> typing.Iterator[str]:
        yield from self.obj.__tokens__()
        yield '['
        for i, e in enumerate(self.items):
            if i:
                yield ','
                yield ' '
            yield from e.__tokens__()
        yield ']'
