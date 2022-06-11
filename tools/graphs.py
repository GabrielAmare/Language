from __future__ import annotations

import abc
import dataclasses
import typing

from tools import queries

__all__ = [
    'Node',
    'Link',
    'Graph'
]


@dataclasses.dataclass
class Node:
    graph: Graph = dataclasses.field(repr=False)

    def _is_origin_of(self, link: Link) -> bool:
        return self is link.origin

    def _is_target_of(self, link: Link) -> bool:
        return self is link.target

    @property
    def origin_links(self) -> queries.Query[Link]:
        return self.graph.links.filter(self._is_target_of)

    @property
    def target_links(self) -> queries.Query[Link]:
        return self.graph.links.filter(self._is_origin_of)

    @property
    def origins(self) -> queries.Query[Node]:
        return self.origin_links.getattr('origin')

    @property
    def targets(self) -> queries.Query[Node]:
        return self.target_links.getattr('target')

    @property
    def origin_order(self) -> int:
        return max(self.origins.getattr('origin_order'), default=-1) + 1

    @property
    def target_order(self) -> int:
        return max(self.targets.getattr('target_order'), default=-1) + 1

    @property
    def all_origins(self) -> typing.List[Node]:
        result = []

        for origin in self.origins:
            if origin not in result:
                result.append(origin)
                for sub_origin in origin.all_origins:
                    if sub_origin not in result:
                        result.append(sub_origin)

        return result

    @property
    def all_targets(self) -> typing.List[Node]:
        result = []

        for target in self.targets:
            if target not in result:
                result.append(target)
                for sub_target in target.all_targets:
                    if sub_target not in result:
                        result.append(sub_target)

        return result


@dataclasses.dataclass
class Link:
    graph: Graph = dataclasses.field(repr=False)
    origin: Node
    target: Node


N = typing.TypeVar('N', bound=Node)
L = typing.TypeVar('L', bound=Link)


@dataclasses.dataclass
class Graph(typing.Generic[N, L], abc.ABC):
    nodes: queries.QueryList[N] = dataclasses.field(default_factory=queries.QueryList)
    links: queries.QueryList[L] = dataclasses.field(default_factory=queries.QueryList)

    @abc.abstractmethod
    def _new_node(self, **kwargs) -> N:
        """Create a new `Node`."""

    def _has_node(self, node: N) -> bool:
        return node in self.nodes

    def _add_node(self, node: N) -> None:
        assert not self._has_node(node)
        self.nodes.append(node)

    def node(self, **kwargs) -> N:
        node = self._new_node(**kwargs)
        self._add_node(node)
        return node

    @abc.abstractmethod
    def _new_link(self, origin: N, target: N, **kwargs) -> L:
        """Create a new `Link`."""

    def _has_link(self, link: L) -> bool:
        return link in self.links

    def _add_link(self, link: L) -> None:
        assert not self._has_link(link)
        self.links.append(link)

    def link(self, origin: N, target: N, **kwargs) -> Link:
        link = self._new_link(origin, target, **kwargs)
        self._add_link(link)
        return link
