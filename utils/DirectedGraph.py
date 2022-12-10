import dataclasses
import typing

import graphviz

__all__ = [
    'DirectedGraph',
]

T = typing.TypeVar('T', bound=typing.Hashable)


@dataclasses.dataclass
class DirectedGraph(typing.Generic[T]):
    nodes: list[T] = dataclasses.field(default_factory=list)
    links_by_origin: dict[T, list[T]] = dataclasses.field(default_factory=dict)
    links_by_target: dict[T, list[T]] = dataclasses.field(default_factory=dict)
    
    def add_node(self, obj: T):
        if obj not in self.nodes:
            self.nodes.append(obj)
    
    def del_node(self, obj: T):
        if obj in self.nodes:
            self.nodes.remove(obj)
    
    def add_link(self, origin: T, target: T):
        self.add_node(origin)
        self.add_node(target)
        self.links_by_origin.setdefault(origin, [])
        if target not in self.links_by_origin[origin]:
            self.links_by_origin[origin].append(target)
        
        self.links_by_target.setdefault(target, [])
        if origin not in self.links_by_target[target]:
            self.links_by_target[target].append(origin)
    
    def del_link(self, origin: T, target: T):
        self.links_by_origin.setdefault(origin, [])
        if target in self.links_by_origin[origin]:
            self.links_by_origin[origin].remove(target)
        
        self.links_by_target.setdefault(target, [])
        if origin in self.links_by_target[target]:
            self.links_by_target[target].remove(origin)
    
    def get_targets(self, origin: T) -> list[T]:
        return self.links_by_origin.get(origin, [])
    
    def get_origins(self, target: T) -> list[T]:
        return self.links_by_target.get(target, [])
    
    def get_dot(self,
                node_config: typing.Callable[[T], dict],
                link_config: typing.Callable[[T, T], dict],
                ) -> graphviz.Digraph:
        dot = graphviz.Digraph()
        
        for node in self.nodes:
            dot.node(name=str(id(node)), **node_config(node))
        
        for origin, targets in self.links_by_origin.items():
            for target in targets:
                dot.edge(tail_name=str(id(origin)), head_name=str(id(target)), **link_config(origin, target))
        
        return dot
