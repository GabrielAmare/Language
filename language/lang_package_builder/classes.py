from __future__ import annotations

import dataclasses
import functools

import utils
from .casters import Caster
from .dependencies.bnf import *
from .namespaces import Namespace, Attribute

__all__ = [
    'MroGraph',
    'BaseClass',
    'TokenClass',
    'LemmaClass',
    'GroupClass',
    'ClassManager',
    'get_static_token_expr',
]


def get_static_token_expr(obj: BuildToken) -> str | None:
    if isinstance(obj.rule, Literal):
        return eval(obj.rule.expr)
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
                    namespace=Namespace(attrs=[
                        Attribute(name='content', types={'str'}, optional=False, multiple=False)
                    ]),
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
    caster: Caster | None = None


@dataclasses.dataclass
class LemmaClass(BaseClass):
    rule: BuildLemma


@dataclasses.dataclass
class GroupClass(BaseClass):
    rule: BuildGroup


@dataclasses.dataclass
class MroGraph(utils.AcyclicDirectedGraph[str]):
    def all_subclasses(self, name: str) -> list[str]:
        return self.get_all_targets(name)
    
    def direct_subclasses(self, name: str) -> list[str]:
        return self.get_targets(name)
    
    def all_superclasses(self, name: str) -> list[str]:
        return self.get_all_origins(name)
    
    def direct_superclasses(self, name: str) -> list[str]:
        return self.get_origins(name)
    
    def bottom_up_hierarchy(self) -> list[str]:
        return sorted(self.nodes, key=self.get_target_order)
    
    def get_mro(self, name: str) -> list[str]:
        """Return a consistent mro for the class `name`."""
        superclasses: list[str] = self.direct_superclasses(name)
        return sorted(superclasses, key=lambda superclass_name: (
            -self.get_origin_order(superclass_name),  # sort the classes by decreasing origin order.
            superclass_name,  # sort them by alphabetical order.
        ))


def _is_static_rule(rule: ParallelGR) -> bool:
    if isinstance(rule, Sequence):
        return all(map(_is_static_rule, rule.rules))
    elif isinstance(rule, Literal):
        return True
    elif isinstance(rule, Match):
        return len(eval(rule.charset)) == 1 and rule.inverted is None
    else:
        return False


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
    def mro_graph(self) -> MroGraph:
        """
        Returns an acyclic directed graph that represents the inheritance relations
        between the classes in the `classes` dictionary.
        """
        
        mro_graph: MroGraph = MroGraph()
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
    
    def simplify_common_signatures(self) -> None:
        """
            If all direct subclasses of A, A_0 -> A_n share the same attributes, move them to the signature of A.
            - we want to move all the attributes without a default value (that could break the behaviour of dataclasses)
        """
        all_classes: list[BaseClass] = [self.classes[name] for name in self.mro_graph.bottom_up_hierarchy()]
        
        for superclass in all_classes:
            subclasses = [self.classes[name] for name in self.mro_graph.direct_subclasses(superclass.name)]
            
            if not subclasses:
                continue
            
            namespaces: list[Namespace] = [cls.namespace for cls in subclasses]
            
            common_namespace: Namespace = functools.reduce(Namespace.intersection, namespaces)
            
            if common_namespace:
                superclass.namespace = superclass.namespace.union(common_namespace)
                
                for subclass in subclasses:
                    subclass.namespace = subclass.namespace.difference(common_namespace)
    
    def is_private_constant_token(self, name: str) -> bool:
        """
        Return True when the given `name` correspond to the nomenclature for the private tokens.
        1) the name must start with '_'
        2) the corresponding class must be a TokenClass
        3) the corresponding class rule must be static.
        """
        if not name.startswith('_'):
            return False
        
        cls = self.classes[name]
        
        return isinstance(cls, TokenClass) and _is_static_rule(cls.rule.rule)
    
    def apply_casters(self, casters: dict[str, Caster]) -> None:
        """This operation will apply casters on the tokens."""
        for target in self.classes.values():
            if not isinstance(target, TokenClass):
                continue
            
            if target.name not in casters:
                continue
            
            target.caster = casters[target.name]
        
        # we then replace all the references to the transformed tokens with appropriate types.
        for target in self.classes.values():
            target.namespace = target.namespace.apply_casters(casters=casters)
    
    def order_class(self, cls: BaseClass) -> tuple[int, int, str]:
        return (
            self.mro_graph.get_origin_order(cls.name),  # sort the classes by inheritance order.
            self.use_graph.get_target_order(cls.name),  # sort the classes by references order.
            cls.name,  # sort by name in alphabetical order
        )
