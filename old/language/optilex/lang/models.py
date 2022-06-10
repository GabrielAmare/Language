"""
    This module has been auto-generated. Do not change manually.
    WARNING : Manual changes to this file are likely to be overwritten.
"""
from __future__ import annotations

import abc
import dataclasses
import typing

from website.language.base.processing import Element, Lemma, Token

__all__ = [
    'Action',
    'ActionList',
    'All',
    'Block',
    'Charset',
    'Clear',
    'GroupSelect',
    'Include',
    'Integer',
    'Inverted',
    'OriginSelect',
    'Outcome',
    'String',
    'Variable'
]


def _flat_str(method):
    def wrapped(self) -> str:
        return ''.join(method(self))
    return wrapped


def _indented(prefix: str):
    def wrapper(method):
        def wrapped(self) -> str:
            return method(self).replace('\n', '\n' + prefix)
        return wrapped
    return wrapper


@dataclasses.dataclass
class All(abc.ABC):
    """
        >>> ActionList  # concrete
        >>> Action  # concrete
        >>> Charset  # concrete
        >>> Outcome  # concrete
        >>> Block  # concrete
        >>> GroupSelect  # concrete
        >>> OriginSelect  # concrete
        >>> Include  # concrete
        >>> Inverted  # concrete
        >>> Clear  # concrete
        >>> Integer  # atomic
        >>> Variable  # atomic
        >>> String  # atomic
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @classmethod
    def parse(cls, obj: Element) -> All:
        if obj.type == 'ActionList':
            return ActionList.parse(obj)
        elif obj.type == 'Action':
            return Action.parse(obj)
        elif obj.type == 'Charset':
            return Charset.parse(obj)
        elif obj.type == 'Outcome':
            return Outcome.parse(obj)
        elif obj.type == 'Block':
            return Block.parse(obj)
        elif obj.type == 'GroupSelect':
            return GroupSelect.parse(obj)
        elif obj.type == 'OriginSelect':
            return OriginSelect.parse(obj)
        elif obj.type == 'Include':
            return Include.parse(obj)
        elif obj.type == 'Inverted':
            return Inverted.parse(obj)
        elif obj.type == 'Clear':
            return Clear.parse(obj)
        elif obj.type == 'Integer':
            return Integer.parse(obj)
        elif obj.type == 'Variable':
            return Variable.parse(obj)
        elif obj.type == 'String':
            return String.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass
class Action(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Action := ?$' ' <Include as include_> ?$' ' <KW_BUILD> <LEFT_PARENTHESIS> <Variable as build> <RIGHT_PAR…
    """
    include_: Include | None = None
    build: Variable | None = None
    goto: Integer | None = None
    clear: Clear | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.include_:
            yield ' '
            yield str(self.include_)
        if self.build:
            yield ' '
            yield 'BUILD'
            yield '('
            yield str(self.build)
            yield ')'
        if self.goto:
            yield ' '
            yield 'GOTO'
            yield '('
            yield str(self.goto)
            yield ')'
        if self.clear:
            yield ' '
            yield str(self.clear)
    
    @classmethod
    def parse(cls, obj: Element) -> Action:
        assert isinstance(obj, Lemma)
        return cls(
            include_=Include.parse(obj.data['include_']) if 'include_' in obj.data else None,
            build=Variable.parse(obj.data['build']) if 'build' in obj.data else None,
            goto=Integer.parse(obj.data['goto']) if 'goto' in obj.data else None,
            clear=Clear.parse(obj.data['clear']) if 'clear' in obj.data else None
        )
    
    def order(self) -> tuple[int, int, int, int]:
        x = 0 if self.build else 1
        y = 0 if self.include_ else 1
        z, t = (0, self.goto.value) if self.goto else (1, 0)
        return x, y, z, t


@dataclasses.dataclass
class ActionList(All):
    """
        This class has been generated automatically from the bnf rule :
        branch ActionList := $' ' <AMPERSAND> $' '..<Action in items>
    """
    items: list[Action]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.items):
            if i:
                yield ' '
                yield '&'
                yield ' '
            yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> ActionList:
        assert isinstance(obj, Lemma)
        return cls(
            items=[Action.parse(item) for item in obj.data['items']]
        )
    
    def order(self) -> tuple[int, tuple[tuple[int, int, int, int], ...]]:
        return len(self.items), tuple(map(Action.order, self.items))


