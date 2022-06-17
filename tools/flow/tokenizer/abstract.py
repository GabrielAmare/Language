import dataclasses

from .core import *

__all__ = [
    'AbstractProxy',
]


@dataclasses.dataclass
class AbstractProxy:
    flow: Flow
    state: int
    entry: int = 0
    
    @property
    def manager(self) -> Manager:
        return self.flow.managers[self.state]
    
    def _state(self, state: int | object) -> int:
        if state is STAY:
            return self.state
        elif state is ENTRY:
            return self.entry
        elif state is NEW:
            return self.flow.new_state()
        elif isinstance(state, int):
            return state
        elif isinstance(state, AbstractProxy):
            return state.state
        else:
            raise ValueError(f"unable to parse {state!r}.")
    
    def init(self):
        if self.state not in self.flow.managers:
            self.flow.managers[self.state] = Manager()
    
    def _action(self, params: ActionParams, to: int | object) -> Action:
        self.init()
        return Action(params=params, to=self._state(to))
