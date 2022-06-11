import typing

from base.decorators import *
from core.langs.bnf.lang.models import *


@__property__
def canonical(self: PatternGR) -> String:
    if isinstance(self, (StringPattern, KeywordPattern)):
        return self.expr

    elif isinstance(self, RegexPattern):
        raise Exception("No canonical form defined for RegexPattern.")

    else:
        raise NotImplementedError


@__property__
def is_optional(self: Buildable) -> bool:
    """Return True when the rule is optional (can be completed without matching any element)."""
    if isinstance(self, (Match, MatchAs, MatchIn, Literal)):
        return False

    elif isinstance(self, (Canonical, Optional, RepeatStar, Negative)):  # TODO : check that it is correct for Negative
        return True

    elif isinstance(self, Repeat):
        return Integer.to_int(self.mn) > 0

    elif isinstance(self, (Grouping, RepeatPlus, Branch, Alias)):
        return self.rule.is_optional

    elif isinstance(self, (Enum0, Enum1)):
        return self.element.is_optional and self.separator.is_optional

    elif isinstance(self, Sequence):
        return all(rule.is_optional for rule in self.rules)

    elif isinstance(self, Parallel):
        return any(rule.is_optional for rule in self.rules)

    elif isinstance(self, Group):
        return False  # TODO : should be implemented !

    else:
        raise NotImplementedError


@__property__
def first_matches(self: Buildable) -> typing.Set[Variable]:
    """Return the types that can be match as first element."""
    if isinstance(self, (Group, Canonical)):
        return set()

    elif isinstance(self, (Match, MatchAs, MatchIn)):
        return {self.type}

    elif isinstance(self, (Branch, Grouping, Repeat, RepeatStar, RepeatPlus, Optional, Negative)):
        return self.rule.first_matches

    elif isinstance(self, (Enum0, Enum1)):
        result = set()
        result = result.union(self.element.first_matches)
        if self.element.is_optional:
            result = result.union(self.separator.first_matches)
        return result

    elif isinstance(self, Sequence):
        result = set()
        for rule in self.rules:
            result = result.union(rule.first_matches)
            if not rule.is_optional:
                break
        return result

    elif isinstance(self, Parallel):
        result = set()
        for rule in self.rules:
            result = result.union(rule.first_matches)
        return result

    elif isinstance(self, (Literal, Alias)):
        return NotImplemented

    else:
        raise NotImplementedError


@__method__
def get_types(self: Parser, __type: Variable) -> list[Variable]:
    """Return the types referenced by the given `__type`"""
    if not self.has(__type):
        return [__type]

    toplevel = self.get(__type)

    if isinstance(toplevel, Group):
        return [
            type2
            for type1 in toplevel.types
            for type2 in self.get_types(type1)
        ]

    elif isinstance(toplevel, Branch):
        return [__type]

    elif isinstance(toplevel, Alias):
        raise TypeError("There should not remain any Alias when Parser.get_types is called.")

    else:
        raise NotImplementedError


@__method__
def get_recursion(self: Parser, __type: Variable) -> typing.Dict[Variable, bool]:
    group = self.get(__type)

    assert isinstance(group, Group)

    result = {}

    for sub_type in group.types:
        if self.has(sub_type):
            toplevel: BranchGR = self.get(sub_type)
            _value = group.type in toplevel.first_matches
        else:
            _value = False
        result[sub_type] = _value

    return result


@__method__
def is_element_of(self: Parser, group_type: Variable, element_type: str) -> bool:
    """Return True if the given element type is a sub type of the given group type."""
    return element_type in map(str, self.get_types(group_type))
