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
class Handler(typing.Generic[C, E], AbstractCondition[E], AbstractAction[C, E]):
    condition: Condition[E]
    action: Action[C, E]
    
    def verify(self, element: E) -> bool:
        return self.condition.verify(element)
    
    def execute(self, context: C, element: E) -> tuple[int, E | None]:
        return self.action.execute(context, element)


@dataclasses.dataclass
class Manager(typing.Generic[C, E]):
    handlers: list[Handler[C, E]] = dataclasses.field(default_factory=list)
    default: Action[C, E] | None = None
    
    def verify(self, element: E) -> bool:
        return any(handler.verify(element) for handler in self.handlers)
    
    def on(self, context: C, element: E) -> tuple[int, E | None]:
        for handler in self.handlers:
            if handler.verify(element):
                return handler.execute(context, element)
        
        else:
            if self.default is None:
                raise NotImplementedError
            
            return self.default.execute(context, element)


@dataclasses.dataclass
class Flow(typing.Generic[C, E], abc.ABC):
    managers: dict[int, Manager[C, E]] = dataclasses.field(default_factory=dict)
    
    @abc.abstractmethod
    def eot(self) -> E:
        """"""
    
    def _on(self, state: int, context: C, element: E) -> int:
        while element:
            manager = self.managers[state]
            state, element = manager.on(context, element)
        return state
    
    def run(self, context: C, elements: typing.Iterable[E]) -> int:
        state = 0
        for element in elements:
            state = self._on(state, context, element)
        state = self._on(state, context, self.eot())
        return state
