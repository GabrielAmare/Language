import abc
import dataclasses
import string

import graphviz

from . import tokenizer as t
from .base import *


@dataclasses.dataclass
class FlowGraph(abc.ABC):
    start_state_id: str = "⚪"
    valid_state_id: str = "✓"
    error_state_id: str = "✗"
    
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
            return self.start_state_id
        elif state == -1:
            return self.valid_state_id
        elif state == -2:
            return self.error_state_id
        else:
            return str(state)
    
    def state_id(self, state: int) -> str:
        return f"s-{self.state_label(state)}"
    
    def action_id(self, action_index: int) -> str:
        return f"a-{action_index}"
    
    def condition_id(self, state: int, handler_index: int) -> str:
        return f"c-{self.state_label(state)}-{handler_index}"
    
    @abc.abstractmethod
    def action_label(self, action: Action) -> str:
        """"""
    
    @abc.abstractmethod
    def condition_label(self, condition: Condition) -> str:
        """"""
    
    def state_node(self, dot: graphviz.Digraph, state: int) -> str:
        node_id = self.state_id(state)
        dot.node(
            name=node_id,
            label=self.state_label(state),
            shape="circle",
            style="filled",
            fillcolor="#FFFFFF"
        )
        return node_id
    
    def condition_node(self, dot: graphviz.Digraph, state: int, handler_index: int, condition: Condition) -> str:
        node_id = self.condition_id(state, handler_index)
        dot.node(
            name=node_id,
            label=self.condition_label(condition),
            shape="hexagon",
            style="filled",
            fillcolor="#FFAA00"
        )
        return node_id
    
    def action_node(self, dot: graphviz.Digraph, action_index: int, action: Action) -> str:
        node_id = self.action_id(action_index)
        dot.node(
            name=node_id,
            label=self.action_label(action),
            shape="box",
            style="filled",
            fillcolor="#00AAFF"
        )
        return node_id
    
    def build(self, flow: Flow) -> graphviz.Digraph:
        dot = self.dot()
        for state, manager in flow.managers.items():
            state_id = self.state_node(dot, state)
            
            for handler_index, handler in enumerate(manager.handlers):
                condition_id = self.condition_node(dot, state, handler_index, handler.condition)
                dot.edge(state_id, condition_id)
                
                action_id = self.action_id(handler.action)
                dot.edge(condition_id, action_id)
            
            if manager.default is not None:
                action_id = self.action_id(manager.default)
                dot.edge(state_id, action_id)
        
        for action_index, action in enumerate(flow.actions):
            action_id = self.action_node(dot, action_index, action)
            state_id = self.state_id(action.to)
            dot.edge(action_id, state_id)
        return dot
    
    def render(self, flow: Flow) -> None:
        dot = self.build(flow)
        
        dot.render('flow-graph', view=True)


@dataclasses.dataclass
class TokenizerGraph(FlowGraph):
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
