import dataclasses
import typing

from .DirectedGraph import DirectedGraph

__all__ = [
    'AcyclicDirectedGraph',
]

T = typing.TypeVar('T', bound=typing.Hashable)


@dataclasses.dataclass
class AcyclicDirectedGraph(typing.Generic[T], DirectedGraph[T]):
    def add_link(self, origin: T, target: T):
        assert origin not in self.get_all_targets(target), "no loop allowed in an acyclic directed graph."
        assert target not in self.get_all_origins(origin), "no loop allowed in an acyclic directed graph."
        super().add_link(origin, target)
    
    def get_all_targets(self, node: T) -> set[T]:
        all_targets: set[T] = set()
        queue: list[T] = [node]
        
        while queue:
            origin: T = queue.pop(0)
            for target in self.get_targets(origin):
                if target not in all_targets and target not in queue:
                    all_targets.add(target)
                    queue.append(target)
        
        return all_targets
    
    def get_all_origins(self, node: T) -> set[T]:
        all_origins: set[T] = set()
        queue: list[T] = [node]
        
        while queue:
            target: T = queue.pop(0)
            for origin in self.get_origins(target):
                if origin not in all_origins and origin not in queue:
                    all_origins.add(origin)
                    queue.append(origin)
        
        return all_origins
    
    def get_origin_order(self, node: T) -> int:
        return max(map(self.get_origin_order, self.get_origins(node)), default=-1) + 1
    
    def get_target_order(self, node: T) -> int:
        return max(map(self.get_target_order, self.get_targets(node)), default=-1) + 1
    
    @property
    def origin_roots(self) -> list[T]:
        """Return all the nodes that have no origins."""
        return [node for node in self.nodes if self.get_origin_order(node) == 0]
    
    @property
    def target_roots(self) -> list[T]:
        """Return all the nodes that have no targets."""
        return [node for node in self.nodes if self.get_target_order(node) == 0]
