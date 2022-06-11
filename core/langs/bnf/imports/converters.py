from base.decorators import *
from core.langs.bnf.lang import *


@__method__
def to_int(self: Integer) -> int:
    if isinstance(self, Integer):
        return int(self.content)

    return 0


@__method__
def to_bool(self: Ignore) -> bool:
    if isinstance(self, Ignore):
        return True

    return False


@__method__
def to_str(self: String) -> str:
    if isinstance(self, String):
        return eval(self.content)

    return ''


@__method__
def to_str(self: Variable) -> str:
    if isinstance(self, Variable):
        return self.content

    return ''


@__property__
def as_grouping(self: ParallelGR) -> GroupingGR:
    """Transform `self` such as it becomes a `GroupingGR` object."""
    if isinstance(self, (Negative, Repeat, RepeatStar, RepeatPlus, Optional, Enum0, Enum1, Sequence, Parallel)):
        return Grouping(rule=self)
    elif isinstance(self, GroupingGR):
        return self
    else:
        raise NotImplementedError


@__property__
def as_sequence_rules(self: ParallelGR) -> list[RepeatGR]:
    """Consider `self` as a `Sequence` and return its child rules."""
    if isinstance(self, Sequence):
        return self.rules
    elif isinstance(self, (Repeat, RepeatStar, RepeatPlus, Optional, Enum0, Enum1, Negative, AtomGR)):
        return [self]
    elif isinstance(self, Grouping):
        return self.rule.as_sequence_rule
    elif isinstance(self, Parallel):
        return [Grouping(rule=self)]
    else:
        raise NotImplementedError


@__property__
def as_parallel_rules(self: ParallelGR) -> list[SequenceGR]:
    """Consider `self` as a `Parallel` and return its child rules."""
    # TODO : handle the case of Grouping.rule -> ParallelGR
    if isinstance(self, Parallel):
        return self.rules
    elif isinstance(self, (Sequence, Repeat, RepeatStar, RepeatPlus, Optional, Enum0, Enum1, Negative, AtomGR)):
        return [self]
    elif isinstance(self, Grouping):
        return self.rule.as_parallel_rules
    else:
        raise NotImplementedError


@__method__
def __and__(self: ParallelGR, other: ParallelGR) -> SequenceGR:
    rules = []
    rules.extend(self.as_sequence_rules)
    rules.extend(other.as_sequence_rules)

    if len(rules) == 1:
        return rules[0]

    return Sequence(rules=rules)


@__method__
def __or__(self: ParallelGR, other: ParallelGR) -> ParallelGR:
    rules = []
    rules.extend(self.as_parallel_rules)
    rules.extend(other.as_parallel_rules)

    if len(rules) == 1:
        return rules[0]

    return Parallel(rules=rules)


@__class_method__
def from_rules(cls: Parallel.__class__, rules: list[ParallelGR]) -> ParallelGR:
    final = []
    for rule in rules:
        final.extend(rule.as_parallel_rules)

    if len(final) == 1:
        return final[0]

    return cls(rules=final)


@__class_method__
def from_rules(cls: Sequence.__class__, rules: list[ParallelGR]) -> SequenceGR:
    final = []
    for rule in rules:
        final.extend(rule.as_sequence_rules)

    if len(final) == 1:
        return final[0]

    return cls(rules=final)


@__class_method__
def from_rule(cls: RepeatStar.__class__, rule: ParallelGR) -> RepeatStar:
    return cls(rule=rule.as_grouping)


@__class_method__
def from_rule(cls: RepeatPlus.__class__, rule: ParallelGR) -> RepeatPlus:
    return cls(rule=rule.as_grouping)


@__class_method__
def from_rule(cls: Optional.__class__, rule: ParallelGR) -> Optional:
    return cls(rule=rule.as_grouping)


@__class_method__
def from_rule(cls: Negative.__class__, rule: ParallelGR) -> Negative:
    return cls(rule=rule.as_grouping)
