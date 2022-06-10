import collections
import dataclasses
import operator
import typing

from website.language.base.decorators import *
from website.language.semi.lang.models import *


@__property__
def hash_order(self: ParallelGR) -> int:
    if isinstance(self, (Valid, Excluded, Error)):
        return 0
    elif isinstance(self, Match):
        return 1
    elif isinstance(self, Grouping):
        return 2
    elif isinstance(self, Repeat):
        return 3
    elif isinstance(self, Sequence):
        return 4
    elif isinstance(self, Parallel):
        return 5
    else:
        raise NotImplementedError


@__property__
def order_key(self: Branch) -> tuple[int, str, int]:
    return Integer.to_int(self.priority), Variable.to_str(self.type), self.rule.hash_order


@__property__
def order_key(self: BranchSet) -> tuple[int, tuple[tuple[int, str, int], ...]]:
    return len(self.branches), tuple(sorted(map(operator.attrgetter('order_key'), self.branches)))


@__property__
def canonical(self: ParallelGR) -> ParallelGR:
    """Return the canonical form of a rule."""
    # property : `obj.canonical.canonical == obj.canonical`
    # property : `obj.canonical` is processed the same as obj
    # use cases : to insure equality of objects processed the same way
    if isinstance(self, MatchGR):  # (Valid, Excluded, Error, Match)
        return self

    elif isinstance(self, Grouping):
        return self.rule.canonical

    elif isinstance(self, Repeat):
        return self.rule.canonical.as_repeat(mn=self.mn, mx=self.mx)

    elif isinstance(self, Sequence):
        return Sequence.from_rules(rule.canonical for rule in self.rules)

    elif isinstance(self, Parallel):
        rule_set = {rule.canonical for rule in self.rules}
        rules = sorted(rule_set, key=operator.attrgetter('hash_order'))
        return Parallel.from_rules(rules=rules)

    else:
        raise NotImplementedError


@__property__
def is_optional(self: Buildable) -> bool:
    """This means the Buildable can be constructed directly without more elements."""
    if isinstance(self, MatchGR):  # (Valid, Excluded, Error, Match)
        return False

    elif isinstance(self, (Grouping, Branch)):
        return self.rule.is_optional

    elif isinstance(self, Repeat):
        return Integer.to_int(self.mn) == 0

    elif isinstance(self, Sequence):
        return all(rule.is_optional for rule in self.rules)

    elif isinstance(self, Parallel):
        return any(rule.is_optional for rule in self.rules)

    elif isinstance(self, BranchSet):
        return all(branch.is_optional for branch in self.branches)

    else:
        raise NotImplementedError


@__property__
def alphabet(self: Buildable) -> typing.FrozenSet[str]:
    """Return the set of elements that can interact with the rule."""
    if isinstance(self, EmptyGR):
        return frozenset()

    elif isinstance(self, Match):
        return self.group_.to_frozenset()

    elif isinstance(self, (Grouping, Repeat, Branch)):
        return self.rule.alphabet

    elif isinstance(self, Sequence):
        # return frozenset.union(*(rule.alphabet for rule in self.rules))
        return frozenset(item for rule in self.rules for item in rule.alphabet)

    elif isinstance(self, Parallel):
        # return frozenset.union(*(rule.alphabet for rule in self.rules))
        return frozenset(item for rule in self.rules for item in rule.alphabet)

    elif isinstance(self, BranchSet):
        # return frozenset.union(*(branch.alphabet for branch in self.branches))
        return frozenset(item for branch in self.branches for item in branch.alphabet)

    else:
        raise NotImplementedError


@__method__
def repeat_minus_one(self: Repeat) -> typing.Union[Valid, Error, Repeat]:
    """Return the `self` with one loop step consumed."""
    mn = Integer.to_int(self.mn)
    mx = Integer.to_int(self.mx)

    if mx == 1:
        return Valid()

    mn = max(0, mn - 1)
    mx = max(0, mx - 1)

    return Repeat(
        rule=self.rule,
        mn=Integer.from_int(mn),
        mx=Integer.from_int(mx)
    )


@__property__
def is_terminal(self: BranchGR) -> bool:
    """Return True if `self` is terminal."""
    if isinstance(self, Branch):
        return isinstance(self.rule, (Valid, Error, Excluded))

    elif isinstance(self, BranchSet):
        return all(branch.is_terminal for branch in self.branches)

    else:
        raise NotImplementedError