@dataclasses.dataclass
class Block(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Block '    ' := *<Outcome in outcomes> ?$'\\n' <KW_DEFAULT> <COLON> $' ' <ActionList as default>
    """
    outcomes: list[Outcome] | None = None
    default: ActionList | None = None
    
    @_indented('    ')
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.outcomes:
            for e in self.outcomes:
                yield str(e)
        if self.default:
            yield '\n'
            yield 'DEFAULT'
            yield ':'
            yield ' '
            yield str(self.default)
    
    @classmethod
    def parse(cls, obj: Element) -> Block:
        assert isinstance(obj, Lemma)
        return cls(
            outcomes=[Outcome.parse(item) for item in obj.data['outcomes']] if 'outcomes' in obj.data else None,
            default=ActionList.parse(obj.data['default']) if 'default' in obj.data else None
        )


@dataclasses.dataclass
class Charset(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Charset := ?<Inverted as inverted> <String as items>
    """
    items: String
    inverted: Inverted | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.inverted:
            yield str(self.inverted)
        yield str(self.items)
    
    @classmethod
    def parse(cls, obj: Element) -> Charset:
        assert isinstance(obj, Lemma)
        return cls(
            items=String.parse(obj.data['items']),
            inverted=Inverted.parse(obj.data['inverted']) if 'inverted' in obj.data else None
        )
    
    def order(self) -> tuple[int, str]:
        content = ''.join(sorted(self.items.value))
        size = len(content)
        return size, content


@dataclasses.dataclass
class Clear(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Clear := <KW_CLEAR>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'CLEAR'
    
    @classmethod
    def parse(cls, obj: Element) -> Clear:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass
class GroupSelect(All):
    """
        This class has been generated automatically from the bnf rule :
        branch GroupSelect := <Integer as origin> $' ' <LS> <Block as block> $'\\n' <RS>
    """
    origin: Integer
    block: Block
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.origin)
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    @classmethod
    def parse(cls, obj: Element) -> GroupSelect:
        assert isinstance(obj, Lemma)
        return cls(
            origin=Integer.parse(obj.data['origin']),
            block=Block.parse(obj.data['block'])
        )


@dataclasses.dataclass
class Include(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Include := <KW_INCLUDE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'INCLUDE'
    
    @classmethod
    def parse(cls, obj: Element) -> Include:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass
class Integer(All):
    """
        This class has been generated automatically from the bnf rule :
        regex   Integer '\\-?\\d+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Integer:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @classmethod
    def from_int(cls, __value: int) -> Integer:
        return cls(content=repr(__value))
    
    @property
    def value(self) -> int:
        return int(self.content)


@dataclasses.dataclass
class Inverted(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Inverted := <KW_NOT>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'NOT'
    
    @classmethod
    def parse(cls, obj: Element) -> Inverted:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass
class OriginSelect(All):
    """
        This class has been generated automatically from the bnf rule :
        branch OriginSelect := $'\\n'.<GroupSelect in cases>
    """
    cases: list[GroupSelect]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.cases:
            for i, e in enumerate(self.cases):
                if i:
                    yield '\n'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> OriginSelect:
        assert isinstance(obj, Lemma)
        return cls(
            cases=[GroupSelect.parse(item) for item in obj.data['cases']]
        )


@dataclasses.dataclass
class Outcome(All):
    """
        This class has been generated automatically from the bnf rule :
        branch Outcome := $'\\n' <Charset as charset> <COLON> $' ' <ActionList as actions>
    """
    charset: Charset
    actions: ActionList
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '\n'
        yield str(self.charset)
        yield ':'
        yield ' '
        yield str(self.actions)
    
    @classmethod
    def parse(cls, obj: Element) -> Outcome:
        assert isinstance(obj, Lemma)
        return cls(
            charset=Charset.parse(obj.data['charset']),
            actions=ActionList.parse(obj.data['actions'])
        )
    
    def order(self) -> tuple[int, int, tuple[tuple[int, int, int, int], ...], str]:
        n_chars, content = self.charset.order()
        n_actions, args = self.actions.order()
        return n_chars, n_actions, args, content


@dataclasses.dataclass
class String(All):
    """
        This class has been generated automatically from the bnf rule :
        regex   String '\\"(?:\\\\\\"|[^\\"])*?\\"|\\'(?:\\\\\\'|[^\\'])*?\\''
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> String:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @classmethod
    def from_str(cls, __value: str) -> String:
        return cls(content=repr(__value))
    
    @property
    def value(self) -> str:
        return eval(self.content)


@dataclasses.dataclass
class Variable(All):
    """
        This class has been generated automatically from the bnf rule :
        regex   Variable '[a-zA-Z_]\\w*'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Variable:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @classmethod
    def from_str(cls, __value: str) -> Variable:
        return cls(content=__value)
