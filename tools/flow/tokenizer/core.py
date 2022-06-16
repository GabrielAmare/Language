from __future__ import annotations

import dataclasses
import functools
import typing

from ... import flow
from .base import *
from .data import *

__all__ = [
    'Condition',
    'Action',
    'Handler',
    'Manager',
    'Flow',
]


@dataclasses.dataclass
class Condition(flow.Condition):
    chars: str

    def __str__(self) -> str:
        return repr(''.join(sorted(set(self.chars))))

    def verify(self, char) -> bool:
        return char in self.chars

    def then(self, action: Action) -> Handler:
        return Handler(condition=self, action=action)

    def shadows(self, other: Condition) -> bool:
        return any(map(self.chars.__contains__, other.chars))

    @property
    def data(self) -> ConditionData:
        return ''.join(sorted(set(self.chars)))


@dataclasses.dataclass
class Action(flow.Action):
    add: bool
    use: bool
    clr: bool
    _build: str | None
    to: int

    def __str__(self) -> str:
        parts = []
        if self.add:
            parts.append("add()")

        if self.use:
            parts.append("use()")

        if self._build:
            parts.append(f"build({self._build!r})")

        parts.append(f"goto({self.to})")
        return " -> ".join(parts)

    def execute(self, context: Context, element: str) -> tuple[int, str | None]:
        if self.add:
            context.content += element

        if self.use:
            context.to += 1

        if self.clr:
            element = None

        if self._build:
            token = Token(type=self._build, content=context.content, at=context.at, to=context.to)
            context.tokens.append(token)
            context.content = ''
            context.at = context.to

        return self.to, element

    @property
    def data(self) -> ActionData:
        return int(self.add), int(self.use), int(self.clr), '' if self._build is None else self._build, self.to


@dataclasses.dataclass
class Handler(flow.Handler):
    condition: Condition
    action: Action

    def __str__(self):
        return f"{self.condition!s}: {self.action!s}"

    def shadows(self, other: Handler) -> bool:
        return self.condition.shadows(other.condition)

    @property
    def data(self) -> HandlerData:
        return self.condition.data, self.action.data


@dataclasses.dataclass
class Manager(flow.Manager):
    handlers: list[Handler] = dataclasses.field(default_factory=list)
    default: Action | None = None

    def __str__(self) -> str:
        if self.default is None:
            return "\n".join(map(str, self.handlers))
        else:
            return "\n".join(map(str, self.handlers)) + "\ndefault: " + str(self.default)

    def __iadd__(self, other: Handler) -> Manager:
        # for handler in self.handlers:
        #     if handler.shadows(other):
        #         raise ValueError(f"{handler} is shadowing {other}")
        self.handlers.append(other)
        return self

    @property
    def data(self) -> ManagerData:
        return [handler.data for handler in self.handlers], None if self.default is None else self.default.data


def indent(s: str) -> str:
    return '\n'.join('  ' + line for line in s.split('\n'))


@dataclasses.dataclass
class Flow(flow.Flow):
    managers: dict[int, Manager] = dataclasses.field(default_factory=dict)
    omits: set[str] = dataclasses.field(default_factory=set)

    @property
    def states(self) -> list[int]:
        return sorted(self.managers.keys())

    def __str__(self):
        return "\n\n".join(f"{state} [\n{indent(str(self.managers[state]))}\n]" for state in self.states)

    def eot(self) -> str:
        return EOT

    def new_state(self) -> int:
        return max(self.managers.keys(), default=0) + 1

    def __getitem__(self, state: int):
        if state in self.managers:
            manager = self.managers[state]
        else:
            manager = self.managers[state] = Manager()

        return manager

    def __setitem__(self, state: int, manager: Manager) -> None:
        self.managers[state] = manager

    def omit(self, *types: str) -> None:
        self.omits = self.omits.union(set(types))

    def __call__(self, src: str) -> typing.Iterator[Token]:
        context = Context()
        state = self.run(context, src)

        for token in context.tokens:
            if token.type not in self.omits:
                yield token

        # if state == ERROR:
        #     raise TokenizerError(Token(type='$ERROR', content=context.content, at=context.at, to=context.to))

    @functools.cached_property
    def max_build_size(self) -> int:
        sizes = set()
        for manager in self.managers.values():
            for handler in manager.handlers:
                build = handler.action._build
                if isinstance(build, str):
                    sizes.add(len(build))

            build = manager.default._build
            if isinstance(build, str):
                sizes.add(len(build))

        return max(sizes, default=0)

    def format_token(self, token: Token) -> str:
        """Return a displayable expression that represent the token."""
        return f"{token.type.ljust(self.max_build_size)} | {token.content!r}"

    def display(self, src: str) -> None:
        for token in self(src):
            print(self.format_token(token))

    @property
    def data(self) -> FlowData:
        state = 0
        data: list[ManagerData] = []
        while state in self.managers:
            data.append(self.managers[state].data)
            state += 1
        data.append([[], 0])  # FOR VALID STATE (-1)
        data.append([[], 0])  # FOR ERROR STATE (-2)
        return data, sorted(self.omits)
