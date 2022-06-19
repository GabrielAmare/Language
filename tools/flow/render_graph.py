import abc
import dataclasses
import functools
import string
import typing

import graphviz

from . import tokenizer as t
from .base import *

start_state_id: str = "⚪"
valid_state_id: str = "✓"
error_state_id: str = "✗"

F = typing.TypeVar('F', bound=Flow)


@dataclasses.dataclass
class FlowGraph(typing.Generic[F], abc.ABC):
    flow: F
    state_nodes: dict[int, str] = dataclasses.field(default_factory=dict)
    condition_nodes: dict[int, str] = dataclasses.field(default_factory=dict)
    action_nodes: dict[int, str] = dataclasses.field(default_factory=dict)
    
    handlers: list[Handler] = dataclasses.field(default_factory=list)
    actions: list[Action] = dataclasses.field(default_factory=list)
    edges: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    
    @functools.cached_property
    def dot(self) -> graphviz.Digraph:
        dot = graphviz.Digraph(
            name="Flow - example",
            comment="Representation of the flow",
            filename="flow-graph.gv",
            format="svg",
        )
        dot.graph_attr['rankdir'] = 'LR'
        return dot
    
    def state_label(self, state: int) -> str:
        if state == 0:
            return start_state_id
        elif state == -1:
            return valid_state_id
        elif state == -2:
            return error_state_id
        else:
            return str(state)
    
    def state_id(self, state: int) -> str:
        return f"s-{self.state_label(state)}"
    
    def action_id(self, action_index: int) -> str:
        return f"a-{action_index}"
    
    def condition_id(self, handler_index: int) -> str:
        return f"c-{handler_index}"
    
    @abc.abstractmethod
    def action_label(self, action: Action) -> str:
        """"""
    
    @abc.abstractmethod
    def condition_label(self, condition: Condition) -> str:
        """"""
    
    def state_node(self, state: int) -> str:
        if state not in self.state_nodes:
            node_id = self.state_id(state)
            self.state_nodes[state] = node_id
            if state == -1:
                color = "#00FF00"
            elif state == -2:
                color = "#FF0000"
            else:
                color = "#FFFFFF"
            
            self.dot.node(
                name=node_id,
                label=self.state_label(state),
                shape="circle",
                style="filled",
                fillcolor=color
            )
        
        return self.state_nodes[state]
    
    def condition_node(self, handler_index: int, condition: Condition) -> str:
        if handler_index not in self.condition_nodes:
            self.condition_nodes[handler_index] = node_id = self.condition_id(handler_index)
            self.dot.node(
                name=node_id,
                label=self.condition_label(condition),
                shape="hexagon",
                style="filled",
                fillcolor="#FFAA00"
            )
        return self.condition_nodes[handler_index]
    
    def action_node(self, action_index: int, action: Action) -> str:
        if action_index not in self.action_nodes:
            self.action_nodes[action_index] = node_id = self.action_id(action_index)
            self.dot.node(
                name=node_id,
                label=self.action_label(action),
                shape="box",
                style="filled",
                fillcolor="#00AAFF"
            )
        
        return self.action_nodes[action_index]
    
    def get_handler_index(self, handler: Handler) -> int:
        try:
            return self.handlers.index(handler)
        except ValueError:
            index = len(self.handlers)
            self.handlers.append(handler)
            return index
    
    def get_action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError:
            index = len(self.actions)
            self.actions.append(action)
            return index
    
    def link(self, *node_ids):
        for origin, target in zip(node_ids, node_ids[1:]):
            key = origin, target
            if key not in self.edges:
                self.edges.append(key)
                self.dot.edge(origin, target)
    
    def build(self) -> None:
        for state, manager in self.flow.managers.items():
            state_id = self.state_node(state)
            
            for handler in manager.handlers:
                handler_index = self.get_handler_index(handler)
                condition_id = self.condition_node(handler_index, handler.condition)
                
                action = self.flow.actions[handler.action]
                action_index = self.get_action_index(action)
                action_id = self.action_node(action_index, action)
                self.link(state_id, condition_id, action_id)
            
            if manager.default is not None:
                action = self.flow.actions[manager.default]
                action_index = self.get_action_index(action)
                action_id = self.action_node(action_index, action)
                self.link(state_id, action_id)
        
        for action in self.flow.actions:
            action_index = self.get_action_index(action)
            action_id = self.action_node(action_index, action)
            state_id = self.state_node(action.to)
            self.link(action_id, state_id)
    
    def render(self) -> None:
        self.build()
        self.dot.render('flow-graph', view=True)
        for handler in self.handlers:
            print('--', handler)


@dataclasses.dataclass
class TokenizerGraph(FlowGraph[t.Flow]):
    def action_label(self, action: t.Action) -> str:
        label = str(action)
        label = label.split(' -> ')[0]
        label = label.replace('add() & inc() & clr()', 'include()')
        label = '\n'.join(label.split(' & '))
        return label
    
    def condition_label(self, condition: t.Condition) -> str:
        label = str(condition)
        label = label.replace(string.ascii_lowercase, 'a-z')  # simplify lowercase letters
        label = label.replace(string.ascii_uppercase, 'A-Z')  # simplify uppercase letters
        label = label.replace(string.digits, '0-9')  # simplify digits
        label = label.replace('<', '\\<').replace('>', '\\>')  # escape '<' and '>'
        label = label[1:-1]
        label = label.replace("\\x00", "⚡")  # display EOT
        label = label.replace(' ', '␣')  # display space
        return label
