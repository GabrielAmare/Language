from __future__ import annotations

import dataclasses
import functools

from base.models import Descriptor, get_shared_descriptor
from tools import queries, graphs, console
from .base import *

__all__ = [
    'Node',
    'Link',
    'Graph'
]


@dataclasses.dataclass
class Node(graphs.Node):
    toplevel: TopLevel
    descriptor: Descriptor
    optimized: Descriptor

    @property
    def type(self) -> Variable:
        return self.toplevel.type

    @property
    def bases(self) -> list[Variable]:
        return self.origins.getattr('type').as_list()

    def is_direct_super_of(self, other: Node) -> bool:
        """Return True when `self.toplevel` defines a direct super-class of `other.toplevel`."""
        return isinstance(self.toplevel, Group) and other.toplevel.type in self.toplevel.types

    def order(self) -> tuple[int, Variable]:
        return self.origin_order, self.type


Link = graphs.Link


@dataclasses.dataclass
class Graph(graphs.Graph[Node, Link]):
    reader: Reader = None

    def _new_node(self, toplevel: TopLevel, descriptor: Descriptor, **__) -> Node:
        return Node(graph=self, toplevel=toplevel, descriptor=descriptor, optimized=descriptor)

    def _new_link(self, origin: Node, target: Node, **__) -> Link:
        return Link(graph=self, origin=origin, target=target)

    def node(self, toplevel: TopLevel, descriptor: Descriptor) -> Node:
        return super().node(toplevel=toplevel, descriptor=descriptor)

    def optimize(self):
        for origin in sorted(self.nodes, key=lambda node: node.target_order):
            targets = origin.targets

            common = get_shared_descriptor(targets.getattr('optimized'))

            for target in targets:
                target.optimized = target.optimized / common

            origin.optimized = origin.optimized & common

    @functools.cached_property
    def root_classes(self) -> queries.Query[Variable]:
        """Return all the classes defined with no super class."""
        return (self.nodes
                .filter(queries.Item.getattr('origin_order').equals(0))
                .getattr("toplevel")
                .getattr("type")
                .as_set())

    @classmethod
    def from_reader(cls, reader: Reader) -> Graph:
        """Build the `Graph` associated with the given `reader`."""
        reader = reader.simplify_aliases  # remove `Alias` objects from the `reader`.
        self = cls(reader=reader)

        for used in reader.get_uses():
            toplevel = reader.get(used)
            self.node(
                toplevel=toplevel,
                descriptor=toplevel.descriptor
            )

        for origin in self.nodes:
            for target in self.nodes:
                if origin.is_direct_super_of(target):
                    self.link(origin, target)

        self.optimize()

        return self

    def debug(self) -> None:
        """
            Warns if types are defined more than once.
            Warns if types are not used.
        """
        def_count = self.reader.def_count
        use_count = self.reader.use_count
        keys = sorted({*def_count.keys(), *use_count.keys()}, key=str)

        for key in keys:
            n_use = use_count.get(key, 0)
            n_def = def_count.get(key, 0)
            if n_use > 0 and n_def == 0:
                console.warning(f"The type `{key!s}` is used {n_use!r} times, but not defined !")

            if n_def > 1:
                console.warning(f"The type `{key!s}` is defined {n_def!r} times !")

        root_classes = set(self.root_classes)
        if len(root_classes) > 1:
            console.warning(f"There are multiple root classes : {', '.join(map(str, root_classes))}")

        for node in self.nodes:
            if node.origin_order == 0:
                if isinstance(node.toplevel, (Branch, PatternGR)):
                    console.warning(f"{str(node.toplevel.type)!r} should have a super class.")
