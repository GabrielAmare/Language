import graphviz
from graphs import Ordering

from .case_converting import pascal_case_to_snake_case
from .classes import ClassManager, TokenClass, LemmaClass, GroupClass

__all__ = [
    'build_mro_dot',
    'build_use_dot',
]


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


def build_use_dot(manager: ClassManager) -> graphviz.Digraph:
    dot = graphviz.Digraph()
    
    graph = manager.use_graph
    ordering = Ordering(graph)
    
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
            ordering.get_node_order(name),
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
