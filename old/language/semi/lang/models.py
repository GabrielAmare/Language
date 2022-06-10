"""
    This module has been auto-generated. Do not change manually.
    WARNING : Manual changes to this file are likely to be overwritten.
"""
from __future__ import annotations

import abc
import collections
import dataclasses
import operator
import typing

from website.language import bnf, optilex as ol, regex
from website.language.semi.processing import make_origin_select

__all__ = [
    'ALWAYS',
    'AllGR',
    'Branch',
    'BranchGR',
    'BranchSet',
    'Buildable',
    'ERROR',
    'EXCLUDED',
    'EmptyGR',
    'Error',
    'Excluded',
    'Group',
    'Grouping',
    'GroupingGR',
    'Ignore',
    'Include',
    'Integer',
    'Inverted',
    'Match',
    'MatchGR',
    'NEVER',
    'Parallel',
    'ParallelGR',
    'Repeat',
    'RepeatGR',
    'Sequence',
    'SequenceGR',
    'String',
    'VALID',
    'Valid',
    'Variable'
]


def _flat_str(method):
    def wrapped(self) -> str:
        return ''.join(method(self))
    return wrapped


@dataclasses.dataclass(frozen=True, order=True)
class AllGR(abc.ABC):
    """
        >>> Buildable  # abstract
        >>> Group  # concrete
        >>> Ignore  # concrete
        >>> Include  # concrete
        >>> Inverted  # concrete
        >>> Integer  # atomic
        >>> String  # atomic
        >>> Variable  # atomic
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Buildable(AllGR, abc.ABC):
    """
        >>> BranchGR  # abstract
        >>> ParallelGR  # abstract
    """
    
    @property
    @abc.abstractmethod
    def is_optional(self) -> bool:
        """This means the Buildable can be constructed directly without more elements."""
    
    @property
    @abc.abstractmethod
    def alphabet(self) -> typing.FrozenSet[str]:
        """Return the set of elements that can interact with the rule."""


@dataclasses.dataclass(frozen=True, order=True)
class Group(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Group := ?<Inverted as inverted> <String as items>
    """
    items: String
    inverted: Inverted | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.inverted:
            yield str(self.inverted)
        yield str(self.items)
    
    def union(self, *others: Group) -> Group:
        l_items: frozenset[str] = self.to_frozenset()
        l_inv: bool = Inverted.to_bool(self.inverted)
        for other in others:
            r_items: frozenset[str] = other.to_frozenset()
            r_inv: bool = Inverted.to_bool(other.inverted)
            if r_inv:
                if l_inv:
                    l_items = r_items.difference(l_items)
                else:
                    l_items = r_items.intersection(l_items)
            elif l_inv:
                l_items = l_items.union(r_items)
            else:
                l_items = l_items.difference(r_items)
            l_inv = l_inv or r_inv
        items: String = String.from_str(''.join(l_items))
        inv: typing.Optional[Inverted] = Inverted.from_bool(l_inv)
        return Group(items=items, inverted=inv)
    
    def intersection(self, *others: Group) -> Group:
        l_items: frozenset[str] = self.to_frozenset()
        l_inv: bool = Inverted.to_bool(self.inverted)
        for other in others:
            r_items: frozenset[str] = other.to_frozenset()
            r_inv: bool = Inverted.to_bool(other.inverted)
            if r_inv:
                if l_inv:
                    l_items = r_items.difference(l_items)
                else:
                    l_items = r_items.union(l_items)
            elif l_inv:
                l_items = l_items.intersection(r_items)
            else:
                l_items = l_items.difference(r_items)
            l_inv = l_inv and r_inv
        items: String = String.from_str(''.join(l_items))
        inv: typing.Optional[Inverted] = Inverted.from_bool(l_inv)
        return Group(items=items, inverted=inv)
    
    @property
    def complement(self) -> Group:
        inverted = Inverted.from_bool(not Inverted.to_bool(self.inverted))
        return Group(items=self.items, inverted=inverted)
    
    def __contains__(self, item: str) -> bool:
        return operator.xor(item in self.to_frozenset(), Inverted.to_bool(self.inverted))
    
    @property
    def is_inverted(self) -> bool:
        return Inverted.to_bool(self.inverted)
    
    @classmethod
    def from_frozenset(cls, items: typing.FrozenSet[str], inverted: bool = False) -> Group:
        return cls(items=String.from_str(''.join(sorted(items))), inverted=Inverted.from_bool(inverted))
    
    def to_frozenset(self) -> typing.FrozenSet[str]:
        return frozenset(self.items.to_str())
    
    @classmethod
    def from_regex(cls, obj: regex.GroupInnerGR) -> Group:
        charset = obj.as_outer_charset
        items = String(content=repr(''.join(sorted(charset.items))))
        inverted = Inverted() if charset.inverted else None
        return cls(items=items, inverted=inverted)
    
    def to_optilex(self) -> ol.Charset:
        items = ol.String(content=repr(''.join(sorted(self.items.to_str()))))
        if isinstance(self.inverted, Inverted):
            inverted = ol.Inverted()
        else:
            inverted = None
        return ol.Charset(items=items, inverted=inverted)