@__property__
def can_be_processed(self: BranchGR) -> bool:
    """Return True if `self` can be processed."""
    # TODO : this method should be removed as soon as the `Error` class is removed.
    if isinstance(self, Branch):
        return not isinstance(self.rule, Error)

    elif isinstance(self, BranchSet):
        return not self.is_terminal

    else:
        raise NotImplementedError


@__property__
def simplified_step_1(self: BranchSet) -> BranchSet:
    """
        Return a simplified version of `self` where the branches
        sharing the same `type` & `priority` are merged in parallel.
    """
    data = collections.defaultdict(list)

    for branch in self.branches:
        key = branch.type, branch.priority
        data[key].append(branch.rule)

    branches = []
    for key, rules in data.items():
        type_ = key[0]
        priority = key[1]
        rule = Parallel.from_rules(rules)
        branch = Branch(type=type_, rule=rule, priority=priority)
        branches.append(branch)
    
    return BranchSet(branches=branches)


@__property__
def simplified_step_2(self: BranchSet) -> BranchSet:
    """"""
    included = []
    excluded = []

    for branch in self.branches:
        if isinstance(branch.rule, Error):
            continue

        if isinstance(branch.rule, Excluded):
            excluded.append(branch)

        else:
            included.append(branch)

    return BranchSet(branches=included or excluded)


@__property__
def simplified(self: BranchSet) -> BranchSet:
    """Return a simplified version of `self` which contains only the useful branches."""
    return self.simplified_step_1.simplified_step_2


@__method__
def split_branches(self: BranchSet) -> tuple[
    list[Branch], list[Branch], list[Branch], list[Branch]]:
    """Split the branches by types."""
    errors = []
    excluded = []
    included = []
    continued = []

    for branch in self.branches:
        if isinstance(branch.rule, Error):
            errors.append(branch)

        elif isinstance(branch.rule, Excluded):
            excluded.append(branch)

        elif isinstance(branch.rule, Valid):
            included.append(branch)

        else:
            continued.append(branch)

    return errors, excluded, included, continued


@__class_method__
def keep_max_priority(cls: Branch.__class__, branches: list[Branch]) -> list[Branch]:
    max_priority = max(Integer.to_int(branch.priority) for branch in branches)
    return [
        branch
        for branch in branches
        if Integer.to_int(branch.priority) == max_priority
    ]


@__method__
def process(self: ParallelGR) -> typing.Iterator[tuple[Group, ParallelGR]]:
    if isinstance(self, Valid):
        yield ALWAYS, EXCLUDED

    elif isinstance(self, Excluded):
        yield from []  # TODO : use () as a return value once the tuple are correctly handled.

    elif isinstance(self, Error):
        raise TypeError("`website.language.semi.models.Error` objects should not be processed.")

    elif isinstance(self, Match):
        yield self.group_, VALID

    elif isinstance(self, Grouping):
        yield from self.rule.process()

    elif isinstance(self, Repeat):
        then = self.repeat_minus_one()

        for group, rule in self.rule.process():
            yield group, Sequence.from_rules([rule, then])

    elif isinstance(self, Sequence):
        for index, base in enumerate(self.rules):
            then = Sequence.from_rules(self.rules[index + 1:])
            for group, rule in base.process():
                yield group, Sequence.from_rules([rule, then])

            if not base.is_optional:
                break

    elif isinstance(self, Parallel):
        for rule in self.rules:
            yield from rule.process()

    else:
        raise NotImplementedError


@__method__
def process(self: Branch) -> typing.Iterator[tuple[Group, Branch]]:
    data = collections.defaultdict(list)
    for group, rule in self.rule.process():
        data[group].append(rule)

    for group, rules in data.items():
        yield group, dataclasses.replace(self, rule=Parallel.from_rules(rules))

    if self.rule.is_optional:
        yield ALWAYS, dataclasses.replace(self, rule=EXCLUDED)


@__method__
def process(self: BranchSet) -> typing.Iterator[tuple[Group, BranchSet]]:
    data = collections.defaultdict(list)
    for i_branch in self.branches:
        for group, o_branch in i_branch.process():
            data[group].append(o_branch)

    for group, branches in data.items():
        yield group, BranchSet.from_branches(branches)


# TODO : remove when Error class is removed
@__property__
def pre_processed(self: BranchSet) -> BranchSet:
    """Treat `self` as an origin point."""
    return BranchSet.from_branches([branch for branch in self.branches if branch.can_be_processed])
