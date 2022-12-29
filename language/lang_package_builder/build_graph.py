from __future__ import annotations

import dataclasses
import functools

import graphviz

from utils.graphs_v2 import Graph
from .case_converting import pascal_case_to_snake_case
from .classes import ClassManager, TokenClass, LemmaClass, GroupClass, BaseClass

__all__ = [
    'ClassManagerGraph',
]


@dataclasses.dataclass
class ClassManagerGraph:
    manager: ClassManager
    graph: Graph = dataclasses.field(default_factory=Graph)
    build_use_links: bool = False
    show_type_hints: bool = True
    
    def _make_node_label(self, name: str) -> str:
        if self.show_type_hints:
            ns = ' '.join(
                "| <%s> %s: %s" % (attr.name, attr.name, ' | '.join(sorted(set(map(self._get_true_type, attr.types)))))
                for attr in self.manager.classes.get(name).namespace.attrs
            )
        else:
            ns = ' '.join(
                "| <%s> %s " % (attr.name, attr.name)
                for attr in self.manager.classes.get(name).namespace.attrs
            )
        
        return "{ <> %s %s }" % (name, ns)
    
    def _is_casted(self, name: str) -> bool:
        ref = self.manager.classes.get(name)
        return isinstance(ref, TokenClass) and ref.caster is not None
    
    def _get_true_type(self, name: str):
        # Doesn't plot the casted classes
        ref = self.manager.classes.get(name)
        if isinstance(ref, TokenClass) and ref.caster is not None:
            return ref.caster.name
        else:
            return name
    
    @functools.cached_property
    def classes(self) -> list[BaseClass]:
        return [
            cls
            for cls in self.manager.classes.values()
            if not self._is_casted(cls.name)
        ]
    
    def _create_nodes(self) -> None:
        # Create the nodes for the classes
        for cls in self.classes:
            node_id = cls.name
            if not self.graph.has_node(node_id):
                if isinstance(cls, TokenClass):
                    if self.manager.is_private_constant_token(cls.name):
                        order = 0
                        style = {
                            'label': pascal_case_to_snake_case(cls.name).upper().lstrip('_'),
                            'shape': "rect",
                            'style': "filled",
                            'fillcolor': "#844de3",
                        }
                    else:
                        order = 1
                        style = {
                            'label': self._make_node_label(cls.name),
                            'shape': "record",
                            'style': "filled",
                            'fillcolor': "lime",
                        }
                elif isinstance(cls, LemmaClass):
                    order = 2
                    style = {
                        'label': self._make_node_label(cls.name),
                        'shape': "record",
                        'style': "filled",
                        'fillcolor': "lightblue",
                    }
                elif isinstance(cls, GroupClass):
                    order = 3
                    style = {
                        'label': self._make_node_label(cls.name),
                        'shape': "record",
                        'style': "filled",
                        'fillcolor': "orange",
                    }
                else:
                    raise NotImplementedError
                
                self.graph.add_node(node_id, {'order': order, 'style': style})
    
    def _create_mro_links(self):
        # Create the mro links between classes
        for cls in self.classes:
            if not isinstance(cls, GroupClass):
                continue
            
            for sub_cls in cls.rule.refs:
                if self._is_casted(sub_cls):
                    continue
                
                if not self.graph.has_link(cls.name, 'is_super_of', sub_cls):
                    style = {
                        'arrowtail': 'diamond',
                        'color': 'darkorange',
                        'dir': 'back',
                    }
                    self.graph.add_link(cls.name, 'is_super_of', sub_cls, {'style': style})
    
    def _create_use_links(self):
        # Create the use links between classes
        for cls in self.classes:
            for attr in cls.namespace.attrs:
                for used_cls in attr.types:
                    # Doesn't plot the casted classes
                    used_cls = self._get_true_type(used_cls)
                    
                    if not self.graph.has_node(used_cls):
                        style = {
                            'label': used_cls,
                            'shape': "rect",
                            'style': "filled",
                            'fillcolor': "gray",
                        }
                        
                        self.graph.add_node(used_cls, {'order': 5, 'style': style})
                    
                    link_type = f'uses:{attr.name}'
                    if not self.graph.has_link(cls.name, link_type, used_cls):
                        style = {
                            'color': 'blue',
                        }
                        if attr.optional:
                            if attr.multiple:
                                style['arrowhead'] = 'oinv'
                            else:
                                style['arrowhead'] = 'onormal'
                        else:
                            if attr.multiple:
                                style['arrowhead'] = 'inv'
                            else:
                                style['arrowhead'] = 'normal'
                        
                        self.graph.add_link(cls.name, link_type, used_cls, {'style': style})
    
    def sort_nodes(self, node_id: str):
        return (
            # sort the classes by most generic.
            self.graph.get_origin_order('is_super_of', node_id),
            # sort the classes by type order (ConstantToken -> VariableToken -> Lemma -> Group)
            self.graph.get_node(node_id)['order'],
            # sort the classes by alphabetical order.
            node_id,
        )
    
    def build_dot(self) -> graphviz.Digraph:
        self._create_nodes()
        self._create_mro_links()
        if self.build_use_links:
            self._create_use_links()
        
        dot = graphviz.Digraph()
        nodes = self.graph.get_sorted_nodes(key=self.sort_nodes)
        
        for node_id in nodes:
            dot.node(name=node_id, **self.graph.get_node(node_id)['style'])
        
        for origin_id in nodes:
            # create the links in the order of the nodes
            sorted_links = sorted(self.graph.target_links(origin_id),
                                  key=lambda item: (item[0], self.sort_nodes(item[1])))
            for link_type, target_id in sorted_links:
                link = self.graph.get_link(origin_id, link_type, target_id)
                
                if link_type.startswith('uses'):
                    origin = origin_id + link_type[4:]
                else:
                    origin = origin_id
                
                dot.edge(
                    tail_name=origin,
                    head_name=target_id,
                    **link['style']
                )
        
        return dot
