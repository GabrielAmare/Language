from .base import *

__all__ = [
    'for_loop',
    'assign',
    'switch',
    'value_eq_switch',
    'value_is_switch',
]

_STMT_LIST = list[Statement]


def for_loop(__tar: StarTargetsGR, __ite: Expression, __body: _STMT_LIST, __else: _STMT_LIST | None = None) -> For:
    return For(
        target=__tar,
        iterator=__ite,
        block=Block(__body),
        alt=Else(Block(__else)) if __else else None
    )


def assign(__tar: Primary, __val: Expression, __typ: Expression | None = None) -> AnnAssign:
    return AnnAssign(target=__tar, value=__val, annotation=__typ)


def switch(cases: list[tuple[Expression, Block]], default: Block | None = None) -> If:
    assert cases
    alt = Else(default) if default else None

    for condition, block in reversed(cases[1:]):
        alt = Elif(condition=condition, block=block, alt=alt)

    condition, block = cases[0]
    return If(condition=condition, block=block, alt=alt)


def value_eq_switch(value: Comparison, cases: list[tuple[BitwiseOrGR, Block]], default: Block | None = None) -> If:
    return switch(cases=[
        (Eq(left=value, right=expected_value), block)
        for expected_value, block in cases
    ], default=default)


def value_is_switch(value: Comparison, cases: list[tuple[BitwiseOrGR, Block]], default: Block | None = None) -> If:
    return switch(cases=[
        (Is(left=value, right=expected_value), block)
        for expected_value, block in cases
    ], default=default)


def instance_switch(value: Expression, cases: list[tuple[BitwiseOrGR, Block]], default: Block | None = None) -> If:
    return switch(cases=[
        (Variable('isinstance').call(value, expected_class), block)
        for expected_class, block in cases
    ], default=default)
