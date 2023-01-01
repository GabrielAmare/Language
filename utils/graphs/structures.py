from __future__ import annotations

import dataclasses
import functools
import typing

__all__ = [
    'DirectedGraph',
    'DirectedAcyclicGraph',
    'Tree',
    'List',
    'Set',
    'Ordering',
]

NODE = typing.TypeVar('NODE')


@dataclasses.dataclass
class DirectedGraph(typing.Mapping[NODE, set[NODE]]):
    _data: dict[NODE, set[NODE]] = dataclasses.field(default_factory=dict)
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, node: NODE) -> set[NODE]:
        return self._data[node]
    
    def __setitem__(self, origin: NODE, targets: set[NODE]):
        if origin not in self._data:
            self.add_node(origin)
        to_del = self._data[origin].difference(targets)
        to_add = targets.difference(self._data[origin])
        for target in to_del:
            self.del_link(origin, target)
        for target in to_add:
            self.add_link(origin, target)
    
    def __delitem__(self, node: NODE) -> None:
        self.del_node(node)
    
    def has_node(self, node: NODE) -> bool:
        return node in self._data
    
    def add_node(self, node: NODE) -> None:
        assert node not in self._data
        self._data[node] = set()
    
    def del_node(self, node: NODE) -> None:
        assert node in self._data
        del self._data[node]
        for targets in self._data.values():
            if node in targets:
                targets.remove(node)
    
    def has_link(self, origin: NODE, target: NODE) -> bool:
        return origin in self._data and target in self._data[origin]
    
    def add_link(self, origin: NODE, target: NODE) -> None:
        assert origin in self._data
        assert target not in self._data[origin]
        self._data[origin].add(target)
    
    def del_link(self, origin: NODE, target: NODE) -> None:
        assert origin in self._data
        assert target in self._data[origin]
        self._data[origin].remove(target)
    
    def targets(self, origin: NODE) -> set[NODE]:
        return self._data.get(origin, set())
    
    def origins(self, target: NODE) -> set[NODE]:
        return set(
            origin
            for origin, targets in self._data.items()
            if target in targets
        )
    
    def explore_from(self, origin: NODE):
        """Yields the nodes that can be reached from `origin`."""
        queue = [origin]
        index = 0
        while index < len(queue):
            node = queue[index]
            index += 1
            
            for target in self.targets(node):
                yield target
                
                if target not in queue:
                    queue.append(target)
    
    def can_reach(self, origin: NODE, target: NODE) -> bool:
        """Return True when it exists a path to link `origin` to `target`."""
        
        for node in self.explore_from(origin):
            if node == target:
                return True
        
        return False
    
    @classmethod
    def from_dict(cls, graph: typing.Mapping[NODE, typing.Iterable[NODE]]):
        self = cls()
        for origin, targets in graph.items():
            if not self.has_node(origin):
                self.add_node(origin)
            for target in targets:
                if not self.has_node(target):
                    self.add_node(target)
                if not self.has_link(origin, target):
                    self.add_link(origin, target)
        return self


@dataclasses.dataclass
class DirectedAcyclicGraph(DirectedGraph):
    def add_link(self, origin: NODE, target: NODE) -> None:
        if origin == target or self.can_reach(target, origin):
            raise Exception(f"No loop allowed in a {self.__class__.__name__} structure.")
        
        super().add_link(origin, target)


@dataclasses.dataclass
class Tree(DirectedAcyclicGraph):
    def add_link(self, origin: NODE, target: NODE) -> None:
        if self.origins(target):
            raise Exception(f"Cannot add more than 1 origin to a node in a {self.__class__.__name__} structure.")
        
        super().add_link(origin, target)


@dataclasses.dataclass
class List(Tree):
    def add_link(self, origin: NODE, target: NODE) -> None:
        if self.origins(target):
            raise Exception(f"Cannot add more than 1 origin to a node in a {self.__class__.__name__} structure.")

        if self.targets(origin):
            raise Exception(f"Cannot add more than 1 target to a node in a {self.__class__.__name__} structure.")
        
        super().add_link(origin, target)


@dataclasses.dataclass
class Set(List):
    def add_link(self, origin: NODE, target: NODE) -> None:
        raise Exception(f"Cannot add links in a {self.__class__.__name__} structure.")


@dataclasses.dataclass
class Ordering(typing.Generic[NODE]):
    graph: typing.Mapping[NODE, typing.Iterable[NODE]]
    """
    A class for computing an ordering of the nodes in a graph.

    Attributes:
        graph (dict[NODE, typing.Iterable[NODE]]): A dictionary representing the graph, where the keys are the nodes and the
        values are iterables of the nodes that each key node has edges to.
    """
    
    @functools.cached_property
    def clusters(self) -> set[frozenset[NODE]]:
        """
        Return the clusters defined in the graph.
        NOTE: We mean `cluster` as a cluster of nodes that can reach any other node of the cluster using the links.
        """
        groups: list[frozenset[NODE]] = [frozenset({node}) for node in self.graph]
        
        def include_subgroup(subgroup: frozenset[NODE]):
            index: int = 0
            while index < len(groups):
                cluster = groups[index]
                if cluster.intersection(subgroup):
                    subgroup = subgroup.union(cluster)
                    del groups[index]
                else:
                    index += 1
            
            groups.append(subgroup)
        
        for origin in self.graph:
            paths = [(origin,)]
            while paths:
                path = paths.pop(0)
                for target in self.graph.get(path[-1], []):
                    if target in path:
                        include_subgroup(frozenset(path[path.index(target):]))
                    else:
                        paths.append(path + (target,))
        
        return set(groups)
    
    @functools.cached_property
    def get_cluster_order(self) -> typing.Callable[[frozenset[NODE]], int]:
        @functools.lru_cache
        def function(cluster: frozenset[NODE]) -> int:
            """
            A function that returns the order of a cluster of nodes.

            Args:
                cluster (frozenset[NODE]): A frozenset representing a cluster of nodes in the graph.
            Returns:
                The order of the cluster of nodes.
            """
            
            return max(
                (
                    self.get_node_order(target)
                    for node in cluster
                    for target in self.graph.get(node, [])
                    if target not in cluster
                ),
                default=-1
            ) + 1
        
        return function
    
    @functools.cached_property
    def get_node_order(self) -> typing.Callable[[NODE], int]:
        @functools.lru_cache
        def function(node: NODE) -> int:
            """
            A function that returns the order of a node in the graph.

            Args:
                node (NODE): A node in the graph.
            Returns:
                The order of the node in the graph.
            """
            
            return self.get_cluster_order(self.get_node_cluster(node))
        
        return function
    
    @functools.cached_property
    def get_node_cluster(self) -> typing.Callable[[NODE], frozenset[NODE]]:
        @functools.lru_cache
        def function(node: NODE) -> frozenset[NODE]:
            """
            A function that returns the cluster that a node belongs to.

            Args:
                node (NODE): A node in the graph.
            Returns:
                A frozenset representing the cluster that the node belongs to.
            """
            
            for cluster in self.clusters:
                if node in cluster:
                    return cluster
            return frozenset({node})
        
        return function
