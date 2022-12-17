import itertools
import typing

from .models import *

__all__ = [
    'engine',
    'build_group',
    'build_lemma',
    'build_token',
    'parallel',
    'sequence',
    'enum0',
    'enum1',
    'optional',
    'repeat0',
    'repeat1',
    'grouping',
    'canonical',
    'literal',
    'match_as',
    'match_char',
    'match_in',
]


def engine(
        tokens: dict[str, BuildGroup],
        lemmas: dict[str, BuildGroup],
        groups: dict[str, list[str]],
        entry: str,
) -> Engine:
    return Engine(
        rules=list(
            *itertools.starmap(build_token, tokens.items()),
            *itertools.starmap(build_lemma, lemmas.items()),
            *itertools.starmap(build_group, groups.items()),
        ),
        entry=Variable(entry)
    )


def build_group(__type: str, names: list[str]) -> BuildGroup:
    return BuildGroup(
        type=Variable(__type),
        refs=list(map(Variable, names)),
    )


def build_lemma(__type: str, rule: ParallelGR) -> BuildLemma:
    return BuildLemma(
        type=Variable(__type),
        rule=rule,
    )


def build_token(__type: str, rule: ParallelGR) -> BuildToken:
    return BuildToken(
        type=Variable(__type),
        rule=rule,
    )


def _split_parallel(rule: ParallelGR) -> typing.Iterator[RepeatGR]:
    if isinstance(rule, Parallel):
        yield from rule.rules
    else:
        yield rule


def parallel(*__rules: ParallelGR) -> ParallelGR:
    rules = []
    for outer in __rules:
        for inner in _split_parallel(outer):
            if inner not in rules:
                rules.append(inner)
    
    if len(rules) == 1:
        return rules[0]
    
    return Parallel(rules=list(rules))


def _split_sequence(rule: ParallelGR) -> typing.Iterator[RepeatGR]:
    if isinstance(rule, Parallel):
        yield grouping(rule)
    elif isinstance(rule, Sequence):
        yield from rule.rules
    else:
        yield rule


def sequence(*__rules: ParallelGR) -> SequenceGR:
    rules = []
    for outer in __rules:
        for inner in _split_sequence(outer):
            rules.append(inner)
    
    if len(rules) == 1:
        return rules[0]
    
    return Sequence(rules=list(rules))


def enum0(separator: ParallelGR, item: ParallelGR) -> Enum0:
    return Enum0(separator=grouping(separator), item=grouping(item))


def enum1(separator: ParallelGR, item: ParallelGR) -> Enum1:
    return Enum1(separator=grouping(separator), item=grouping(item))


def optional(rule: ParallelGR) -> RepeatGR:
    return Optional(grouping(rule))


def repeat0(rule: ParallelGR) -> Repeat0:
    return Repeat0(grouping(rule))


def repeat1(rule: ParallelGR) -> Repeat1:
    return Repeat1(grouping(rule))


def grouping(rule: ParallelGR) -> GroupingGR:
    if isinstance(rule, GroupingGR):
        return rule
    else:
        return Grouping(rule=rule)


def canonical(__expr: str) -> Canonical:
    return Canonical(expr=String(repr(__expr)))


def literal(__expr: str) -> Literal:
    return Literal(expr=String(repr(__expr)))


def match_as(__type: str, key: str) -> MatchAs:
    return MatchAs(
        type=Variable(__type),
        key=Variable(key),
    )


def match_in(__type: str, key: str) -> MatchIn:
    return MatchIn(
        type=Variable(__type),
        key=Variable(key),
    )


def match_char(__expr: str, inverted: bool = False) -> MatchChar:
    return MatchChar(
        charset=String(repr(''.join(sorted(set(__expr))))),
        inverted=INVERTED if inverted else None
    )