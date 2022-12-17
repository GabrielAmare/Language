from __future__ import annotations

import dataclasses
import functools

import utils
from language.base.bnf.v0_0_1 import *
from .namespaces import Namespace, Attribute

__all__ = [
    'BaseClass',
    'TokenClass',
    'LemmaClass',
    'GroupClass',
    'ClassManager',
    'get_static_token_expr',
]


def get_static_token_expr(obj: BuildToken) -> str | None:
    if isinstance(obj.rule, Literal):
        return obj.rule.expr.content[1:-1]
    else:
        return None


@dataclasses.dataclass
class BaseClass:
    name: str
    namespace: Namespace
    rule: BuildGR
    subclasses: set[str]
    
    class _BaseClassConstructor(BuildGRVisitor['BaseClass']):
        def _build_group(self, obj: BuildGroup) -> GroupClass:
            return GroupClass(
                name=str(obj.type),
                namespace=Namespace(),
                rule=obj,
                subclasses=set(map(str, obj.refs)),
            )
        
        def _build_lemma(self, obj: BuildLemma) -> LemmaClass:
            return LemmaClass(
                name=str(obj.type),
                namespace=Namespace.from_bnf_rule(obj.rule),
                rule=obj,
                subclasses=set(),
            )
        
        def _build_token(self, obj: BuildToken) -> TokenClass | KeywordClass:
            static_expr: str | None = get_static_token_expr(obj)
            
            if static_expr is None:
                return TokenClass(
                    name=str(obj.type),
                    namespace=Namespace(
                        names=['content'],
                        attrs=[Attribute(types={'str'}, optional=False, multiple=False)]
                    ),
                    rule=obj,
                    subclasses=set(),
                )
            else:
                return TokenClass(
                    name=str(obj.type),
                    namespace=Namespace(),
                    rule=obj,
                    subclasses=set(),
                )
    
    from_rule = staticmethod(_BaseClassConstructor())


@dataclasses.dataclass
class KeywordClass(BaseClass):
    pass


@dataclasses.dataclass
class TokenClass(BaseClass):
    rule: BuildToken


@dataclasses.dataclass
class LemmaClass(BaseClass):
    rule: BuildLemma


@dataclasses.dataclass
class GroupClass(BaseClass):
    rule: BuildGroup


@dataclasses.dataclass
class ClassManager:
    classes: dict[str, BaseClass] = dataclasses.field(default_factory=dict)
    
    """A class that manages a set of classes and their relations.

    The ClassManager class stores a set of classes and provides two properties that
    return the inheritance and reference relations between the classes.

    Attributes:
        classes: A dictionary that maps class names (strings) to `BaseClass` objects.

    Properties:
        mro_graph: An acyclic directed graph that represents the inheritance relations
            between the classes in the `classes` dictionary.
        use_graph: An acyclic directed graph that represents the references from a class
            to another via attributes in the `classes` dictionary.
    """
    
    @functools.cached_property
    def mro_graph(self) -> utils.AcyclicDirectedGraph:
        """
        Returns an acyclic directed graph that represents the inheritance relations
        between the classes in the `classes` dictionary.
        """
        
        mro_graph: utils.AcyclicDirectedGraph[str] = utils.AcyclicDirectedGraph()
        for class_name, class_definition in self.classes.items():
            for subclass_name in class_definition.subclasses:
                mro_graph.add_link(class_name, subclass_name)
        
        return mro_graph
    
    @functools.cached_property
    def use_graph(self) -> utils.AcyclicDirectedGraph:
        """
        Returns an acyclic directed graph that represents the references from a class
        to another via attributes in the `classes` dictionary.
        """
        use_graph: utils.AcyclicDirectedGraph[str] = utils.AcyclicDirectedGraph()
        for class_name, class_definition in self.classes.items():
            for attr in class_definition.namespace.attrs:
                for attr_type in attr.types:
                    use_graph.add_link(class_name, attr_type)
        return use_graph
    
    @classmethod
    def from_grammar(cls, grammar: Engine) -> ClassManager:
        return cls({
            str(obj.type): BaseClass.from_rule(obj)
            for obj in grammar.rules
            if isinstance(obj, (BuildGroup, BuildLemma, BuildToken))
        })
