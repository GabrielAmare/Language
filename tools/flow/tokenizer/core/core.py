from __future__ import annotations

import dataclasses
import typing

from tools import flow
from .base import *
from .data import *

__all__ = [
    'Condition',
    'Params',
    'Action',
    'Handler',
    'Manager',
    'Flow',
]


@dataclasses.dataclass(unsafe_hash=True)
class Condition(flow.Condition[str]):
    chars: str
    
    def __str__(self) -> str:
        return repr(''.join(sorted(set(self.chars))))
    
    def verify(self, char: str) -> bool:
        return char in self.chars
    
    def then(self, action: Action) -> Handler:
        return Handler(condition=self, action=action)
    
    def shadows(self, other: Condition) -> bool:
        return any(map(self.chars.__contains__, other.chars))
    
    @property
    def data(self) -> ConditionData:
        return ''.join(sorted(set(self.chars)))


@dataclasses.dataclass(unsafe_hash=True)
class Params:
    options: int
    build: str  # Build a token with the given type.
    
    def __str__(self) -> str:
        parts = []
        
        if self.options & ADD:
            parts.append("add()")
        
        if self.options & INC:
            parts.append("inc()")
        
        if self.options & CLR:
            parts.append("clr()")
        
        if self.build:
            parts.append(f"build({self.build!r})")
        
        if self.options & CLEAR:
            parts.append("clear()")
        
        return " & ".join(parts)
    
    def execute(self, context: Context, element: str) -> str | None:
        if self.options & ADD:
            context.content += element
        
        if self.options & INC:
            context.to += 1
            if element == '\n':
                context.at_row += 1
                context.at_col = 0
            else:
                context.at_col += 1
        
        if self.options & CLR:
            element = None
        
        if self.build:
            token = Token(type=self.build, content=context.content,
                          at=context.at, to=context.to,
                          at_row=context.at_row, at_col=context.at_col,
                          to_row=context.to_row, to_col=context.to_col)
            context.tokens.append(token)
        
        if self.options & CLEAR:
            context.content = ''
            context.at = context.to
            context.at_row = context.to_row
            context.at_col = context.to_col
        
        return element
    
    @property
    def data(self) -> ActionParamsData:
        return self.options, self.build


@dataclasses.dataclass(unsafe_hash=True)
class Action(flow.Action[Context, str]):
    params: Params
    to: int
    
    def __str__(self) -> str:
        return f"{self.params!s} -> goto({self.to})"
    
    def execute(self, context: Context, element: str) -> tuple[int, str | None]:
        return self.to, self.params.execute(context, element)
    
    @property
    def data(self) -> ActionData:
        return self.params.data, self.to


@dataclasses.dataclass
class Handler(flow.Handler[str]):
    condition: Condition
    action: int
    
    def shadows(self, other: Handler) -> bool:
        return self.condition.shadows(other.condition)
    
    @property
    def data(self) -> HandlerData:
        return self.condition.data, self.action


@dataclasses.dataclass
class Manager(flow.Manager[str]):
    handlers: list[Handler] = dataclasses.field(default_factory=list)
    default: int | None = None
    
    @property
    def data(self) -> ManagerData:
        return [handler.data for handler in self.handlers], self.default


@dataclasses.dataclass
class Flow(flow.Flow[Context, str]):
    managers: dict[int, Manager] = dataclasses.field(default_factory=dict)
    actions: list[Action] = dataclasses.field(default_factory=list)
    
    def eot(self) -> str:
        return EOT
    
    def new_state(self) -> int:
        return max(self.managers.keys(), default=0) + 1
    
    def __call__(self, src: str) -> typing.Iterator[Token]:
        context = Context()
        state = 0
        
        for state in self.run(context, src):
            while context.tokens:
                yield context.tokens.pop(0)
        
        # if state == ERROR:
        #     raise TokenizerError(Token(type='$ERROR', content=context.content, at=context.at, to=context.to))
    
    @property
    def data(self) -> FlowData:
        state = 0
        data: list[ManagerData] = []
        while state in self.managers:
            data.append(self.managers[state].data)
            state += 1
        return data, [action.data for action in self.actions]
