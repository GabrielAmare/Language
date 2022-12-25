import dataclasses
import os

import graphviz

from utils.graphs import DirectedGraph
from utils.graphs.graphviz import GraphvizDotBuilder
from .casters import Caster
from .classes import ClassManager, TokenClass, LemmaClass, GroupClass, MroGraph
from .dependencies.bnf import Engine
from .dependencies.python import Environment, DynamicPackage
from .factories import build_models, build_visitors

__all__ = [
    'LangPackageBuilder'
]


@dataclasses.dataclass
class CustomGraphvizDotBuilder(GraphvizDotBuilder):
    manager: ClassManager
    
    def _node_style(self, _graph: DirectedGraph, node: str):
        return dict(
            label=node,
            shape="rect",
            style="filled",
            fillcolor={
                GroupClass: "orange",
                LemmaClass: "lightblue",
                TokenClass: "lime"
            }.get(type(self.manager.classes.get(node)), "gray")
        )


@dataclasses.dataclass
class MroGraphvizBuilder(GraphvizDotBuilder):
    manager: ClassManager
    
    def _node_style(self, _graph: MroGraph, node: str):
        return dict(
            label=node,
            shape="rect",
            style="filled",
            fillcolor={
                GroupClass: "orange",
                LemmaClass: "lightblue",
                TokenClass: "lime"
            }.get(type(self.manager.classes.get(node)), "gray")
        )
    
    def build(self, graph: MroGraph) -> graphviz.Digraph:
        """Custom build method to render the graph in an deterministic way."""
        dot = graphviz.Digraph()
        
        def sort_nodes(name: str):
            class_type = self.manager.classes.get(name).__class__
            return (
                # sort the classes by most generic.
                graph.get_origin_order(name),
                # sort the classes by type order (Token -> Lemma -> Group)
                [TokenClass, LemmaClass, GroupClass, ].index(class_type),
                # sort the classes by alphabetical order.
                name,
            )
        
        graph.nodes.sort(key=sort_nodes)
        
        for node in graph.nodes:
            dot.node(
                name=self._node_name(graph, node),
                **self._node_style(graph, node)
            )
        
        for origin in graph.nodes:
            # create the links in the order of the nodes
            for target in sorted(graph.direct_subclasses(origin), key=sort_nodes):
                dot.edge(
                    tail_name=self._node_name(graph, origin),
                    head_name=self._node_name(graph, target),
                    **self._link_style(graph, origin, target)
                )
        
        return dot


@dataclasses.dataclass
class LangPackageBuilder:
    name: str
    build_grammar_file: bool = True
    build_mro_graph: bool = True
    build_use_graph: bool = True
    build_models: bool = True
    build_visitors: list[str] | None = None
    python_env: Environment = Environment.default((3, 10, 0))
    casters: dict[str, Caster] = dataclasses.field(default_factory=dict)
    
    def build(self, grammar: Engine):
        if os.path.exists(self.name):
            if not os.path.isdir(self.name):
                raise NotADirectoryError(self.name)
        else:
            os.mkdir(self.name)
        
        class_manager = ClassManager.from_grammar(grammar)
        
        class_manager.apply_casters(self.casters)
        
        class_manager.simplify_common_signatures()
        
        if self.build_grammar_file:
            src = str(grammar)
            with open(f"{self.name}/grammar.bnf", mode="w", encoding="utf-8") as file:
                file.write(src)
        
        build_mro_dot = MroGraphvizBuilder(class_manager).build
        build_use_dot = CustomGraphvizDotBuilder(class_manager).build
        
        if self.build_mro_graph:
            mro_dot = build_mro_dot(class_manager.mro_graph)
            mro_dot.save(f'{self.name}/mro_graph.gv')
        
        if self.build_use_graph:
            use_dot = build_use_dot(class_manager.use_graph)
            use_dot.save(f'{self.name}/use_graph.gv')
        
        package = DynamicPackage(name=self.name, env=self.python_env)
        
        if self.build_models:
            build_models(package, class_manager)
        
        if self.build_visitors:
            build_visitors(package, class_manager, self.build_visitors)
        
        package.save()
