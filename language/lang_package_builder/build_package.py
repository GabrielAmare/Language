import dataclasses
import os

import graphviz

from utils.graphs import DirectedGraph
from utils.graphs.graphviz import GraphvizDotBuilder
from .build_graph import ClassManagerGraph
from .case_converting import pascal_case_to_snake_case
from .casters import Caster
from .classes import ClassManager, TokenClass, LemmaClass, GroupClass
from .dependencies.bnf import Engine
from .dependencies.python import Environment, Package
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


def build_mro_dot(manager: ClassManager) -> graphviz.Digraph:
    dot = graphviz.Digraph()
    
    graph = manager.mro_graph
    
    def sort_nodes(name: str):
        definition = manager.classes.get(name)
        if isinstance(definition, TokenClass):
            if manager.is_private_constant_token(name):
                index = 0
            else:
                index = 1
        elif isinstance(definition, LemmaClass):
            index = 2
        elif isinstance(definition, GroupClass):
            index = 3
        else:
            index = 4
        
        return (
            # sort the classes by most generic.
            graph.get_origin_order(name),
            # sort the classes by type order (ConstantToken -> VariableToken -> Lemma -> Group -> External)
            index,
            # sort the classes by alphabetical order.
            name,
        )
    
    for origin in sorted(graph, key=sort_nodes):
        cls = manager.classes.get(origin)
        label = origin
        if isinstance(cls, GroupClass):
            fillcolor = "orange"
        elif isinstance(cls, LemmaClass):
            fillcolor = "lightblue"
        elif isinstance(cls, TokenClass):
            if manager.is_private_constant_token(origin):
                fillcolor = "#844de3"
                label = pascal_case_to_snake_case(origin).upper().lstrip('_')
            else:
                fillcolor = "lime"
        else:
            fillcolor = "gray"
        
        dot.node(
            name=origin,
            label=label,
            shape="rect",
            style="filled",
            fillcolor=fillcolor
        )
        
        for target in sorted(graph.targets(origin), key=sort_nodes):
            dot.edge(
                tail_name=origin,
                head_name=target,
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
    
    def build(self, grammar: Engine, root: str = os.curdir):
        class_manager = ClassManager.from_grammar(grammar)
        class_manager.apply_casters(self.casters)
        class_manager.simplify_common_signatures()
        
        with Package(name=self.name, env=self.python_env) as package:
            if self.build_models:
                build_models(package, class_manager)
            
            if self.build_visitors:
                build_visitors(package, class_manager, self.build_visitors)
            
            package.save(root=root)
        
        if self.build_grammar_file:
            src = str(grammar)
            with open(f"{root}/{self.name}/grammar.bnf", mode="w", encoding="utf-8") as file:
                file.write(src)
        
        ClassManagerGraph(class_manager).build_dot().save(f'{root}/{self.name}/graph.gv')
        
        build_use_dot = CustomGraphvizDotBuilder(class_manager).build
        
        if self.build_mro_graph:
            mro_dot = build_mro_dot(class_manager)
            mro_dot.save(f'{root}/{self.name}/mro_graph.gv')
        
        if self.build_use_graph:
            use_dot = build_use_dot(class_manager.use_graph)
            use_dot.save(f'{root}/{self.name}/use_graph.gv')
