import collections
import typing

from website.language.base.decorators import *
from website.language.bnf.lang.models import *


@__property__
def explicit_uses(self: TopLevel) -> typing.Iterator[Variable]:
    """Yields the types used explicitly in `self`. (Assumes that the `reader` has no `Alias` in it)"""
    if isinstance(self, Group):
        for sub_type in self.types:
            yield sub_type

    elif isinstance(self, Branch):
        for attribute in self.descriptor.attributes.values():
            for sub_type in attribute.types:
                yield Variable(sub_type)

    elif isinstance(self, Alias):
        raise NotImplementedError("Alias.explicit_uses should never be called !")

    elif isinstance(self, PatternGR):
        yield from []

    else:
        raise NotImplementedError


@__property__
def explicit_uses(self: Parser) -> typing.Iterator[Variable]:
    """Yields the types used explicitly in `self` branches."""
    for branch in self.branches:
        yield from branch.explicit_uses


@__method__
def get_uses(self: Reader) -> typing.Set[Variable]:
    done: typing.Set[Variable] = set()
    todo: typing.Deque[Variable] = collections.deque([self.parser.start])

    for branch in self.parser.branches:
        used_type = branch.type
        todo.append(used_type)

    while todo:
        item = todo.popleft()
        done.add(item)

        try:
            toplevel = self.get(item)
        except KeyError:
            continue  # type used but not defined !

        for used_type in toplevel.explicit_uses:
            if used_type not in done:
                todo.append(used_type)

    return done


@__property__
def def_count(self: Reader) -> typing.DefaultDict[str, int]:
    """Return the number of definitions for each type."""
    result: typing.DefaultDict[str, int] = collections.defaultdict(int)

    for pattern in self.lexer.patterns:
        result[str(pattern.type)] += 1

    for toplevel in self.parser.branches:
        result[str(toplevel.type)] += 1

    return result


@__property__
def use_count(self: Reader) -> typing.DefaultDict[str, int]:
    """Return the number of uses for each type. (assumes Alias have been removed)"""
    result: typing.DefaultDict[str, int] = collections.defaultdict(int)

    for toplevel in self.parser.branches:
        if isinstance(toplevel, Branch):
            for attribute in toplevel.descriptor.attributes.values():
                for _type in attribute.types:
                    result[_type] += 1
        elif isinstance(toplevel, Group):
            for _type in toplevel.types:
                result[str(_type)] += 1
        else:
            raise NotImplementedError(type(toplevel))

    return result


@__property__
def is_casted_pattern(self: TopLevel) -> bool:
    """Return True when the node refer to a casted `PatternGR` object."""
    if isinstance(self, PatternGR):
        return bool(self.cast)
    elif isinstance(self, (Group, Branch, Alias)):
        return False
    else:
        raise NotImplementedError


@__property__
def as_cast(self: Variable) -> str:
    if self.content == 'var':
        return 'str'
    elif self.content == 'str':
        return 'str'
    elif self.content == 'int':
        return 'int'
    elif self.content == 'float':
        return 'float'
    elif self.content == 'true':
        return 'bool'
    elif self.content == 'false':
        return 'bool'
    else:
        raise ValueError("Unable to convert " + repr(self) + "to a cast type.")


@__property__
def casted_type(self: TopLevel) -> str:
    """Return the correct casted type corresponding to `self`."""
    if isinstance(self, PatternGR):
        if isinstance(self.cast, Variable):
            return self.cast.as_cast
        else:
            return str(self.type)

    elif isinstance(self, (Group, Branch)):
        return str(self.type)

    elif isinstance(self, Alias):
        raise NotImplementedError("Alias objects does not have casted type.")

    else:
        raise NotImplementedError
