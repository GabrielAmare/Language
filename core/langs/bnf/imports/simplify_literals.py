import dataclasses
import string
import typing

from base.constants import SYMBOL_NAMES
from base.decorators import *
from core.langs.bnf.lang import *


@__property__
def is_keyword_expr(self: String) -> bool:
    """Return True if the string only contains letters."""
    return all(map(string.ascii_letters.__contains__, self.value))


@__property__
def is_symbols_expr(self: String) -> bool:
    """Return True if the string only contains symbols."""
    return all(map(SYMBOL_NAMES.__contains__, self.value))


@__method__
def as_pattern(self: Literal, __type: Variable) -> PatternGR:
    """Build the PatternGR object associated with `self`."""
    if self.expr.is_keyword_expr:
        return KeywordPattern(type=__type, expr=self.expr, priority=Integer('200'))
    elif self.expr.is_symbols_expr:
        return StringPattern(type=__type, expr=self.expr, priority=Integer('100'))
    else:
        # TODO : handle mixin patterns (those with both letters & symbols)
        #  it's important that the associated names are in bijection with the pattern expressions.
        raise NotImplementedError("Mixin patterns are not handled yet.")


@__method__
def simplify_literals(self: Buildable, literals: typing.Dict[Variable, Literal]):
    """Simplify a `Buildable` object, this turns the Literal objects into `Match` of `PatternGR`."""
    if isinstance(self, (Match, MatchAs, MatchIn, Canonical, Group)):
        return self

    elif isinstance(self, (Grouping, Repeat, RepeatStar, RepeatPlus, Optional, Branch, Negative, Alias)):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)

    elif isinstance(self, (Enum0, Enum1)):
        separator = self.separator.simplify_literals(literals)
        element = self.element.simplify_literals(literals)
        return dataclasses.replace(self, separator=separator, element=element)

    elif isinstance(self, (Sequence, Parallel)):
        rules = [rule.simplify_literals(literals) for rule in self.rules]
        return dataclasses.replace(self, rules=rules)

    elif isinstance(self, Literal):
        # """
        #     This function will include `self` into the `literals` dict.
        #     And replace `self` to be a `Match` of a `PatternGR`
        # """
        if self.expr.is_keyword_expr:
            pattern_type = Variable("KW_" + String.to_str(self.expr).upper())

        elif self.expr.is_symbols_expr:
            pattern_type = Variable('_'.join(map(SYMBOL_NAMES.__getitem__, String.to_str(self.expr))))

        else:
            raise NotImplementedError("cannot extrapolate name for expression : " + self.expr.content)

        if pattern_type in literals:
            assert literals[pattern_type] == self
        else:
            literals[pattern_type] = self

        return Match(type=pattern_type)

    else:
        raise NotImplementedError


@__cached_property__
def simplify_literals(self: Reader) -> Reader:
    """This method return the Reader where all the `Literal` instances are transformed into `Pattern` & `Match`."""
    literals: typing.Dict[Variable, Literal] = {}

    # this line will include all the literals into the `pattern_to_build` list
    branches = [branch.simplify_literals(literals) for branch in self.parser.branches]
    parser = dataclasses.replace(self.parser, branches=branches)

    new_patterns = [literal.as_pattern(name) for name, literal in literals.items()]
    patterns = new_patterns + self.lexer.patterns
    lexer = dataclasses.replace(self.lexer, patterns=patterns)

    return dataclasses.replace(self, lexer=lexer, parser=parser)
