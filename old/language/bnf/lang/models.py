"""
    This module has been auto-generated. Do not change manually.
    WARNING : Manual changes to this file are likely to be overwritten.
"""
from __future__ import annotations

import abc
import collections
import dataclasses
import functools
import operator
import string
import typing

from website.language.base.constants import SYMBOL_NAMES
from website.language.base.models import Attribute, Descriptor

__all__ = [
    'Alias',
    'All',
    'AtomGR',
    'Branch',
    'BranchGR',
    'Buildable',
    'Canonical',
    'Enum0',
    'Enum1',
    'Group',
    'Grouping',
    'GroupingGR',
    'Ignore',
    'Integer',
    'KeywordPattern',
    'Lexer',
    'Literal',
    'Match',
    'MatchAs',
    'MatchGR',
    'MatchIn',
    'MatchKeyGR',
    'Negative',
    'NegativeGR',
    'Optional',
    'Parallel',
    'ParallelGR',
    'Parser',
    'PatternGR',
    'Reader',
    'RegexPattern',
    'Repeat',
    'RepeatGR',
    'RepeatPlus',
    'RepeatStar',
    'Sequence',
    'SequenceGR',
    'String',
    'StringPattern',
    'TopLevel',
    'Variable'
]


def _flat_str(method):
    def wrapped(self) -> str:
        return ''.join(method(self))
    return wrapped


@dataclasses.dataclass(frozen=True, order=True)
class All(abc.ABC):
    """
        >>> String  # atomic
        >>> Variable  # atomic
        >>> Integer  # atomic
        >>> Ignore  # concrete
        >>> TopLevel  # abstract
        >>> Buildable  # abstract
        >>> Lexer  # concrete
        >>> Parser  # concrete
        >>> Reader  # concrete
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Buildable(All, abc.ABC):
    """
        >>> BranchGR  # abstract
        >>> ParallelGR  # abstract
    """
    
    @property
    @abc.abstractmethod
    def is_optional(self) -> bool:
        """Return True when the rule is optional (can be completed without matching any element)."""
    
    @property
    @abc.abstractmethod
    def first_matches(self) -> typing.Set[Variable]:
        """Return the types that can be match as first element."""
    
    @abc.abstractmethod
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        """Simplify a `Buildable` object, this turns the Literal objects into `Match` of `PatternGR`."""


@dataclasses.dataclass(frozen=True, order=True)
class Ignore(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Ignore := <KW_IGNORE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'ignore'
    
    def to_bool(self) -> bool:
        if isinstance(self, Ignore):
            return True
        return False


@dataclasses.dataclass(frozen=True, order=True)
class Integer(All):
    """
        This class has been generated automatically from the bnf rule :
        regex   Integer '\\-?\\d+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @property
    def value(self) -> int:
        return int(self.content)
    
    def to_int(self) -> int:
        if isinstance(self, Integer):
            return int(self.content)
        return 0


