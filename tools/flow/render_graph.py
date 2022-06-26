import abc
import dataclasses
import functools
import string
import typing

import graphviz

from . import tokenizer as t
from .base import *

F = typing.TypeVar('F', bound=Flow)


@dataclasses.dataclass
class Node(abc.ABC):
    name: str
    
    @property
    @abc.abstractmethod
    def _config(self) -> dict:
        """"""
    
    @property
    def config(self) -> dict:
        return dict(name=self.name, **self._config)


@dataclasses.dataclass
class ActionNode(Node):
    label: str
    
    @property
    def _config(self) -> dict:
        return dict(
            label=self.label,
            shape="box",
            style="filled",
            width="0",
            fillcolor="#6d47ec"
        )


@dataclasses.dataclass
class ConditionNode(Node):
    label: str
    
    @property
    def _config(self) -> dict:
        return dict(
            label=self.label,
            shape="hexagon",
            style="filled",
            width="0",
            fillcolor="#cda219"
        )


@dataclasses.dataclass
class StateNode(Node):
    state: int
    
    @property
    def label(self) -> str:
        if self.state == 0:
            return "⚪"
        elif self.state == -1:
            return "✓"
        elif self.state == -2:
            return "✗"
        else:
            return str(self.state)
    
    @property
    def color(self) -> str:
        if self.state == -1:
            return "#00FF00"
        elif self.state == -2:
            return "#FF0000"
        elif self.state == 0:
            return "#d6e613"
        else:
            return "#FFFFFF"
    
    @property
    def _config(self) -> dict:
        if self.state == 0:
            return dict(
                label="",
                shape="circle",
                width="0.2",
                fontsize="10pt",
                style="filled",
                fillcolor=self.color
            )
        else:
            return dict(
                label=self.label,
                shape="circle",
                style="filled",
                width="0",
                height="0",
                fontsize="10pt",
                fillcolor=self.color
            )


@dataclasses.dataclass
class FlowGraph(typing.Generic[F], abc.ABC):
    name: str
    flow: F
    state_nodes: dict[str, StateNode] = dataclasses.field(default_factory=dict)
    
    handlers: list[Handler] = dataclasses.field(default_factory=list)
    actions: list[Action] = dataclasses.field(default_factory=list)
    edges: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    
    @functools.cached_property
    def dot(self) -> graphviz.Digraph:
        dot = graphviz.Digraph(
            name="Flow - example",
            comment="Representation of the flow",
            filename=f"{self.name}.gv",
            format="svg",
            graph_attr=dict(
                splines="compound",
                bgcolor="#151515"
            ),
            edge_attr=dict(
                arrowhead="onormal",
                color="#e3ddcd"
            ),
            node_attr=dict(
                color="#504f4c"
            )
        )
        dot.graph_attr['rankdir'] = 'LR'
        return dot
    
    end: int = 0
    
    @abc.abstractmethod
    def action_labels(self, action: Action) -> list[str]:
        """"""
    
    @abc.abstractmethod
    def condition_label(self, condition: Condition) -> str:
        """"""
    
    nodes: list[str] = dataclasses.field(default_factory=list)
    
    def create(self, node: Node, target: Node) -> Node:
        node.name = f"{node.name}-{target.name}"
        
        if node.name not in self.nodes:
            self.nodes.append(node.name)
            self.dot.node(**node.config)
            self.link(node.name, target.name)
        
        return node
    
    def chain(self, origin: Node, nodes: list[Node], target: Node):
        for node in reversed(nodes):
            target = self.create(node, target)
        
        self.link(origin.name, target.name)
    
    def state_id(self, state: int, end: bool) -> str:
        if state == 0 and end:
            self.end += 1
            return f"s-{str(state)}-end-{self.end}"
        else:
            return f"s-{str(state)}"
    
    def state_node(self, state: int, end: bool) -> StateNode:
        node_id = self.state_id(state, end)
        if node_id not in self.state_nodes:
            node = StateNode(
                name=node_id,
                state=state
            )
            self.state_nodes[node_id] = node
            self.dot.node(**node.config)
        
        return self.state_nodes[node_id]
    
    def link(self, origin, target):
        if (origin, target) not in self.edges:
            self.edges.append((origin, target))
            self.dot.edge(origin, target)
    
    def condition_node(self, condition: Condition) -> ConditionNode:
        return ConditionNode(
            name=hex(hash(condition))[2:],
            label=self.condition_label(condition)
        )
    
    def action_nodes(self, action: Action) -> list[ActionNode]:
        return [ActionNode(
            name=hex(hash(label))[2:],
            label=label
        ) for label in self.action_labels(action)]
    
    def build(self) -> None:
        for state, manager in self.flow.managers.items():
            origin = self.state_node(state, end=False)
            
            for handler in manager.handlers:
                action = self.flow.actions[handler.action]
                condition_node = self.condition_node(handler.condition)
                action_nodes = self.action_nodes(action)
                self.chain(origin=origin, nodes=[condition_node, *action_nodes],
                           target=self.state_node(action.to, end=True))
            
            if manager.default is not None:
                action = self.flow.actions[manager.default]
                action_nodes = self.action_nodes(action)
                self.chain(origin=origin, nodes=[*action_nodes], target=self.state_node(action.to, end=True))
    
    def render(self) -> None:
        self.build()
        self.dot.render(filename=self.name + ".gv", outfile=self.name + ".svg", view=True)
        for handler in self.handlers:
            print('--', handler)
    
    def save(self, fp: str) -> None:
        self.build()
        self.dot.render(outfile=fp, view=False)


@dataclasses.dataclass
class TokenizerGraph(FlowGraph[t.Flow]):
    def action_labels(self, action: t.Action) -> list[str]:
        label = str(action)
        label = label.split(' -> ')[0]
        label = label.replace('add() & inc() & clr()', 'include()')
        label = label.replace('include()', '∈')
        label = label.replace('clear()', 'Ø')
        # label = '\n'.join()
        return [label for label in label.split(' & ') if label]
    
    def condition_label(self, condition: t.Condition) -> str:
        label = str(condition)
        label = label.replace(string.ascii_lowercase, 'a-z')  # simplify lowercase letters
        label = label.replace(string.ascii_uppercase, 'A-Z')  # simplify uppercase letters
        label = label.replace(string.digits, '0-9')  # simplify digits
        label = label.replace('<', '\\<').replace('>', '\\>')  # escape '<' and '>'
        label = label[1:-1]
        label = label.replace("\\x00", "⚡")  # display EOT
        label = label.replace(' ', '␣')  # display space
        label = label.replace('\\n', '\\\\n')
        return label
