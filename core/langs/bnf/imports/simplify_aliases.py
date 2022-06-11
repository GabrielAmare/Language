import dataclasses

from base.decorators import *
from core.langs.bnf.lang.models import *


@__method__
def simplify_aliases(self: ParallelGR, reader: Reader):
    """Return a simplified version of `self` without `Alias` objects."""
    if isinstance(self, Match):
        if reader.has(self.type):
            toplevel = reader.get(self.type)
            if isinstance(toplevel, Alias):
                return toplevel.rule.simplify_aliases(reader)

        return self

    elif isinstance(self, (Literal, MatchAs, MatchIn, Canonical)):
        return self

    elif isinstance(self, (Grouping, Repeat, RepeatStar, RepeatPlus, Optional, Negative)):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)

    elif isinstance(self, (Enum0, Enum1)):
        separator = self.separator.simplify_aliases(reader)
        element = self.element.simplify_aliases(reader)
        return dataclasses.replace(self, separator=separator, element=element)

    elif isinstance(self, (Sequence, Parallel)):
        rules = [rule.simplify_aliases(reader) for rule in self.rules]
        return dataclasses.replace(self, rules=rules)

    else:
        raise NotImplementedError


@__method__
def simplify_aliases(self: TopLevel, reader: Reader):
    """Return a simplified version of `self` without `Alias` objects."""
    if isinstance(self, (Group, PatternGR)):
        return self

    elif isinstance(self, Branch):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)

    elif isinstance(self, Alias):
        raise NotImplementedError("Alias.simplify_aliases() should never be called !")

    else:
        raise NotImplementedError


@__cached_property__
def simplify_aliases(self: Reader) -> Reader:
    """Return a simplified version of `self` without `Alias` objects."""
    branches = [
        branch.simplify_aliases(self)
        for branch in self.parser.branches
        if not isinstance(branch, Alias)
    ]
    parser = dataclasses.replace(self.parser, branches=branches)
    return dataclasses.replace(self, parser=parser)


@__method__
def simplify(self: Reader, **config) -> Reader:
    """Return a simplified version of `self` using `config` options."""
    simplified_reader: Reader = self
    if config.get('aliases'):
        simplified_reader = simplified_reader.simplify_aliases
    if config.get('literals'):
        simplified_reader = simplified_reader.simplify_literals
    if config.get('canonicals'):
        simplified_reader = simplified_reader.remove_canonicals
    if config.get('repeats'):
        simplified_reader = simplified_reader.simplify_repeats
    return simplified_reader