@dataclasses.dataclass(frozen=True, order=True)
class Lexer(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Lexer := $'\\n'.<PatternGR in patterns>
    """
    patterns: list[PatternGR]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.patterns:
            for i, e in enumerate(self.patterns):
                if i:
                    yield '\n'
                yield str(e)
    
    def has(self, var: Variable) -> bool:
        for toplevel in self.patterns:
            if toplevel.type == var:
                return True
        else:
            return False
    
    def get(self, var: Variable) -> PatternGR:
        for toplevel in self.patterns:
            if toplevel.type == var:
                return toplevel
        else:
            raise KeyError(var)


@dataclasses.dataclass(frozen=True, order=True)
class Parser(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Parser := $'\\n'.<BranchGR in branches> $'\\n' $'\\n' <RV> $' ' <Variable as start>
    """
    branches: list[BranchGR]
    start: Variable
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.branches:
            for i, e in enumerate(self.branches):
                if i:
                    yield '\n'
                yield str(e)
        yield '\n'
        yield '\n'
        yield '>'
        yield ' '
        yield str(self.start)
    
    def has(self, var: Variable) -> bool:
        for toplevel in self.branches:
            if toplevel.type == var:
                return True
        else:
            return False
    
    def get(self, var: Variable) -> BranchGR:
        for toplevel in self.branches:
            if toplevel.type == var:
                return toplevel
        else:
            raise KeyError(var)
    
    def get_classes(self) -> typing.Dict[Variable, BranchGR]:
        return {toplevel.type: toplevel for toplevel in self.branches if not isinstance(toplevel, Alias)}
    
    def get_types(self, __type: Variable) -> list[Variable]:
        if not self.has(__type):
            return [__type]
        toplevel = self.get(__type)
        if isinstance(toplevel, Group):
            return [type2 for type1 in toplevel.types for type2 in self.get_types(type1)]
        elif isinstance(toplevel, Branch):
            return [__type]
        elif isinstance(toplevel, Alias):
            raise TypeError('There should not remain any Alias when Parser.get_types is called.')
        else:
            raise NotImplementedError
    
    def get_recursion(self, __type: Variable) -> typing.Dict[Variable, bool]:
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
    
    def is_element_of(self, group_type: Variable, element_type: str) -> bool:
        return element_type in map(str, self.get_types(group_type))
    
    def remove_canonicals(self) -> Parser:
        branches = []
        for branch in self.branches:
            try:
                branches.append(branch.remove_canonicals())
            except ValueError:
                continue
        return dataclasses.replace(self, branches=branches)
    
    def simplify_repeats(self) -> Parser:
        branches = [branch.simplify_repeats() for branch in self.branches]
        return dataclasses.replace(self, branches=branches)
    
    @property
    def explicit_uses(self) -> typing.Iterator[Variable]:
        for branch in self.branches:
            yield from branch.explicit_uses


@dataclasses.dataclass(frozen=True, order=True)
class Reader(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Reader := <Lexer as lexer> $'\\n' $'\\n' <Parser as parser>
    """
    lexer: Lexer
    parser: Parser
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.lexer)
        yield '\n'
        yield '\n'
        yield str(self.parser)
    
    def has(self, var: Variable) -> bool:
        if self.parser.has(var):
            return True
        elif self.lexer.has(var):
            return True
        else:
            return False
    
    def get(self, var: Variable) -> TopLevel:
        if self.parser.has(var):
            return self.parser.get(var)
        elif self.lexer.has(var):
            return self.lexer.get(var)
        else:
            raise KeyError(var)
    
    @functools.cached_property
    def simplify_literals(self) -> Reader:
        literals: typing.Dict[Variable, Literal] = {}
        branches = [branch.simplify_literals(literals) for branch in self.parser.branches]
        parser = dataclasses.replace(self.parser, branches=branches)
        new_patterns = [literal.as_pattern(name) for name, literal in literals.items()]
        patterns = new_patterns + self.lexer.patterns
        lexer = dataclasses.replace(self.lexer, patterns=patterns)
        return dataclasses.replace(self, lexer=lexer, parser=parser)
    
    @functools.cached_property
    def simplify_aliases(self) -> Reader:
        branches = [branch.simplify_aliases(self) for branch in self.parser.branches if not isinstance(branch, Alias)]
        parser = dataclasses.replace(self.parser, branches=branches)
        return dataclasses.replace(self, parser=parser)
    
    def simplify(self, **config) -> Reader:
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
    
    @functools.cached_property
    def remove_canonicals(self):
        parser = self.parser.remove_canonicals()
        return dataclasses.replace(self, parser=parser)
    
    @functools.cached_property
    def simplify_repeats(self):
        parser = self.parser.simplify_repeats()
        return dataclasses.replace(self, parser=parser)
    
    def get_uses(self) -> typing.Set[Variable]:
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
                continue
            for used_type in toplevel.explicit_uses:
                if used_type not in done:
                    todo.append(used_type)
        return done
    
    @property
    def def_count(self) -> typing.DefaultDict[str, int]:
        result: typing.DefaultDict[str, int] = collections.defaultdict(int)
        for pattern in self.lexer.patterns:
            result[str(pattern.type)] += 1
        for toplevel in self.parser.branches:
            result[str(toplevel.type)] += 1
        return result
    
    @property
    def use_count(self) -> typing.DefaultDict[str, int]:
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


@dataclasses.dataclass(frozen=True, order=True)
class String(All):
    """
        This class has been generated automatically from the bnf rule :
        regex   String '\\"(?:\\"|[^\\"])*?(?<!\\\\\\\\)\\"|\\'(?:\\'|[^\\'])*?(?<!\\\\\\\\)\\''
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @property
    def value(self) -> str:
        return eval(self.content)
    
    def to_str(self) -> str:
        if isinstance(self, String):
            return eval(self.content)
        return ''
    
    @property
    def is_keyword_expr(self) -> bool:
        return all(map(string.ascii_letters.__contains__, self.value))
    
    @property
    def is_symbols_expr(self) -> bool:
        return all(map(SYMBOL_NAMES.__contains__, self.value))


@dataclasses.dataclass(frozen=True, order=True)
class TopLevel(All, abc.ABC):
    """
        >>> BranchGR  # abstract
        >>> PatternGR  # abstract
    """
    type: Variable
    
    @abc.abstractmethod
    def simplify_aliases(self, reader: Reader):
        """Return a simplified version of `self` without `Alias` objects."""
    
    @property
    @abc.abstractmethod
    def explicit_uses(self) -> typing.Iterator[Variable]:
        """Yields the types used explicitly in `self`. (Assumes that the `reader` has no `Alias` in it)"""
    
    @property
    @abc.abstractmethod
    def is_casted_pattern(self) -> bool:
        """Return True when the node refer to a casted `PatternGR` object."""
    
    @property
    @abc.abstractmethod
    def casted_type(self) -> str:
        """Return the correct casted type corresponding to `self`."""
    
    @property
    @abc.abstractmethod
    def descriptor(self) -> Descriptor:
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Variable(All):
    """
        This class has been generated automatically from the bnf rule :
        regex   Variable '[a-zA-Z_]\\w*'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    def to_str(self) -> str:
        if isinstance(self, Variable):
            return self.content
        return ''
    
    @property
    def as_cast(self) -> str:
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
            raise ValueError('Unable to convert ' + repr(self) + 'to a cast type.')


@dataclasses.dataclass(frozen=True, order=True)
class BranchGR(Buildable, TopLevel, abc.ABC):
    """
        >>> Branch  # concrete
        >>> Alias  # concrete
        >>> Group  # concrete
    """
    
    @abc.abstractmethod
    def remove_canonicals(self) -> BranchGR:
        """Remove `Canonical` objects from `self`."""
    
    @abc.abstractmethod
    def simplify_repeats(self) -> BranchGR:
        """Remove `Repeat` & `RepeatPlus` & `Enum0` & `Enum1` occurrences in `self`."""


@dataclasses.dataclass(frozen=True, order=True)
class ParallelGR(Buildable, abc.ABC):
    """
        >>> Parallel  # concrete
        >>> SequenceGR  # abstract
    """
    
    @property
    @abc.abstractmethod
    def as_grouping(self) -> GroupingGR:
        """Transform `self` such as it becomes a `GroupingGR` object."""
    
    @property
    @abc.abstractmethod
    def as_sequence_rules(self) -> list[RepeatGR]:
        """Consider `self` as a `Sequence` and return its child rules."""
    
    @property
    @abc.abstractmethod
    def as_parallel_rules(self) -> list[SequenceGR]:
        """Consider `self` as a `Parallel` and return its child rules."""
    
    def __and__(self, other: ParallelGR) -> SequenceGR:
        rules = []
        rules.extend(self.as_sequence_rules)
        rules.extend(other.as_sequence_rules)
        if len(rules) == 1:
            return rules[0]
        return Sequence(rules=rules)
    
    def __or__(self, other: ParallelGR) -> ParallelGR:
        rules = []
        rules.extend(self.as_parallel_rules)
        rules.extend(other.as_parallel_rules)
        if len(rules) == 1:
            return rules[0]
        return Parallel(rules=rules)
    
    @abc.abstractmethod
    def simplify_aliases(self, reader: Reader):
        """Return a simplified version of `self` without `Alias` objects."""
    
    @abc.abstractmethod
    def remove_canonicals(self):
        """Remove `Canonical` objects from `self`."""
    
    @abc.abstractmethod
    def simplify_repeats(self):
        """Remove `Repeat` & `RepeatPlus` & `Enum0` & `Enum1` occurrences in `self`."""
    
    @property
    @abc.abstractmethod
    def descriptor(self) -> Descriptor:
        """Return the descriptor associated with `self` (assumes that no match refers to `Alias` objects)."""


@dataclasses.dataclass(frozen=True, order=True)
class PatternGR(TopLevel, abc.ABC):
    """
        >>> StringPattern  # concrete
        >>> RegexPattern  # concrete
        >>> KeywordPattern  # concrete
    """
    expr: String
    priority: Integer | None = None
    cast: Variable | None = None
    ignore_: Ignore | None = None
    
    @property
    @abc.abstractmethod
    def canonical(self) -> String:
        pass
    
    def simplify_aliases(self, reader: Reader):
        return self
    
    @property
    def explicit_uses(self) -> typing.Iterator[Variable]:
        yield from []
    
    @property
    def is_casted_pattern(self) -> bool:
        return bool(self.cast)
    
    @property
    def casted_type(self) -> str:
        if isinstance(self.cast, Variable):
            return self.cast.as_cast
        else:
            return str(self.type)
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor({'content': Attribute(name='content', types={'str'}, required=True, multiple=False)})


@dataclasses.dataclass(frozen=True, order=True)
class Alias(BranchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Alias := <KW_ALIAS> $' ' $' ' <Variable as type> ?[$' ' <String as line_prefix>] $' ' <COLON_EQ> $' ' <P…
    """
    rule: ParallelGR
    line_prefix: String | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'alias'
        yield ' '
        yield ' '
        yield str(self.type)
        if self.line_prefix:
            yield ' '
            yield str(self.line_prefix)
        yield ' '
        yield ':='
        yield ' '
        yield str(self.rule)
    
    @property
    def is_optional(self) -> bool:
        return self.rule.is_optional
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return NotImplemented
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        raise NotImplementedError('Alias.simplify_aliases() should never be called !')
    
    def remove_canonicals(self) -> BranchGR:
        return self
    
    def simplify_repeats(self) -> BranchGR:
        return self
    
    @property
    def explicit_uses(self) -> typing.Iterator[Variable]:
        raise NotImplementedError('Alias.explicit_uses should never be called !')
    
    @property
    def is_casted_pattern(self) -> bool:
        return False
    
    @property
    def casted_type(self) -> str:
        raise NotImplementedError('Alias objects does not have casted type.')
    
    @property
    def descriptor(self) -> Descriptor:
        return self.rule.descriptor


@dataclasses.dataclass(frozen=True, order=True)
class Branch(BranchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Branch := <KW_BRANCH> ?[<LB> <Integer as priority> <RB>] $' ' <Variable as type> ?[$' ' <String as line_…
    """
    rule: ParallelGR
    priority: Integer | None = None
    line_prefix: String | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'branch'
        if self.priority:
            yield '['
            yield str(self.priority)
            yield ']'
        yield ' '
        yield str(self.type)
        if self.line_prefix:
            yield ' '
            yield str(self.line_prefix)
        yield ' '
        yield ':='
        yield ' '
        yield str(self.rule)
    
    @property
    def is_optional(self) -> bool:
        return self.rule.is_optional
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self) -> BranchGR:
        try:
            rule = self.rule.remove_canonicals()
        except ValueError:
            raise ValueError('Cannot build (empty branch) : ' + repr(self))
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self) -> BranchGR:
        rule = self.rule.simplify_repeats()
        return dataclasses.replace(self, rule=rule)
    
    @property
    def explicit_uses(self) -> typing.Iterator[Variable]:
        for attribute in self.descriptor.attributes.values():
            for sub_type in attribute.types:
                yield Variable(sub_type)
    
    @property
    def is_casted_pattern(self) -> bool:
        return False
    
    @property
    def casted_type(self) -> str:
        return str(self.type)
    
    @property
    def descriptor(self) -> Descriptor:
        return self.rule.descriptor


@dataclasses.dataclass(frozen=True, order=True)
class Group(BranchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Group := <KW_GROUP> $' ' $' ' <Variable as type> $' ' <COLON_EQ> $' ' [$' ' <VBAR> $' '].<Variable in ty…
    """
    types: list[Variable]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'group'
        yield ' '
        yield ' '
        yield str(self.type)
        yield ' '
        yield ':='
        yield ' '
        if self.types:
            for i, e in enumerate(self.types):
                if i:
                    yield ' '
                    yield '|'
                    yield ' '
                yield str(e)
    
    @property
    def is_optional(self) -> bool:
        return False
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return set()
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        return self
    
    def simplify_aliases(self, reader: Reader):
        return self
    
    def remove_canonicals(self) -> BranchGR:
        return self
    
    def simplify_repeats(self) -> BranchGR:
        return self
    
    @property
    def explicit_uses(self) -> typing.Iterator[Variable]:
        for sub_type in self.types:
            yield sub_type
    
    @property
    def is_casted_pattern(self) -> bool:
        return False
    
    @property
    def casted_type(self) -> str:
        return str(self.type)
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor()


@dataclasses.dataclass(frozen=True, order=True)
class KeywordPattern(PatternGR):
    """
        This class has been generated automatically from the bnf rule :
        branch KeywordPattern := <KW_KEYWORD> ?[<LB> <Integer as priority> <RB>] $' ' <Variable as type> ?[<LEFT_PARENT…
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'keyword'
        if self.priority:
            yield '['
            yield str(self.priority)
            yield ']'
        yield ' '
        yield str(self.type)
        if self.cast:
            yield '('
            yield str(self.cast)
            yield ')'
        yield ' '
        yield str(self.expr)
        if self.ignore_:
            yield ' '
            yield str(self.ignore_)
    
    @property
    def canonical(self) -> String:
        return self.expr


@dataclasses.dataclass(frozen=True, order=True)
class Parallel(ParallelGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Parallel := [$' ' <VBAR> $' ']..<SequenceGR in rules>
    """
    rules: list[SequenceGR]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
                yield '|'
                yield ' '
            yield str(e)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [Grouping(rule=self)]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return self.rules
    
    @classmethod
    def from_rules(cls, rules: list[ParallelGR]) -> ParallelGR:
        final = []
        for rule in rules:
            final.extend(rule.as_parallel_rules)
        if len(final) == 1:
            return final[0]
        return cls(rules=final)
    
    @property
    def is_optional(self) -> bool:
        return any((rule.is_optional for rule in self.rules))
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        result = set()
        for rule in self.rules:
            result = result.union(rule.first_matches)
        return result
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rules = [rule.simplify_literals(literals) for rule in self.rules]
        return dataclasses.replace(self, rules=rules)
    
    def simplify_aliases(self, reader: Reader):
        rules = [rule.simplify_aliases(reader) for rule in self.rules]
        return dataclasses.replace(self, rules=rules)
    
    def remove_canonicals(self):
        rules = []
        for rule in self.rules:
            try:
                rules.append(rule.remove_canonicals())
            except ValueError:
                continue
        if not rules:
            raise ValueError('`Parallel` objects with only `Canonical` parts must be removed.')
        return dataclasses.replace(self, rules=rules)
    
    def simplify_repeats(self):
        rules = [rule.simplify_repeats() for rule in self.rules]
        return Parallel.from_rules(rules)
    
    @property
    def descriptor(self) -> Descriptor:
        return functools.reduce(operator.or_, [rule.descriptor for rule in self.rules], Descriptor())


@dataclasses.dataclass(frozen=True, order=True)
class RegexPattern(PatternGR):
    """
        This class has been generated automatically from the bnf rule :
        branch RegexPattern := <KW_REGEX> $' ' $' ' ?[<LB> <Integer as priority> <RB>] $' ' <Variable as type> ?[<LEFT_…
    """
    flags: Integer | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'regex'
        yield ' '
        yield ' '
        if self.priority:
            yield '['
            yield str(self.priority)
            yield ']'
        yield ' '
        yield str(self.type)
        if self.cast:
            yield '('
            yield str(self.cast)
            yield ')'
        yield ' '
        yield str(self.expr)
        if self.flags:
            yield ' '
            yield str(self.flags)
        if self.ignore_:
            yield ' '
            yield str(self.ignore_)
    
    @property
    def canonical(self) -> String:
        raise Exception('No canonical form defined for RegexPattern.')


@dataclasses.dataclass(frozen=True, order=True)
class SequenceGR(ParallelGR, abc.ABC):
    """
        >>> Sequence  # concrete
        >>> RepeatGR  # abstract
    """


@dataclasses.dataclass(frozen=True, order=True)
class StringPattern(PatternGR):
    """
        This class has been generated automatically from the bnf rule :
        branch StringPattern := <KW_STRING> $' ' ?[<LB> <Integer as priority> <RB>] $' ' <Variable as type> ?[<LEFT_PAR…
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'string'
        yield ' '
        if self.priority:
            yield '['
            yield str(self.priority)
            yield ']'
        yield ' '
        yield str(self.type)
        if self.cast:
            yield '('
            yield str(self.cast)
            yield ')'
        yield ' '
        yield str(self.expr)
        if self.ignore_:
            yield ' '
            yield str(self.ignore_)
    
    @property
    def canonical(self) -> String:
        return self.expr


@dataclasses.dataclass(frozen=True, order=True)
class RepeatGR(SequenceGR, abc.ABC):
    """
        >>> Repeat  # concrete
        >>> RepeatStar  # concrete
        >>> RepeatPlus  # concrete
        >>> Optional  # concrete
        >>> Enum0  # concrete
        >>> Enum1  # concrete
        >>> NegativeGR  # abstract
    """


@dataclasses.dataclass(frozen=True, order=True)
class Sequence(SequenceGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Sequence := $' '..<RepeatGR in rules>
    """
    rules: list[RepeatGR]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.rules):
            if i:
                yield ' '
            yield str(e)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return self.rules
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @classmethod
    def from_rules(cls, rules: list[ParallelGR]) -> SequenceGR:
        final = []
        for rule in rules:
            final.extend(rule.as_sequence_rules)
        if len(final) == 1:
            return final[0]
        return cls(rules=final)
    
    @property
    def is_optional(self) -> bool:
        return all((rule.is_optional for rule in self.rules))
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        result = set()
        for rule in self.rules:
            result = result.union(rule.first_matches)
            if not rule.is_optional:
                break
        return result
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rules = [rule.simplify_literals(literals) for rule in self.rules]
        return dataclasses.replace(self, rules=rules)
    
    def simplify_aliases(self, reader: Reader):
        rules = [rule.simplify_aliases(reader) for rule in self.rules]
        return dataclasses.replace(self, rules=rules)
    
    def remove_canonicals(self):
        rules = []
        for rule in self.rules:
            try:
                rules.append(rule.remove_canonicals())
            except ValueError:
                continue
        if not rules:
            raise ValueError('`Sequence` objects with only `Canonical` parts must be removed.')
        return dataclasses.replace(self, rules=rules)
    
    def simplify_repeats(self):
        rules = [rule.simplify_repeats() for rule in self.rules]
        return Sequence.from_rules(rules)
    
    @property
    def descriptor(self) -> Descriptor:
        return functools.reduce(operator.and_, [rule.descriptor for rule in self.rules], Descriptor())


@dataclasses.dataclass(frozen=True, order=True)
class Enum0(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Enum0 := <NegativeGR as separator> <DOT> <NegativeGR as element>
    """
    separator: NegativeGR
    element: NegativeGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.separator)
        yield '.'
        yield str(self.element)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @property
    def is_optional(self) -> bool:
        return self.element.is_optional and self.separator.is_optional
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        result = set()
        result = result.union(self.element.first_matches)
        if self.element.is_optional:
            result = result.union(self.separator.first_matches)
        return result
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        separator = self.separator.simplify_literals(literals)
        element = self.element.simplify_literals(literals)
        return dataclasses.replace(self, separator=separator, element=element)
    
    def simplify_aliases(self, reader: Reader):
        separator = self.separator.simplify_aliases(reader)
        element = self.element.simplify_aliases(reader)
        return dataclasses.replace(self, separator=separator, element=element)
    
    def remove_canonicals(self):
        try:
            element = self.element.remove_canonicals()
        except ValueError:
            element = None
        try:
            separator = self.separator.remove_canonicals()
        except ValueError:
            separator = None
        if element is None and separator is None:
            raise ValueError('`Enum` objects with only `Canonical` parts must be removed.')
        elif element is None:
            return RepeatStar(rule=separator)
        elif separator is None:
            return RepeatPlus(rule=element)
        else:
            return dataclasses.replace(self, element=element, separator=separator)
    
    def simplify_repeats(self):
        element = self.element.simplify_repeats()
        separator = self.separator.simplify_repeats()
        return element & RepeatStar.from_rule(separator & element)
    
    @property
    def descriptor(self) -> Descriptor:
        model = self.separator.descriptor.optional() & self.element.descriptor
        assert model.only_multiple_attributes(), 'Enum only allow attributes with `multiple`'
        return model


@dataclasses.dataclass(frozen=True, order=True)
class Enum1(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Enum1 := <NegativeGR as separator> <DOT> <DOT> <NegativeGR as element>
    """
    separator: NegativeGR
    element: NegativeGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.separator)
        yield '.'
        yield '.'
        yield str(self.element)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @property
    def is_optional(self) -> bool:
        return self.element.is_optional and self.separator.is_optional
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        result = set()
        result = result.union(self.element.first_matches)
        if self.element.is_optional:
            result = result.union(self.separator.first_matches)
        return result
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        separator = self.separator.simplify_literals(literals)
        element = self.element.simplify_literals(literals)
        return dataclasses.replace(self, separator=separator, element=element)
    
    def simplify_aliases(self, reader: Reader):
        separator = self.separator.simplify_aliases(reader)
        element = self.element.simplify_aliases(reader)
        return dataclasses.replace(self, separator=separator, element=element)
    
    def remove_canonicals(self):
        try:
            element = self.element.remove_canonicals()
        except ValueError:
            element = None
        try:
            separator = self.separator.remove_canonicals()
        except ValueError:
            separator = None
        if element is None and separator is None:
            raise ValueError('`Enum` objects with only `Canonical` parts must be removed.')
        elif element is None:
            return RepeatStar(rule=separator)
        elif separator is None:
            return Repeat(rule=element, mn=Integer('2'), mx=None)
        else:
            return dataclasses.replace(self, element=element, separator=separator)
    
    def simplify_repeats(self):
        element = self.element.simplify_repeats()
        separator = self.separator.simplify_repeats()
        return element & separator & element & RepeatStar.from_rule(separator & element)
    
    @property
    def descriptor(self) -> Descriptor:
        model = self.separator.descriptor & self.element.descriptor
        assert model.only_multiple_attributes(), 'EnumPlus only allow attributes with `multiple`'
        return model


@dataclasses.dataclass(frozen=True, order=True)
class NegativeGR(RepeatGR, abc.ABC):
    """
        >>> Negative  # concrete
        >>> GroupingGR  # abstract
    """


@dataclasses.dataclass(frozen=True, order=True)
class Optional(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Optional := <INT> <NegativeGR as rule>
    """
    rule: NegativeGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '?'
        yield str(self.rule)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @classmethod
    def from_rule(cls, rule: ParallelGR) -> Optional:
        return cls(rule=rule.as_grouping)
    
    @property
    def is_optional(self) -> bool:
        return True
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self):
        rule = self.rule.simplify_repeats()
        return Optional.from_rule(rule)
    
    @property
    def descriptor(self) -> Descriptor:
        return self.rule.descriptor.optional()


@dataclasses.dataclass(frozen=True, order=True)
class Repeat(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Repeat := <LS> ?<Integer as mn> <COMMA> ?<Integer as mx> <RS> <NegativeGR as rule>
    """
    rule: NegativeGR
    mn: Integer | None = None
    mx: Integer | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '{'
        if self.mn:
            yield str(self.mn)
        yield ','
        if self.mx:
            yield str(self.mx)
        yield '}'
        yield str(self.rule)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @property
    def is_optional(self) -> bool:
        return Integer.to_int(self.mn) > 0
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self):
        rule = self.rule.simplify_repeats()
        mn = Integer.to_int(self.mn)
        if mn == 0:
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
            optional_part = Optional.from_rule(rule)
            for _ in range(mx - 1):
                optional_part = Optional.from_rule(rule & optional_part)
        if required_part is None:
            return optional_part
        else:
            return required_part & optional_part
    
    @property
    def descriptor(self) -> Descriptor:
        model = self.rule.descriptor
        assert model.only_multiple_attributes(), 'Repeat only allow attributes with `multiple`'
        if Integer.to_int(self.mn) > 0:
            return model.optional()
        else:
            return model


@dataclasses.dataclass(frozen=True, order=True)
class RepeatPlus(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch RepeatPlus := <PLUS> <NegativeGR as rule>
    """
    rule: NegativeGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '+'
        yield str(self.rule)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @classmethod
    def from_rule(cls, rule: ParallelGR) -> RepeatPlus:
        return cls(rule=rule.as_grouping)
    
    @property
    def is_optional(self) -> bool:
        return self.rule.is_optional
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self):
        rule = self.rule.simplify_repeats()
        return rule & RepeatStar.from_rule(rule)
    
    @property
    def descriptor(self) -> Descriptor:
        model = self.rule.descriptor
        assert model.only_multiple_attributes(), 'RepeatPlus only allow attributes with `multiple`'
        return model


@dataclasses.dataclass(frozen=True, order=True)
class RepeatStar(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch RepeatStar := <ASTERISK> <NegativeGR as rule>
    """
    rule: NegativeGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '*'
        yield str(self.rule)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @classmethod
    def from_rule(cls, rule: ParallelGR) -> RepeatStar:
        return cls(rule=rule.as_grouping)
    
    @property
    def is_optional(self) -> bool:
        return True
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self):
        rule = self.rule.simplify_repeats()
        return RepeatStar.from_rule(rule)
    
    @property
    def descriptor(self) -> Descriptor:
        model = self.rule.descriptor
        assert model.only_multiple_attributes(), 'RepeatStar only allow attributes with `multiple`'
        return model.optional()


@dataclasses.dataclass(frozen=True, order=True)
class GroupingGR(NegativeGR, abc.ABC):
    """
        >>> Grouping  # concrete
        >>> AtomGR  # abstract
    """
    
    @property
    def as_grouping(self) -> GroupingGR:
        return self


@dataclasses.dataclass(frozen=True, order=True)
class Negative(NegativeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Negative := <EXC> <GroupingGR as rule>
    """
    rule: GroupingGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '!'
        yield str(self.rule)
    
    @property
    def as_grouping(self) -> GroupingGR:
        return Grouping(rule=self)
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    @classmethod
    def from_rule(cls, rule: ParallelGR) -> Negative:
        return cls(rule=rule.as_grouping)
    
    @property
    def is_optional(self) -> bool:
        return True
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self):
        rule = self.rule.simplify_repeats()
        return Negative.from_rule(rule)
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor()


@dataclasses.dataclass(frozen=True, order=True)
class AtomGR(GroupingGR, abc.ABC):
    """
        >>> Canonical  # concrete
        >>> Literal  # concrete
        >>> MatchGR  # abstract
    """
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return [self]
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return [self]
    
    def simplify_repeats(self):
        return self


@dataclasses.dataclass(frozen=True, order=True)
class Grouping(GroupingGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Grouping := <LB> <ParallelGR as rule> <RB>
    """
    rule: ParallelGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '['
        yield str(self.rule)
        yield ']'
    
    @property
    def as_sequence_rules(self) -> list[RepeatGR]:
        return self.rule.as_sequence_rule
    
    @property
    def as_parallel_rules(self) -> list[SequenceGR]:
        return self.rule.as_parallel_rules
    
    @property
    def is_optional(self) -> bool:
        return self.rule.is_optional
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return self.rule.first_matches
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        rule = self.rule.simplify_literals(literals)
        return dataclasses.replace(self, rule=rule)
    
    def simplify_aliases(self, reader: Reader):
        rule = self.rule.simplify_aliases(reader)
        return dataclasses.replace(self, rule=rule)
    
    def remove_canonicals(self):
        rule = self.rule.remove_canonicals()
        return dataclasses.replace(self, rule=rule)
    
    def simplify_repeats(self):
        rule = self.rule.simplify_repeats()
        return rule
    
    @property
    def descriptor(self) -> Descriptor:
        return self.rule.descriptor


@dataclasses.dataclass(frozen=True, order=True)
class Canonical(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Canonical := <DOLLAR> <String as expr>
    """
    expr: String
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '$'
        yield str(self.expr)
    
    @property
    def is_optional(self) -> bool:
        return True
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return set()
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        return self
    
    def simplify_aliases(self, reader: Reader):
        return self
    
    def remove_canonicals(self):
        raise ValueError('`Canonical` objects must be removed.')
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor()


@dataclasses.dataclass(frozen=True, order=True)
class Literal(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Literal := <String as expr>
    """
    expr: String
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.expr)
    
    @property
    def is_optional(self) -> bool:
        return False
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return NotImplemented
    
    def as_pattern(self, __type: Variable) -> PatternGR:
        if self.expr.is_keyword_expr:
            return KeywordPattern(type=__type, expr=self.expr, priority=Integer('200'))
        elif self.expr.is_symbols_expr:
            return StringPattern(type=__type, expr=self.expr, priority=Integer('100'))
        else:
            raise NotImplementedError('Mixin patterns are not handled yet.')
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        if self.expr.is_keyword_expr:
            pattern_type = Variable('KW_' + String.to_str(self.expr).upper())
        elif self.expr.is_symbols_expr:
            pattern_type = Variable('_'.join(map(SYMBOL_NAMES.__getitem__, String.to_str(self.expr))))
        else:
            raise NotImplementedError('cannot extrapolate name for expression : ' + self.expr.content)
        if pattern_type in literals:
            assert literals[pattern_type] == self
        else:
            literals[pattern_type] = self
        return Match(type=pattern_type)
    
    def simplify_aliases(self, reader: Reader):
        return self
    
    def remove_canonicals(self):
        return self
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor()


@dataclasses.dataclass(frozen=True, order=True)
class MatchGR(AtomGR, abc.ABC):
    """
        >>> MatchKeyGR  # abstract
        >>> Match  # concrete
    """
    type: Variable


@dataclasses.dataclass(frozen=True, order=True)
class Match(MatchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Match := <LV> <Variable as type> <RV>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '<'
        yield str(self.type)
        yield '>'
    
    @property
    def is_optional(self) -> bool:
        return False
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return {self.type}
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        return self
    
    def simplify_aliases(self, reader: Reader):
        if reader.has(self.type):
            toplevel = reader.get(self.type)
            if isinstance(toplevel, Alias):
                return toplevel.rule.simplify_aliases(reader)
        return self
    
    def remove_canonicals(self):
        return self
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor()


@dataclasses.dataclass(frozen=True, order=True)
class MatchKeyGR(MatchGR, abc.ABC):
    """
        >>> MatchAs  # concrete
        >>> MatchIn  # concrete
    """
    key: Variable


@dataclasses.dataclass(frozen=True, order=True)
class MatchAs(MatchKeyGR):
    """
        This class has been generated automatically from the bnf rule :
        branch MatchAs := <LV> <Variable as type> $' ' <KW_AS> $' ' <Variable as key> <RV>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '<'
        yield str(self.type)
        yield ' '
        yield 'as'
        yield ' '
        yield str(self.key)
        yield '>'
    
    @property
    def is_optional(self) -> bool:
        return False
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return {self.type}
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        return self
    
    def simplify_aliases(self, reader: Reader):
        return self
    
    def remove_canonicals(self):
        return self
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor({str(self.key): Attribute(name=str(self.key), types={str(self.type)}, multiple=False, required=True)})


@dataclasses.dataclass(frozen=True, order=True)
class MatchIn(MatchKeyGR):
    """
        This class has been generated automatically from the bnf rule :
        branch MatchIn := <LV> <Variable as type> $' ' <KW_IN> $' ' <Variable as key> <RV>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '<'
        yield str(self.type)
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.key)
        yield '>'
    
    @property
    def is_optional(self) -> bool:
        return False
    
    @property
    def first_matches(self) -> typing.Set[Variable]:
        return {self.type}
    
    def simplify_literals(self, literals: typing.Dict[Variable, Literal]):
        return self
    
    def simplify_aliases(self, reader: Reader):
        return self
    
    def remove_canonicals(self):
        return self
    
    @property
    def descriptor(self) -> Descriptor:
        return Descriptor({str(self.key): Attribute(name=str(self.key), types={str(self.type)}, multiple=True, required=True)})
