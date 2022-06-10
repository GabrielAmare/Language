"""
    This module has been auto-generated. Do not change manually.
    WARNING : Manual changes to this file are likely to be overwritten.
"""
from __future__ import annotations

import abc
import dataclasses
import string
import typing

from website.language.base.groups import Charset
from website.language.base.processing import Element, Lemma, Token

__all__ = [
    'AllGR',
    'AnyDigit',
    'AnyNonDigit',
    'AnyNonWhitespace',
    'AnyNonWord',
    'AnyWhitespace',
    'AnyWord',
    'AtomGR',
    'Character',
    'CharacterGR',
    'Dash',
    'Digit',
    'Dot',
    'EscapedCharacter',
    'GroupIgnore',
    'GroupInner',
    'GroupInnerGR',
    'GroupInnerNot',
    'GroupOuter',
    'GroupOuterGR',
    'Integer',
    'LazyRepeatPlus',
    'LazyRepeatStar',
    'NegativeLookAhead',
    'NegativeLookBehind',
    'Optional',
    'Parallel',
    'ParallelGR',
    'PositiveLookAhead',
    'PositiveLookBehind',
    'Range',
    'RangeGR',
    'Repeat',
    'RepeatGR',
    'RepeatPlus',
    'RepeatStar',
    'Sequence',
    'SequenceGR'
]


def _flat_str(method):
    def wrapped(self) -> str:
        return ''.join(method(self))
    return wrapped


@dataclasses.dataclass(frozen=True, order=True)
class AllGR(abc.ABC):
    """
        >>> ParallelGR  # abstract
        >>> Integer  # concrete
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @classmethod
    def parse(cls, obj: Element) -> AllGR:
        if obj.type == 'Integer':
            return Integer.parse(obj)
        else:
            return ParallelGR.parse(obj)


@dataclasses.dataclass(frozen=True, order=True)
class RangeGR(abc.ABC):
    """
        >>> Range  # concrete
        >>> AtomGR  # abstract
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @classmethod
    def parse(cls, obj: Element) -> RangeGR:
        if obj.type == 'Range':
            return Range.parse(obj)
        else:
            return AtomGR.parse(obj)
    
    @property
    @abc.abstractmethod
    def literal_chars(self) -> typing.FrozenSet[str]:
        """Return the literal characters that `self` refers to."""
    
    @property
    @abc.abstractmethod
    def as_inner_charset(self) -> Charset:
        """
                Return the Charset object corresponding to `self`.
                - Assuming `self` is an element inside a GroupInner | GroupInnerNot.
            
        """


