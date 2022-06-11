import dataclasses

from base.decorators import *
from core.langs.bnf.lang.models import *


@__method__
def remove_canonicals(self: ParallelGR):
    """Remove `Canonical` objects from `self`."""
    if isinstance(self, MatchAs):
        return self
    elif isinstance(self, MatchIn):
        return self
    elif isinstance(self, Match):
        return self
    elif isinstance(self, Canonical):
        raise ValueError("`Canonical` objects must be removed.")
    elif isinstance(self, Literal):
        return self
    elif isinstance(self, Negative):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, Grouping):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, Repeat):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, RepeatStar):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, RepeatPlus):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, Optional):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, Enum0):
        try:
            element = self.element.remove_canonicals()
        except ValueError:
            element = None
        try:
            separator = self.separator.remove_canonicals()
        except ValueError:
            separator = None

        if element is None and separator is None:
            raise ValueError("`Enum` objects with only `Canonical` parts must be removed.")  # $X.$Y -> ValueError
        elif element is None:
            return RepeatStar(rule=separator)  # X.$Y -> $Y *[X $Y] -> *X
        elif separator is None:
            return RepeatPlus(rule=element)  # $Y.X -> X *[$Y X] -> +X
        else:
            return dataclasses.replace(self, element=element, separator=separator)

    elif isinstance(self, Enum1):
        try:
            element = self.element.remove_canonicals()
        except ValueError:
            element = None
        try:
            separator = self.separator.remove_canonicals()
        except ValueError:
            separator = None

        if element is None and separator is None:
            raise ValueError("`Enum` objects with only `Canonical` parts must be removed.")  # $X..$Y -> ValueError
        elif element is None:
            return RepeatStar(rule=separator)  # X..$Y -> $Y +[X $Y] -> +X
        elif separator is None:
            return Repeat(rule=element, mn=Integer('2'), mx=None)  # $Y..X -> X +[$Y X] -> {2,}X
        else:
            return dataclasses.replace(self, element=element, separator=separator)
    elif isinstance(self, Sequence):
        rules = []
        for rule in self.rules:
            try:
                rules.append(rule.remove_canonicals())
            except ValueError:
                continue

        if not rules:
            raise ValueError("`Sequence` objects with only `Canonical` parts must be removed.")

        return dataclasses.replace(self, rules=rules)
    elif isinstance(self, Parallel):
        rules = []
        for rule in self.rules:
            try:
                rules.append(rule.remove_canonicals())
            except ValueError:
                continue

        if not rules:
            raise ValueError("`Parallel` objects with only `Canonical` parts must be removed.")

        return dataclasses.replace(self, rules=rules)
    else:
        raise NotImplementedError


@__method__
def remove_canonicals(self: BranchGR) -> BranchGR:
    """Remove `Canonical` objects from `self`."""
    if isinstance(self, Branch):
        try:
            rule = self.rule.remove_canonicals()
        except ValueError:
            raise ValueError("Cannot build (empty branch) : " + repr(self))
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, (Group, Alias)):
        return self
    else:
        raise NotImplementedError


@__method__
def remove_canonicals(self: Parser) -> Parser:
    """Remove `Canonical` objects from `self`."""
    branches = []
    for branch in self.branches:
        try:
            branches.append(branch.remove_canonicals())
        except ValueError:
            # ignore non buildable branches
            continue
    return dataclasses.replace(self, branches=branches)


@__cached_property__
def remove_canonicals(self: Reader):
    """Remove `Canonical` objects from `self`."""
    parser = self.parser.remove_canonicals()
    return dataclasses.replace(self, parser=parser)
