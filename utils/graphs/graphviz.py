import abc
import typing

import graphviz

from .DirectedGraph import DirectedGraph

__all__ = [
    'AbstractGraphvizDotBuilder',
    'GraphvizDotBuilder',
]

_T = typing.TypeVar('_T')


class AbstractGraphvizDotBuilder(typing.Generic[_T]):
    @abc.abstractmethod
    def _node_name(self, graph: DirectedGraph[_T], node: _T) -> str:
        pass
    
    @abc.abstractmethod
    def _node_style(self, graph: DirectedGraph[_T], node: _T) -> dict:
        pass
    
    @abc.abstractmethod
    def _link_style(self, graph: DirectedGraph[_T], origin: _T, target: _T) -> dict:
        pass
    
    def build(self, graph: DirectedGraph[_T]) -> graphviz.Digraph:
        dot = graphviz.Digraph()
        
        for node in graph.nodes:
            dot.node(
                name=self._node_name(graph, node),
                **self._node_style(graph, node)
            )
        
        for origin, targets in graph.links_by_origin.items():
            for target in targets:
                dot.edge(
                    tail_name=self._node_name(graph, origin),
                    head_name=self._node_name(graph, target),
                    **self._link_style(graph, origin, target)
                )
        
        return dot


class GraphvizDotBuilder(typing.Generic[_T], AbstractGraphvizDotBuilder[_T]):
    def _node_name(self, graph: DirectedGraph[_T], node: _T) -> str:
        return str(graph.nodes.index(node))
    
    def _node_style(self, graph: DirectedGraph[_T], node: _T) -> dict:
        return dict(label=str(node))
    
    def _link_style(self, graph: DirectedGraph[_T], origin: _T, target: _T) -> dict:
        return dict()