@dataclasses.dataclass(frozen=True, order=True)
class Integer(AllGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Integer := +<Digit in digits>
    """
    digits: list[Digit]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for e in self.digits:
            yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Integer:
        assert isinstance(obj, Lemma)
        return cls(
            digits=[Digit.parse(item) for item in obj.data['digits']]
        )


@dataclasses.dataclass(frozen=True, order=True)
class ParallelGR(AllGR, abc.ABC):
    """
        >>> Parallel  # concrete
        >>> SequenceGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> ParallelGR:
        if obj.type == 'Parallel':
            return Parallel.parse(obj)
        else:
            return SequenceGR.parse(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Range(RangeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Range := <CharacterGR as start> <Dash> <CharacterGR as end>
    """
    start: CharacterGR
    end: CharacterGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.start)
        yield '-'
        yield str(self.end)
    
    @classmethod
    def parse(cls, obj: Element) -> Range:
        assert isinstance(obj, Lemma)
        return cls(
            start=CharacterGR.parse(obj.data['start']),
            end=CharacterGR.parse(obj.data['end'])
        )
    
    @property
    def as_char(self) -> str:
        raise NotImplementedError('no single character associated with a `Range` object.')
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        start = ord(self.start.as_char)
        end = ord(self.end.as_char) + 1
        assert start <= end, 'invalid character range !'
        return frozenset(map(chr, range(start, end)))
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        raise NotImplementedError('Range objects does not have outer charset.')


@dataclasses.dataclass(frozen=True, order=True)
class Parallel(ParallelGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Parallel := <VBAR>..<SequenceGR in items>
    """
    items: list[SequenceGR]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.items):
            if i:
                yield '|'
            yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Parallel:
        assert isinstance(obj, Lemma)
        return cls(
            items=[SequenceGR.parse(item) for item in obj.data['items']]
        )


@dataclasses.dataclass(frozen=True, order=True)
class SequenceGR(ParallelGR, abc.ABC):
    """
        >>> Sequence  # concrete
        >>> RepeatGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> SequenceGR:
        if obj.type == 'Sequence':
            return Sequence.parse(obj)
        else:
            return RepeatGR.parse(obj)


@dataclasses.dataclass(frozen=True, order=True)
class RepeatGR(SequenceGR, abc.ABC):
    """
        >>> LazyRepeatStar  # concrete
        >>> LazyRepeatPlus  # concrete
        >>> RepeatStar  # concrete
        >>> RepeatPlus  # concrete
        >>> Repeat  # concrete
        >>> Optional  # concrete
        >>> GroupOuterGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> RepeatGR:
        if obj.type == 'LazyRepeatStar':
            return LazyRepeatStar.parse(obj)
        elif obj.type == 'LazyRepeatPlus':
            return LazyRepeatPlus.parse(obj)
        elif obj.type == 'RepeatStar':
            return RepeatStar.parse(obj)
        elif obj.type == 'RepeatPlus':
            return RepeatPlus.parse(obj)
        elif obj.type == 'Repeat':
            return Repeat.parse(obj)
        elif obj.type == 'Optional':
            return Optional.parse(obj)
        else:
            return GroupOuterGR.parse(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Sequence(SequenceGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Sequence := {2,}<RepeatGR in items>
    """
    items: list[RepeatGR] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.items:
            for e in self.items:
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Sequence:
        assert isinstance(obj, Lemma)
        return cls(
            items=[RepeatGR.parse(item) for item in obj.data['items']] if 'items' in obj.data else None
        )


@dataclasses.dataclass(frozen=True, order=True)
class GroupOuterGR(RepeatGR, abc.ABC):
    """
        >>> PositiveLookAhead  # concrete
        >>> NegativeLookAhead  # concrete
        >>> PositiveLookBehind  # concrete
        >>> NegativeLookBehind  # concrete
        >>> GroupIgnore  # concrete
        >>> GroupOuter  # concrete
        >>> GroupInnerGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> GroupOuterGR:
        if obj.type == 'PositiveLookAhead':
            return PositiveLookAhead.parse(obj)
        elif obj.type == 'NegativeLookAhead':
            return NegativeLookAhead.parse(obj)
        elif obj.type == 'PositiveLookBehind':
            return PositiveLookBehind.parse(obj)
        elif obj.type == 'NegativeLookBehind':
            return NegativeLookBehind.parse(obj)
        elif obj.type == 'GroupIgnore':
            return GroupIgnore.parse(obj)
        elif obj.type == 'GroupOuter':
            return GroupOuter.parse(obj)
        else:
            return GroupInnerGR.parse(obj)


@dataclasses.dataclass(frozen=True, order=True)
class LazyRepeatPlus(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch LazyRepeatPlus := <GroupOuterGR as item> <PLUS> <INT>
    """
    item: GroupOuterGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.item)
        yield '+'
        yield '?'
    
    @classmethod
    def parse(cls, obj: Element) -> LazyRepeatPlus:
        assert isinstance(obj, Lemma)
        return cls(
            item=GroupOuterGR.parse(obj.data['item'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class LazyRepeatStar(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch LazyRepeatStar := <GroupOuterGR as item> <ASTERISK> <INT>
    """
    item: GroupOuterGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.item)
        yield '*'
        yield '?'
    
    @classmethod
    def parse(cls, obj: Element) -> LazyRepeatStar:
        assert isinstance(obj, Lemma)
        return cls(
            item=GroupOuterGR.parse(obj.data['item'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Optional(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Optional := <GroupOuterGR as item> <INT>
    """
    item: GroupOuterGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.item)
        yield '?'
    
    @classmethod
    def parse(cls, obj: Element) -> Optional:
        assert isinstance(obj, Lemma)
        return cls(
            item=GroupOuterGR.parse(obj.data['item'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Repeat(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Repeat := <GroupOuterGR as item> <LS> ?<Integer as mn> <COMMA> ?<Integer as mx> <RS>
    """
    item: GroupOuterGR
    mn: Integer | None = None
    mx: Integer | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.item)
        yield '{'
        if self.mn:
            yield str(self.mn)
        yield ','
        if self.mx:
            yield str(self.mx)
        yield '}'
    
    @classmethod
    def parse(cls, obj: Element) -> Repeat:
        assert isinstance(obj, Lemma)
        return cls(
            item=GroupOuterGR.parse(obj.data['item']),
            mn=Integer.parse(obj.data['mn']) if 'mn' in obj.data else None,
            mx=Integer.parse(obj.data['mx']) if 'mx' in obj.data else None
        )


@dataclasses.dataclass(frozen=True, order=True)
class RepeatPlus(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch RepeatPlus := <GroupOuterGR as item> <PLUS>
    """
    item: GroupOuterGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.item)
        yield '+'
    
    @classmethod
    def parse(cls, obj: Element) -> RepeatPlus:
        assert isinstance(obj, Lemma)
        return cls(
            item=GroupOuterGR.parse(obj.data['item'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class RepeatStar(RepeatGR):
    """
        This class has been generated automatically from the bnf rule :
        branch RepeatStar := <GroupOuterGR as item> <ASTERISK>
    """
    item: GroupOuterGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.item)
        yield '*'
    
    @classmethod
    def parse(cls, obj: Element) -> RepeatStar:
        assert isinstance(obj, Lemma)
        return cls(
            item=GroupOuterGR.parse(obj.data['item'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class GroupIgnore(GroupOuterGR):
    """
        This class has been generated automatically from the bnf rule :
        branch GroupIgnore := <LEFT_PARENTHESIS> <INT> <COLON> *<ParallelGR in items> <RIGHT_PARENTHESIS>
    """
    items: list[ParallelGR] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        yield '?'
        yield ':'
        if self.items:
            for e in self.items:
                yield str(e)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> GroupIgnore:
        assert isinstance(obj, Lemma)
        return cls(
            items=[ParallelGR.parse(item) for item in obj.data['items']] if 'items' in obj.data else None
        )


@dataclasses.dataclass(frozen=True, order=True)
class GroupInnerGR(GroupOuterGR, abc.ABC):
    """
        >>> GroupInner  # concrete
        >>> GroupInnerNot  # concrete
        >>> AtomGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> GroupInnerGR:
        if obj.type == 'GroupInner':
            return GroupInner.parse(obj)
        elif obj.type == 'GroupInnerNot':
            return GroupInnerNot.parse(obj)
        else:
            return AtomGR.parse(obj)
    
    @property
    @abc.abstractmethod
    def as_outer_charset(self) -> Charset:
        """
                Return the Charset object corresponding to `self`.
                - Assuming `self` is not an element inside a GroupInner | GroupInnerNot.
            
        """


@dataclasses.dataclass(frozen=True, order=True)
class GroupOuter(GroupOuterGR):
    """
        This class has been generated automatically from the bnf rule :
        branch GroupOuter := <LEFT_PARENTHESIS> *<ParallelGR in items> <RIGHT_PARENTHESIS>
    """
    items: list[ParallelGR] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        if self.items:
            for e in self.items:
                yield str(e)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> GroupOuter:
        assert isinstance(obj, Lemma)
        return cls(
            items=[ParallelGR.parse(item) for item in obj.data['items']] if 'items' in obj.data else None
        )


@dataclasses.dataclass(frozen=True, order=True)
class NegativeLookAhead(GroupOuterGR):
    """
        This class has been generated automatically from the bnf rule :
        branch NegativeLookAhead := <LEFT_PARENTHESIS> <INT> <EXC> <ParallelGR as rule> <RIGHT_PARENTHESIS>
    """
    rule: ParallelGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        yield '?'
        yield '!'
        yield str(self.rule)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> NegativeLookAhead:
        assert isinstance(obj, Lemma)
        return cls(
            rule=ParallelGR.parse(obj.data['rule'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class NegativeLookBehind(GroupOuterGR):
    """
        This class has been generated automatically from the bnf rule :
        branch NegativeLookBehind := <LEFT_PARENTHESIS> <INT> <LV> <EXC> <ParallelGR as rule> <RIGHT_PARENTHESIS>
    """
    rule: ParallelGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        yield '?'
        yield '<'
        yield '!'
        yield str(self.rule)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> NegativeLookBehind:
        assert isinstance(obj, Lemma)
        return cls(
            rule=ParallelGR.parse(obj.data['rule'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class PositiveLookAhead(GroupOuterGR):
    """
        This class has been generated automatically from the bnf rule :
        branch PositiveLookAhead := <LEFT_PARENTHESIS> <INT> <EQ> <ParallelGR as rule> <RIGHT_PARENTHESIS>
    """
    rule: ParallelGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        yield '?'
        yield '='
        yield str(self.rule)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> PositiveLookAhead:
        assert isinstance(obj, Lemma)
        return cls(
            rule=ParallelGR.parse(obj.data['rule'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class PositiveLookBehind(GroupOuterGR):
    """
        This class has been generated automatically from the bnf rule :
        branch PositiveLookBehind := <LEFT_PARENTHESIS> <INT> <LV> <EQ> <ParallelGR as rule> <RIGHT_PARENTHESIS>
    """
    rule: ParallelGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        yield '?'
        yield '<'
        yield '='
        yield str(self.rule)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> PositiveLookBehind:
        assert isinstance(obj, Lemma)
        return cls(
            rule=ParallelGR.parse(obj.data['rule'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class AtomGR(GroupInnerGR, RangeGR, abc.ABC):
    """
        >>> AnyDigit  # atomic
        >>> AnyWhitespace  # atomic
        >>> AnyWord  # atomic
        >>> AnyNonDigit  # atomic
        >>> AnyNonWhitespace  # atomic
        >>> AnyNonWord  # atomic
        >>> EscapedCharacter  # atomic
        >>> CharacterGR  # abstract
    """
    content: str
    
    @classmethod
    def parse(cls, obj: Element) -> AtomGR:
        if obj.type == 'AnyDigit':
            return AnyDigit.parse(obj)
        elif obj.type == 'AnyWhitespace':
            return AnyWhitespace.parse(obj)
        elif obj.type == 'AnyWord':
            return AnyWord.parse(obj)
        elif obj.type == 'AnyNonDigit':
            return AnyNonDigit.parse(obj)
        elif obj.type == 'AnyNonWhitespace':
            return AnyNonWhitespace.parse(obj)
        elif obj.type == 'AnyNonWord':
            return AnyNonWord.parse(obj)
        elif obj.type == 'EscapedCharacter':
            return EscapedCharacter.parse(obj)
        else:
            return CharacterGR.parse(obj)
    
    @property
    @abc.abstractmethod
    def as_char(self) -> str:
        """Return the character corresponding to `self`."""


@dataclasses.dataclass(frozen=True, order=True)
class GroupInner(GroupInnerGR):
    """
        This class has been generated automatically from the bnf rule :
        branch GroupInner := <LB> *<RangeGR in items> <RB>
    """
    items: list[RangeGR] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '['
        if self.items:
            for e in self.items:
                yield str(e)
        yield ']'
    
    @classmethod
    def parse(cls, obj: Element) -> GroupInner:
        assert isinstance(obj, Lemma)
        return cls(
            items=[RangeGR.parse(item) for item in obj.data['items']] if 'items' in obj.data else None
        )
    
    @property
    def as_outer_charset(self) -> Charset:
        charsets = [item.as_inner_charset for item in self.items]
        return Charset.union(*charsets)


@dataclasses.dataclass(frozen=True, order=True)
class GroupInnerNot(GroupInnerGR):
    """
        This class has been generated automatically from the bnf rule :
        branch GroupInnerNot := <LB> <HAT> *<RangeGR in items> <RB>
    """
    items: list[RangeGR] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '['
        yield '^'
        if self.items:
            for e in self.items:
                yield str(e)
        yield ']'
    
    @classmethod
    def parse(cls, obj: Element) -> GroupInnerNot:
        assert isinstance(obj, Lemma)
        return cls(
            items=[RangeGR.parse(item) for item in obj.data['items']] if 'items' in obj.data else None
        )
    
    @property
    def as_outer_charset(self) -> Charset:
        charsets = [item.as_inner_charset for item in self.items]
        return Charset.union(*charsets).complement


@dataclasses.dataclass(frozen=True, order=True)
class AnyDigit(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        string [5] AnyDigit '\\d'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> AnyDigit:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def as_char(self) -> str:
        assert len(self.content) == 2, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[1]
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(string.digits)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class AnyNonDigit(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        string [5] AnyNonDigit '\\D'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> AnyNonDigit:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def as_char(self) -> str:
        assert len(self.content) == 2, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[1]
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(string.digits)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=True)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class AnyNonWhitespace(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        string [5] AnyNonWhitespace '\\S'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> AnyNonWhitespace:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(string.whitespace)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=True)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class AnyNonWord(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        string [5] AnyNonWord '\\W'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> AnyNonWord:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(string.ascii_letters + string.digits + '_')
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=True)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class AnyWhitespace(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        string [5] AnyWhitespace '\\s'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> AnyWhitespace:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def as_char(self) -> str:
        assert len(self.content) == 2, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[1]
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(string.whitespace)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class AnyWord(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        string [5] AnyWord '\\w'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> AnyWord:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def as_char(self) -> str:
        assert len(self.content) == 2, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[1]
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(string.ascii_letters + string.digits + '_')
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class CharacterGR(AtomGR, abc.ABC):
    """
        >>> Dot  # atomic
        >>> Dash  # atomic
        >>> Digit  # atomic
        >>> Character  # atomic
    """
    @classmethod
    def parse(cls, obj: Element) -> CharacterGR:
        if obj.type == 'Dot':
            return Dot.parse(obj)
        elif obj.type == 'Dash':
            return Dash.parse(obj)
        elif obj.type == 'Digit':
            return Digit.parse(obj)
        elif obj.type == 'Character':
            return Character.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @property
    def as_char(self) -> str:
        assert len(self.content) == 1, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[0]


@dataclasses.dataclass(frozen=True, order=True)
class EscapedCharacter(AtomGR):
    """
        This class has been generated automatically from the bnf rule :
        regex  [1] EscapedCharacter '\\\\\\\\.'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> EscapedCharacter:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def as_char(self) -> str:
        assert len(self.content) == 2, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[1]
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(self.as_char)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class Character(CharacterGR):
    """
        This class has been generated automatically from the bnf rule :
        regex  [3] Character '.'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Character:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(self.as_char)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class Dash(CharacterGR):
    """
        This class has been generated automatically from the bnf rule :
        string [4] Dash '-'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Dash:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(self.as_char)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class Digit(CharacterGR):
    """
        This class has been generated automatically from the bnf rule :
        regex  [2] Digit '\\d'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Digit:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(self.as_char)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return self.as_inner_charset


@dataclasses.dataclass(frozen=True, order=True)
class Dot(CharacterGR):
    """
        This class has been generated automatically from the bnf rule :
        string [4] Dot '.'
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Dot:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @property
    def literal_chars(self) -> typing.FrozenSet[str]:
        return frozenset(self.as_char)
    
    @property
    def as_inner_charset(self) -> Charset:
        return Charset(items=self.literal_chars, inverted=False)
    
    @property
    def as_outer_charset(self) -> Charset:
        return Charset(items=frozenset(''), inverted=True)
