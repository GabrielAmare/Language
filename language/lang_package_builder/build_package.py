import dataclasses
import os

from .build_graph import ClassManagerGraph
from .casters import Caster
from .classes import ClassManager
from .dependencies.bnf import Engine
from .dependencies.python import Environment, Package
from .factories import build_models, build_visitors
from .graphs import build_mro_dot, build_use_dot

__all__ = [
    'LangPackageBuilder'
]


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
        
        if self.build_mro_graph:
            mro_dot = build_mro_dot(class_manager)
            mro_dot.save(f'{root}/{self.name}/mro_graph.gv')
        
        if self.build_use_graph:
            use_dot = build_use_dot(class_manager)
            use_dot.save(f'{root}/{self.name}/use_graph.gv')
