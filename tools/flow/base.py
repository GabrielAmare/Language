import abc
import dataclasses
import typing

__all__ = [
    'Condition',
    'Action',
    'Handler',
    'Manager',
    'Flow',
]

E = typing.TypeVar('E')
C = typing.TypeVar('C')


class AbstractCondition(typing.Generic[E], abc.ABC):
    @abc.abstractmethod
    def verify(self, element: E) -> bool:
        """"""


class AbstractAction(typing.Generic[C, E], abc.ABC):
    @abc.abstractmethod
    def execute(self, context: C, element: E) -> tuple[int, E | None]:
        """"""


class Condition(typing.Generic[E], AbstractCondition[E], abc.ABC):
    pass


class Action(typing.Generic[C, E], AbstractAction[C, E], abc.ABC):
    @abc.abstractmethod
    def execute(self, context: C, element: E) -> tuple[int, E | None]:
        """"""


@dataclasses.dataclass
class Handler(typing.Generic[E]):
    condition: Condition[E]
    action: int
    
    def __str__(self):
        return f"{self.condition!s}: {self.action!s}"


@dataclasses.dataclass
class Manager(typing.Generic[E]):
    handlers: list[Handler[E]] = dataclasses.field(default_factory=list)
    default: int | None = None
    
    def __str__(self) -> str:
        if self.default is None:
            return "\n".join(map(str, self.handlers))
        else:
            return "\n".join(map(str, self.handlers)) + "\ndefault: " + str(self.default)
    
    def verify(self, element: E) -> bool:
        return any(handler.condition.verify(element) for handler in self.handlers)
    
    def get_action(self, element: E) -> int | None:
        for handler in self.handlers:
            if handler.condition.verify(element):
                return handler.action
        return self.default


def indent(s: str) -> str:
    return '\n'.join('  ' + line for line in s.split('\n'))


@dataclasses.dataclass
class Flow(typing.Generic[C, E], abc.ABC):
    managers: dict[int, Manager[E]] = dataclasses.field(default_factory=dict)
    actions: list[Action[C, E]] = dataclasses.field(default_factory=list)
    
    @abc.abstractmethod
    def eot(self) -> E:
        """"""
    
    @property
    def states(self) -> list[int]:
        return sorted(self.managers.keys())
    
    def __str__(self):
        return "\n\n".join(f"{state} [\n{indent(str(self.managers[state]))}\n]" for state in self.states)
    
    def _on(self, state: int, context: C, element: E) -> int:
        while element:
            manager: Manager = self.managers[state]
            action_index: int = manager.get_action(element)
            action: Action = self.actions[action_index]
            state, element = action.execute(context, element)
        return state
    
    def run(self, context: C, elements: typing.Iterable[E]) -> int:
        state = 0
        for element in elements:
            state = self._on(state, context, element)
        state = self._on(state, context, self.eot())
        return state
    
    def add_action(self, action: Action[C, E]) -> int:
        """Add an action to the list and return its index. If the action already exists, only return its index."""
        try:
            return self.actions.index(action)
        except ValueError:
            index = len(self.actions)
            self.actions.append(action)
            return index
    
    def set_default(self, state: int, action: Action[C, E]) -> None:
        action_index: int = self.add_action(action)
        self.managers[state].default = action_index
    
    def add_handler(self, state: int, handler: Handler[E]) -> None:
        self.managers[state].handlers.append(handler)
