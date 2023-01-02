from __future__ import annotations

import dataclasses
import functools

from utils.graphs.structures import DirectedAcyclicGraph, DirectedGraph, Ordering
from .casters import Caster
from .dependencies.bnf import *
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
        return obj.rule.expr[1:-1]
    else:
        return None


@dataclasses.dataclass
class BaseClass:
    manager: ClassManager
    name: str
    namespace: Namespace
    rule: BuildGR
    subclasses: set[str]
    
    @property
    def mro(self) -> list[BaseClass]:
        """Return a consistent mro for the class `name`."""
        names = self.manager.mro_graph.origins(self.name)
        classes = map(self.manager.classes.get, names)
        sorted_classes = sorted(classes, key=BaseClass.mro_order)
        return list(sorted_classes)
    
    def mro_order(self) -> tuple[int, str]:
        """
            Sorting criteria for direct superclasses of a common class.
            1) It will make sure that the mro is consistent
            2) It will make sure the output mro does not rely on the order of inputs.
        """
        return (
            -self.manager.mro_graph.get_origin_order(self.name),  # sort the classes by decreasing origin order.
            self.name,  # sort them by alphabetical order.
        )
    
    @staticmethod
    def from_rule(manager: ClassManager, obj: BuildGR):
        if isinstance(obj, BuildGroup):
            return GroupClass(
                manager=manager,
                name=str(obj.type),
                namespace=Namespace(),
                rule=obj,
                subclasses=set(map(str, obj.refs)),
            )
        elif isinstance(obj, BuildLemma):
            return LemmaClass(
                manager=manager,
                name=str(obj.type),
                namespace=Namespace.from_bnf_rule(obj.rule),
                rule=obj,
                subclasses=set(),
            )
        elif isinstance(obj, BuildToken):
            static_expr: str | None = get_static_token_expr(obj)
            
            if static_expr is None:
                return TokenClass(
                    manager=manager,
                    name=str(obj.type),
                    namespace=Namespace(attrs=[
                        Attribute(name='content', types={'str'}, optional=False, multiple=False)
                    ]),
                    rule=obj,
                    subclasses=set(),
                )
            else:
                return TokenClass(
                    manager=manager,
                    name=str(obj.type),
                    namespace=Namespace(),
                    rule=obj,
                    subclasses=set(),
                )
        else:
            raise ValueError(obj)


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
    def mro_graph(self) -> DirectedAcyclicGraph[str]:
        """
        Returns an acyclic directed graph that represents the inheritance relations
        between the classes in the `classes` dictionary.
        """
        return DirectedAcyclicGraph({
            class_name: set(class_definition.subclasses)
            for class_name, class_definition in self.classes.items()
        })
    
    @functools.cached_property
    def use_graph(self) -> DirectedGraph:
        """
        Returns an acyclic directed graph that represents the references from a class
        to another via attributes in the `classes` dictionary.
        """
        
        def get_type(name: str):
            cls = self.classes.get(name)
            if isinstance(cls, TokenClass) and cls.caster:
                return cls.caster.name
            else:
                return name
        
        return DirectedGraph({
            class_name: {
                get_type(attr_type)
                for attr in class_definition.namespace.attrs
                for attr_type in attr.types
            }
            for class_name, class_definition in self.classes.items()
        })
    
    @classmethod
    def from_grammar(cls, grammar: Engine) -> ClassManager:
        self = cls({})
        for obj in grammar.rules:
            self.classes[obj.type] = BaseClass.from_rule(self, obj)
        return self
    
    def simplify_common_signatures(self) -> None:
        """
            If all direct subclasses of A, A_0 -> A_n share the same attributes, move them to the signature of A.
            - we want to move all the attributes without a default value (that could break the behaviour of dataclasses)
        """
        
        all_classes: list[BaseClass] = [
            self.classes[name]
            for name in sorted(self.mro_graph, key=self.mro_graph.get_target_order)
        ]
        
        for superclass in all_classes:
            subclasses = [
                self.classes[name]
                for name in self.mro_graph.targets(superclass.name)
            ]
            
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
        use_ordering = Ordering(self.use_graph)
        return (
            self.mro_graph.get_origin_order(cls.name),  # sort the classes by inheritance order.
            use_ordering.get_node_order(cls.name),  # sort the classes by references order.
            cls.name,  # sort by name in alphabetical order
        )
