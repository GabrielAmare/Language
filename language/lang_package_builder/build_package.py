import dataclasses
import os

from language.base.bnf.v0_0_1 import Engine
from language.base.python.v3_10_0 import Environment, DynamicPackage
from utils.graphs import DirectedGraph
from utils.graphs.graphviz import GraphvizDotBuilder
from .classes import ClassManager, TokenClass, LemmaClass, GroupClass
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
class LangPackageBuilder:
    name: str
    build_grammar_file: bool = True
    build_mro_graph: bool = True
    build_use_graph: bool = True
    build_models: bool = True
    build_visitors: list[str] | None = None
    python_env: Environment = Environment.default((3, 10, 0))
    
    def build(self, grammar: Engine):
        if os.path.exists(self.name):
            if not os.path.isdir(self.name):
                raise NotADirectoryError(self.name)
        else:
            os.mkdir(self.name)
        
        class_manager = ClassManager.from_grammar(grammar)
        
        if self.build_grammar_file:
            src = str(grammar)
            with open(f"{self.name}/grammar.bnf", mode="w", encoding="utf-8") as file:
                file.write(src)
        
        get_dot = CustomGraphvizDotBuilder(class_manager).build
        
        if self.build_mro_graph:
            mro_dot = get_dot(class_manager.mro_graph)
            mro_dot.save(f'{self.name}/mro_graph.gv')
        
        if self.build_use_graph:
            use_dot = get_dot(class_manager.use_graph)
            use_dot.save(f'{self.name}/use_graph.gv')
        
        package = DynamicPackage(name=self.name, env=self.python_env)
        
        if self.build_models:
            build_models(package, class_manager)
        
        if self.build_visitors:
            build_visitors(package, class_manager, self.build_visitors)
        
        package.save()
