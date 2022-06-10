import typing

from website.language.base.decorators import *
from website.language.semi.lang.models import *


@__class_method__
def from_rules(cls: Sequence.__class__, rules: typing.Iterator[ParallelGR]) -> SequenceGR:
    """Return a SequenceGR object for a list of rules applied in sequence."""
    final: list[RepeatGR] = []

    for rule in rules:
        for local in rule.split_sequence():
            if isinstance(local, Error):
                return Error()

            if isinstance(local, Valid):
                continue

            final.append(local)

    if len(final) == 0:
        return Valid()

    if len(final) == 1:
        return final[0]

    return cls(rules=final)


@__class_method__
def from_rules(cls: Parallel.__class__, rules: typing.Iterator[ParallelGR], eager: bool = False) -> ParallelGR:
    """Return a ParallelGR object for a list of rules applied in parallel."""
    final: list[SequenceGR] = []

    for rule in rules:
        for local in rule.split_parallel():
            if isinstance(local, Valid):
                if eager:
                    continue
                else:
                    return Valid()

            if isinstance(local, Error):
                continue

            final.append(local)

    if len(final) == 0:
        return Error()

    if len(final) == 1:
        return final[0]

    return cls(rules=final)


@__method__
def split_sequence(self: ParallelGR) -> list[RepeatGR]:
    """Return the list of rules applied in sequence that represent `self`."""
    if isinstance(self, Parallel):
        return [Grouping(self)]

    elif isinstance(self, Sequence):
        return self.rules

    elif isinstance(self, RepeatGR):
        return [self]

    else:
        raise NotImplementedError


@__method__
def split_parallel(self: ParallelGR) -> list[SequenceGR]:
    """Return the list of rules applied in parallel that represent `self`."""
    if isinstance(self, Parallel):
        return self.rules

    elif isinstance(self, SequenceGR):
        return [self]

    else:
        raise NotImplementedError


@__method__
def __and__(self: ParallelGR, other: ParallelGR) -> SequenceGR:
    return Sequence.from_rules([self, other])


@__method__
def __or__(self: ParallelGR, other: ParallelGR) -> ParallelGR:
    return Parallel.from_rules([self, other])


@__method__
def split_branch_set(self: BranchGR) -> list[Branch]:
    """Return the list of branches applied in parallel that represent `self`."""
    if isinstance(self, Branch):
        return [self]

    elif isinstance(self, BranchSet):
        return self.branches

    else:
        raise NotImplementedError


@__class_method__
def from_branches(cls: BranchSet.__class__, branches: typing.Iterator[BranchGR]) -> BranchSet:
    """Return a BranchSet object for a list of branches applied in parallel."""
    return cls(branches=[inner for outer in branches for inner in outer.split_branch_set()])
