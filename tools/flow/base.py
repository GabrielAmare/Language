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
class Handler(typing.Generic[C, E]):
    condition: Condition[E]
    action: Action[C, E]
    
    def __str__(self):
        return f"{self.condition!s}: {self.action!s}"


@dataclasses.dataclass
class Manager(typing.Generic[C, E]):
    handlers: list[Handler[C, E]] = dataclasses.field(default_factory=list)
    default: Action[C, E] | None = None
    
    def __str__(self) -> str:
        if self.default is None:
            return "\n".join(map(str, self.handlers))
        else:
            return "\n".join(map(str, self.handlers)) + "\ndefault: " + str(self.default)
    
    def verify(self, element: E) -> bool:
        return any(handler.condition.verify(element) for handler in self.handlers)
    
    def get_action(self, element: E) -> Action[C, E]:
        for handler in self.handlers:
            if handler.condition.verify(element):
                return handler.action
        return self.default


def indent(s: str) -> str:
    return '\n'.join('  ' + line for line in s.split('\n'))


@dataclasses.dataclass
class Flow(typing.Generic[C, E], abc.ABC):
    managers: dict[int, Manager[C, E]] = dataclasses.field(default_factory=dict)
    
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
            action: Action = manager.get_action(element)
            if action is None:
                raise NotImplementedError
            state, element = action.execute(context, element)
        return state
    
    def run(self, context: C, elements: typing.Iterable[E]) -> int:
        state = 0
        for element in elements:
            state = self._on(state, context, element)
        state = self._on(state, context, self.eot())
        return state
