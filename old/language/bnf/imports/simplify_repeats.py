import dataclasses

from website.language.base.decorators import *
from website.language.bnf.lang.models import *


# MatchKeyGR := MatchAs | MatchIn
# MatchGR := MatchKeyGR | Match
# AtomGR := Canonical | Literal | MatchGR # does not contain child rules
# GroupingGR := Grouping | AtomGR
# NegativeGR := Negative | GroupingGR
# RepeatGR := Repeat | RepeatStar | RepeatPlus | Optional | Enum0 | Enum1 | NegativeGR
# SequenceGR := Sequence | RepeatGR
# ParallelGR := Parallel | SequenceGR


@__method__
def simplify_repeats(self: ParallelGR):
    """Remove `Repeat` & `RepeatPlus` & `Enum0` & `Enum1` occurrences in `self`."""
    if isinstance(self, AtomGR):
        return self
    elif isinstance(self, Grouping):
        rule = self.rule.simplify_repeats()
        return rule
    elif isinstance(self, Negative):
        rule = self.rule.simplify_repeats()
        return Negative.from_rule(rule)
    elif isinstance(self, Repeat):
        # TODO*
        rule = self.rule.simplify_repeats()

        mn = Integer.to_int(self.mn)
        if mn == 0:
            # no required part
            required_part = None
        elif mn == 1:
            required_part = rule
        else:
            required_part = Sequence.from_rules(mn * [rule])

        mx = Integer.to_int(self.mx)
        if mx == 0:
            optional_part = RepeatStar.from_rule(rule)
        elif mx == 1:
            optional_part = Optional.from_rule(rule)
        else:
            optional_part = Optional.from_rule(rule)  # ?X
            for _ in range(mx - 1):
                optional_part = Optional.from_rule(rule & optional_part)  # ?(X curr)

        if required_part is None:
            return optional_part
        else:
            return required_part & optional_part

    elif isinstance(self, RepeatStar):
        rule = self.rule.simplify_repeats()
        return RepeatStar.from_rule(rule)
    elif isinstance(self, RepeatPlus):
        rule = self.rule.simplify_repeats()
        return rule & RepeatStar.from_rule(rule)
    elif isinstance(self, Optional):
        rule = self.rule.simplify_repeats()
        return Optional.from_rule(rule)
    elif isinstance(self, Enum0):
        element = self.element.simplify_repeats()
        separator = self.separator.simplify_repeats()
        return element & RepeatStar.from_rule(separator & element)
    elif isinstance(self, Enum1):
        element = self.element.simplify_repeats()
        separator = self.separator.simplify_repeats()
        return element & separator & element & RepeatStar.from_rule(separator & element)
    elif isinstance(self, Sequence):
        rules = [rule.simplify_repeats() for rule in self.rules]
        return Sequence.from_rules(rules)
    elif isinstance(self, Parallel):
        rules = [rule.simplify_repeats() for rule in self.rules]
        return Parallel.from_rules(rules)
    else:
        raise NotImplementedError


@__method__
def simplify_repeats(self: BranchGR) -> BranchGR:
    """Remove `Repeat` & `RepeatPlus` & `Enum0` & `Enum1` occurrences in `self`."""
    if isinstance(self, Branch):
        rule = self.rule.simplify_repeats()
        return dataclasses.replace(self, rule=rule)
    elif isinstance(self, (Group, Alias)):
        return self
    else:
        raise NotImplementedError


@__method__
def simplify_repeats(self: Parser) -> Parser:
    """Remove `Repeat` & `RepeatPlus` & `Enum0` & `Enum1` occurrences in `self`."""
    branches = [branch.simplify_repeats() for branch in self.branches]
    return dataclasses.replace(self, branches=branches)


@__cached_property__
def simplify_repeats(self: Reader):
    """Remove `Repeat` & `RepeatPlus` & `Enum0` & `Enum1` occurrences in `self`."""
    parser = self.parser.simplify_repeats()
    return dataclasses.replace(self, parser=parser)