@dataclasses.dataclass(frozen=True, order=True)
class Ignore(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Ignore := <KW_IGNORE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'ignore'


@dataclasses.dataclass(frozen=True, order=True)
class Include(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Include := <PLUS>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '+'


@dataclasses.dataclass(frozen=True, order=True)
class Integer(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        regex   Integer '\\d+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def from_int(cls, value: int) -> typing.Optional[Integer]:
        if value == 0:
            return None
        return cls(content=repr(value))
    
    def to_int(self) -> int:
        if self is None:
            return 0
        return int(self.content)
    
    @classmethod
    def from_regex(cls, obj: typing.Optional[regex.Integer]) -> typing.Optional[Integer]:
        if isinstance(obj, regex.Integer):
            return cls(content=''.join((digit.content for digit in obj.digits)))
        else:
            return None


@dataclasses.dataclass(frozen=True, order=True)
class Inverted(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Inverted := <WAVE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '~'
    
    @classmethod
    def from_bool(cls, value: bool) -> typing.Optional[Inverted]:
        return cls() if value else None
    
    def to_bool(self) -> bool:
        return isinstance(self, Inverted)


@dataclasses.dataclass(frozen=True, order=True)
class String(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        regex   String '\\".*?\\"'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def from_str(cls, value: str) -> String:
        return cls(content=repr(value))
    
    def to_str(self) -> str:
        return eval(self.content)


@dataclasses.dataclass(frozen=True, order=True)
class Variable(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        regex   Variable '[a-zA-Z_]\\w+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def from_str(cls, value: str) -> Variable:
        return cls(content=value)
    
    def to_str(self) -> str:
        return self.content


@dataclasses.dataclass(frozen=True, order=True)
class BranchGR(Buildable, abc.ABC):
    """
        >>> BranchSet  # concrete
        >>> Branch  # concrete
    """
    
    @abc.abstractmethod
    def split_branch_set(self) -> list[Branch]:
        """Return the list of branches applied in parallel that represent `self`."""
    
    @property
    @abc.abstractmethod
    def is_terminal(self) -> bool:
        """Return True if `self` is terminal."""
    
    @property
    @abc.abstractmethod
    def can_be_processed(self) -> bool:
        """Return True if `self` can be processed."""


@dataclasses.dataclass(frozen=True, order=True)
class ParallelGR(Buildable, abc.ABC):
    """
        >>> Parallel  # concrete
        >>> SequenceGR  # abstract
    """
    
    @abc.abstractmethod
    def as_grouping(self) -> GroupingGR:
        """Transform the given rule to a GroupingGR instance."""
    
    def as_repeat(self, mn: typing.Optional[Integer], mx: typing.Optional[Integer]) -> RepeatGR:
        rule = self.as_grouping()
        v_mn = Integer.to_int(mn)
        v_mx = Integer.to_int(mx)
        if v_mx == 0 or v_mn <= v_mx:
            return Repeat(rule=rule, mn=mn, mx=mx)
        else:
            return Error()
    
    @abc.abstractmethod
    def split_sequence(self) -> list[RepeatGR]:
        """Return the list of rules applied in sequence that represent `self`."""
    
    @abc.abstractmethod
    def split_parallel(self) -> list[SequenceGR]:
        """Return the list of rules applied in parallel that represent `self`."""
    
    def __and__(self, other: ParallelGR) -> SequenceGR:
        return Sequence.from_rules([self, other])
    
    def __or__(self, other: ParallelGR) -> ParallelGR:
        return Parallel.from_rules([self, other])
    
    @property
    @abc.abstractmethod
    def hash_order(self) -> int:
        pass
    
    @property
    @abc.abstractmethod
    def canonical(self) -> ParallelGR:
        """Return the canonical form of a rule."""
    
    @abc.abstractmethod
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        pass
    
    @classmethod
    def from_regex(cls, obj: regex.ParallelGR) -> ParallelGR:
        if isinstance(obj, regex.GroupInnerGR):
            return Match(Group.from_regex(obj))
        elif isinstance(obj, regex.Parallel):
            return Parallel.from_rules(rules=map(cls.from_regex, obj.items))
        elif isinstance(obj, (regex.Sequence, regex.GroupOuter, regex.GroupIgnore)):
            return Sequence.from_rules(rules=map(cls.from_regex, obj.items))
        elif isinstance(obj, regex.Repeat):
            return cls.from_regex(obj.item).as_repeat(mn=Integer.from_regex(obj.mn), mx=Integer.from_regex(obj.mx))
        elif isinstance(obj, regex.Optional):
            return cls.from_regex(obj.item).as_repeat(mn=Integer.from_int(0), mx=Integer.from_int(1))
        elif isinstance(obj, (regex.RepeatStar, regex.LazyRepeatStar)):
            return cls.from_regex(obj.item).as_repeat(mn=Integer.from_int(0), mx=Integer.from_int(0))
        elif isinstance(obj, (regex.RepeatPlus, regex.LazyRepeatPlus)):
            return cls.from_regex(obj.item).as_repeat(mn=Integer.from_int(1), mx=Integer.from_int(0))
        elif isinstance(obj, regex.NegativeLookBehind):
            return cls.from_regex(obj.rule)
        else:
            raise NotImplementedError(type(obj))
    
    @classmethod
    def from_bnf(cls, obj: bnf.PatternGR) -> ParallelGR:
        if isinstance(obj, (bnf.StringPattern, bnf.KeywordPattern)):
            rules = [Match(Group(String(repr(char)))) for char in obj.expr.value]
            return Sequence.from_rules(rules=rules)
        elif isinstance(obj, bnf.RegexPattern):
            regex_pattern = regex.engine(obj.expr.value)
            return cls.from_regex(regex_pattern)
        else:
            raise NotImplementedError(type(obj))
    
    def to_optilex(self) -> typing.Optional[ol.Include]:
        raise TypeError(type(self))


@dataclasses.dataclass(frozen=True, order=True)
class Branch(BranchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Branch := <Variable as type> ?[<LB> <Integer as priority> <RB>] ?[$' ' <Ignore as ignore_>] $' ' <Parall…
    """
    type: Variable
    rule: ParallelGR
    priority: Integer | None = None
    ignore_: Ignore | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.type)
        if self.priority:
            yield '['
            yield str(self.priority)
            yield ']'
        if self.ignore_:
            yield ' '
            yield str(self.ignore_)
        yield ' '
        yield str(self.rule)
    
    def split_branch_set(self) -> list[Branch]:
        return [self]
    
    @property
    def order_key(self) -> tuple[int, str, int]:
        return Integer.to_int(self.priority), Variable.to_str(self.type), self.rule.hash_order
    
    @property
    def is_optional(self) -> bool:
        return self.rule.is_optional
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return self.rule.alphabet
    
    @property
    def is_terminal(self) -> bool:
        return isinstance(self.rule, (Valid, Error, Excluded))
    
    @property
    def can_be_processed(self) -> bool:
        return not isinstance(self.rule, Error)
    
    @classmethod
    def keep_max_priority(cls, branches: list[Branch]) -> list[Branch]:
        max_priority = max((Integer.to_int(branch.priority) for branch in branches))
        return [branch for branch in branches if Integer.to_int(branch.priority) == max_priority]
    
    def process(self) -> typing.Iterator[tuple[Group, Branch]]:
        data = collections.defaultdict(list)
        for group, rule in self.rule.process():
            data[group].append(rule)
        for group, rules in data.items():
            yield group, dataclasses.replace(self, rule=Parallel.from_rules(rules))
        if self.rule.is_optional:
            yield ALWAYS, dataclasses.replace(self, rule=EXCLUDED)
    
    @classmethod
    def from_bnf(cls, obj: bnf.PatternGR) -> Branch:
        type_ = Variable(str(obj.type))
        rule = ParallelGR.from_bnf(obj)
        if obj.priority:
            priority = Integer(obj.priority.content)
        else:
            priority = None
        return cls(type=type_, rule=rule, priority=priority)
    
    def to_optilex(self) -> ol.Action:
        include = self.rule.to_optilex()
        build = ol.Variable(self.type.content)
        goto = ol.Integer.from_int(0)
        if isinstance(self.ignore_, Ignore):
            clear = ol.Clear()
        else:
            clear = None
        return ol.Action(include_=include, build=build, goto=goto, clear=clear)


@dataclasses.dataclass(frozen=True, order=True)
class BranchSet(BranchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch BranchSet := <NEWLINE>.<Branch in branches>
    """
    branches: list[Branch]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.branches:
            for i, e in enumerate(self.branches):
                if i:
                    yield '\n'
                yield str(e)
    
    def split_branch_set(self) -> list[Branch]:
        return self.branches
    
    @classmethod
    def from_branches(cls, branches: typing.Iterator[BranchGR]) -> BranchSet:
        return cls(branches=[inner for outer in branches for inner in outer.split_branch_set()])
    
    @property
    def order_key(self) -> tuple[int, tuple[tuple[int, str, int], ...]]:
        return len(self.branches), tuple(sorted(map(operator.attrgetter('order_key'), self.branches)))
    
    @property
    def is_optional(self) -> bool:
        return all((branch.is_optional for branch in self.branches))
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return frozenset((item for branch in self.branches for item in branch.alphabet))
    
    @property
    def is_terminal(self) -> bool:
        return all((branch.is_terminal for branch in self.branches))
    
    @property
    def can_be_processed(self) -> bool:
        return not self.is_terminal
    
    @property
    def simplified_step_1(self) -> BranchSet:
        data = collections.defaultdict(list)
        for branch in self.branches:
            key = (branch.type, branch.priority)
            data[key].append(branch.rule)
        branches = []
        for key, rules in data.items():
            type_ = key[0]
            priority = key[1]
            rule = Parallel.from_rules(rules)
            branch = Branch(type=type_, rule=rule, priority=priority)
            branches.append(branch)
        return BranchSet(branches=branches)
    
    @property
    def simplified_step_2(self) -> BranchSet:
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
    
    @property
    def simplified(self) -> BranchSet:
        return self.simplified_step_1.simplified_step_2
    
    def split_branches(self) -> tuple[list[Branch], list[Branch], list[Branch], list[Branch]]:
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
    
    def process(self) -> typing.Iterator[tuple[Group, BranchSet]]:
        data = collections.defaultdict(list)
        for i_branch in self.branches:
            for group, o_branch in i_branch.process():
                data[group].append(o_branch)
        for group, branches in data.items():
            yield group, BranchSet.from_branches(branches)
    
    @property
    def pre_processed(self) -> BranchSet:
        return BranchSet.from_branches([branch for branch in self.branches if branch.can_be_processed])
    
    @classmethod
    def from_bnf(cls, obj: bnf.Lexer) -> BranchSet:
        branches = list(map(Branch.from_bnf, obj.patterns))
        return cls(branches=branches)
    
    def to_optilex_index(self, origins: list[BranchSet]) -> int:
        try:
            return origins.index(self.pre_processed)
        except ValueError:
            return -1
    
    def to_optilex_al(self, origins: list[BranchSet], origin: BranchSet) -> ol.ActionList:
        errors, excluded, included, continued = self.split_branches()
        if continued:
            goto = ol.Integer.from_int(self.to_optilex_index(origins))
            action = ol.Action(include_=ol.Include(), build=None, goto=goto, clear=None)
            actions = [action]
        elif included:
            included = Branch.keep_max_priority(included)
            actions = [branch.to_optilex() for branch in included]
        elif excluded:
            excluded = Branch.keep_max_priority(excluded)
            actions = [branch.to_optilex() for branch in excluded]
        else:
            if origin == origins[0]:
                error = None
            else:
                error_types = [branch.type.content for branch in self.branches]
                error_types = set(error_types)
                error_types = sorted(error_types)
                error = ol.Variable.from_str('!' + '|'.join(error_types))
            action = ol.Action(include_=ol.Include(), build=error, goto=ol.Integer.from_int(-1), clear=None)
            actions = [action]
        return ol.ActionList(actions)
    
    def to_optilex_gs(self, choice: list[tuple[Group, BranchSet]], origins: list[BranchSet]) -> ol.GroupSelect:
        default_group, default_target = choice.pop(-1)
        outcomes: list[ol.Outcome] = []
        for group, target in choice:
            charset: ol.Charset = group.to_optilex()
            actions: ol.ActionList = target.to_optilex_al(origins=origins, origin=self)
            outcome: ol.Outcome = ol.Outcome(charset=charset, actions=actions)
            outcomes.append(outcome)
        outcomes: list[ol.Outcome] = list(sorted(outcomes, key=ol.Outcome.order))
        default: ol.ActionList = default_target.to_optilex_al(origins=origins, origin=self)
        block: ol.Block = ol.Block(outcomes=outcomes, default=default)
        origin_index: ol.Integer = ol.Integer.from_int(self.to_optilex_index(origins))
        return ol.GroupSelect(origin=origin_index, block=block)
    
    def to_optilex(self) -> ol.OriginSelect:
        origins, choices = make_origin_select(self)
        cases = [origin.to_optilex_gs(choice=choice, origins=origins) for origin, choice in zip(origins, choices)]
        return ol.OriginSelect(cases=cases)


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
    
    def as_grouping(self) -> GroupingGR:
        return Grouping(self)
    
    @classmethod
    def from_rules(cls, rules: typing.Iterator[ParallelGR], eager: bool = False) -> ParallelGR:
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
    
    def split_sequence(self) -> list[RepeatGR]:
        return [Grouping(self)]
    
    def split_parallel(self) -> list[SequenceGR]:
        return self.rules
    
    @property
    def hash_order(self) -> int:
        return 5
    
    @property
    def canonical(self) -> ParallelGR:
        rule_set = {rule.canonical for rule in self.rules}
        rules = sorted(rule_set, key=operator.attrgetter('hash_order'))
        return Parallel.from_rules(rules=rules)
    
    @property
    def is_optional(self) -> bool:
        return any((rule.is_optional for rule in self.rules))
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return frozenset((item for rule in self.rules for item in rule.alphabet))
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        for rule in self.rules:
            yield from rule.process()


@dataclasses.dataclass(frozen=True, order=True)
class SequenceGR(ParallelGR, abc.ABC):
    """
        >>> Sequence  # concrete
        >>> RepeatGR  # abstract
    """
    
    def split_parallel(self) -> list[SequenceGR]:
        return [self]


@dataclasses.dataclass(frozen=True, order=True)
class RepeatGR(SequenceGR, abc.ABC):
    """
        >>> Repeat  # concrete
        >>> GroupingGR  # abstract
    """
    
    def split_sequence(self) -> list[RepeatGR]:
        return [self]


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
    
    def as_grouping(self) -> GroupingGR:
        return Grouping(self)
    
    @classmethod
    def from_rules(cls, rules: typing.Iterator[ParallelGR]) -> SequenceGR:
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
    
    def split_sequence(self) -> list[RepeatGR]:
        return self.rules
    
    @property
    def hash_order(self) -> int:
        return 4
    
    @property
    def canonical(self) -> ParallelGR:
        return Sequence.from_rules((rule.canonical for rule in self.rules))
    
    @property
    def is_optional(self) -> bool:
        return all((rule.is_optional for rule in self.rules))
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return frozenset((item for rule in self.rules for item in rule.alphabet))
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        for index, base in enumerate(self.rules):
            then = Sequence.from_rules(self.rules[index + 1:])
            for group, rule in base.process():
                yield group, Sequence.from_rules([rule, then])
            if not base.is_optional:
                break


@dataclasses.dataclass(frozen=True, order=True)
class GroupingGR(RepeatGR, abc.ABC):
    """
        >>> Grouping  # concrete
        >>> MatchGR  # abstract
    """
    
    def as_grouping(self) -> GroupingGR:
        return self


@dataclasses.dataclass(frozen=True, order=True)
class Repeat(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Repeat := <LS> ?<Integer as mn> <COMMA> ?<Integer as mx> <RS> <GroupingGR as rule>
    """
    rule: GroupingGR
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
    
    def as_grouping(self) -> GroupingGR:
        return Grouping(self)
    
    @property
    def hash_order(self) -> int:
        return 3
    
    @property
    def canonical(self) -> ParallelGR:
        return self.rule.canonical.as_repeat(mn=self.mn, mx=self.mx)
    
    @property
    def is_optional(self) -> bool:
        return Integer.to_int(self.mn) == 0
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return self.rule.alphabet
    
    def repeat_minus_one(self) -> typing.Union[Valid, Error, Repeat]:
        mn = Integer.to_int(self.mn)
        mx = Integer.to_int(self.mx)
        if mx == 1:
            return Valid()
        mn = max(0, mn - 1)
        mx = max(0, mx - 1)
        return Repeat(rule=self.rule, mn=Integer.from_int(mn), mx=Integer.from_int(mx))
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        then = self.repeat_minus_one()
        for group, rule in self.rule.process():
            yield group, Sequence.from_rules([rule, then])


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
    def hash_order(self) -> int:
        return 2
    
    @property
    def canonical(self) -> ParallelGR:
        return self.rule.canonical
    
    @property
    def is_optional(self) -> bool:
        return self.rule.is_optional
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return self.rule.alphabet
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        yield from self.rule.process()


@dataclasses.dataclass(frozen=True, order=True)
class MatchGR(GroupingGR, abc.ABC):
    """
        >>> Match  # concrete
        >>> EmptyGR  # abstract
    """
    
    @property
    def canonical(self) -> ParallelGR:
        return self
    
    @property
    def is_optional(self) -> bool:
        return False


@dataclasses.dataclass(frozen=True, order=True)
class EmptyGR(MatchGR, abc.ABC):
    """
        >>> Valid  # concrete
        >>> Excluded  # concrete
        >>> Error  # concrete
    """
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return frozenset()


@dataclasses.dataclass(frozen=True, order=True)
class Match(MatchGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Match := <Group as group_>
    """
    group_: Group
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.group_)
    
    @property
    def hash_order(self) -> int:
        return 1
    
    @property
    def alphabet(self) -> typing.FrozenSet[str]:
        return self.group_.to_frozenset()
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        yield self.group_, VALID


@dataclasses.dataclass(frozen=True, order=True)
class Error(EmptyGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Error := <KW_ERROR>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'ERROR'
    
    @property
    def hash_order(self) -> int:
        return 0
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        raise TypeError('`website.language.semi.models.Error` objects should not be processed.')


@dataclasses.dataclass(frozen=True, order=True)
class Excluded(EmptyGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Excluded := <KW_EXCLUDED>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'EXCLUDED'
    
    @property
    def hash_order(self) -> int:
        return 0
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        yield from []
    
    def to_optilex(self) -> typing.Optional[ol.Include]:
        return None


@dataclasses.dataclass(frozen=True, order=True)
class Valid(EmptyGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Valid := <KW_VALID>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'VALID'
    
    @property
    def hash_order(self) -> int:
        return 0
    
    def process(self) -> typing.Iterator[tuple[Group, ParallelGR]]:
        yield ALWAYS, EXCLUDED
    
    def to_optilex(self) -> typing.Optional[ol.Include]:
        return ol.Include()

ALWAYS = Group(items=String(content=repr('')), inverted=Inverted())

NEVER = Group(items=String(content=repr('')), inverted=None)

VALID = Valid()

ERROR = Error()

EXCLUDED = Excluded()
