import dataclasses
import re
import typing

from language.base.python import *
from .classes import ClassManager, BaseClass, TokenClass, GroupClass, get_static_token_expr
from .namespaces import Namespace, Attribute
from language.base.bnf import v0_0_1 as bnf

__all__ = [
    'build_models',
    'build_visitors',
]



def _pascal_case_to_snake_case(class_name: str) -> str:
    """
    Extract the method name from a class name in PascalCase format and convert it to snake_case format.

    Args:
    - class_name (str): The class name in PascalCase format to process.

    Returns:
    - str: The method name in snake_case format.

    Examples:
    - _extract_method_name("FooBarBaz") -> "_foo_bar_baz"
    - _extract_method_name("Foo123Bar456Baz") -> "_foo123_bar456_baz"
    - _extract_method_name("ExampleGR") -> "_example_g_r"
    """
    if not re.match(r'^_?(?:[A-Z][a-z\d_]*)+$', class_name):
        raise ValueError('`class_name` must be in PascalCase format.')
    
    return re.sub(r'[A-Z][a-z\d_]*', lambda m: '_' + m.group(0).lower(), class_name)


def _order_attribute(item: tuple[str, Attribute]) -> tuple[bool, bool]:
    attr = item[1]
    return (
        attr.optional,  # sort the optional fields in the end
        attr.multiple,  # sort the multiple fields in the end
        # name,  # sort by name in alphabetical order
    )


def _order_class(class_manager: ClassManager) -> typing.Callable[[typing.Any], tuple[int, int, str]]:
    def wrapped(item: typing.Tuple[str, BaseClass]) -> tuple[int, int, str]:
        name = item[0]
        return (
            class_manager.mro_graph.get_origin_order(name),  # sort the classes by inheritance order.
            class_manager.use_graph.get_target_order(name),  # sort the classes by references order.
            name,  # sort by name in alphabetical order
        )
    
    return wrapped


def _on_multiple_attributes(module: DynamicModule, type_: BitwiseOrGR) -> tuple[GetItem, Variable]:
    if module.env.lint(LintRule.DATACLASS_FROZEN):
        if module.env.lint(LintRule.DATACLASS_MULTIPLE_NO_REPEATS):
            return module.typing.frozenset(type_), Variable('frozenset')
        else:
            return module.typing.tuple(type_, ELLIPSIS), Variable('tuple')
    else:
        if module.env.lint(LintRule.DATACLASS_MULTIPLE_NO_REPEATS):
            return module.typing.set(type_), Variable('set')
        else:
            return module.typing.list(type_), Variable('list')


def _build_class_attribute(module: DynamicModule, cls: DynamicClass, name: str, attr: Attribute) -> None:
    default: BitwiseXorGR | None = None
    target_type = module.typing.union(*map(Variable, sorted(attr.types)))
    
    if attr.multiple:
        target_type, default_factory = _on_multiple_attributes(module, target_type)
        
        if attr.optional:
            default = Call(
                left=module.imports.get('field', from_='dataclasses'),
                args=[Kwarg(name=Variable('default_factory'), value=default_factory)]
            )
    
    if attr.optional:
        target_type = module.typing.optional(target_type)
        
        if not attr.multiple or module.env.lint(LintRule.DATACLASS_MULTIPLE_CAN_BE_NONE):
            default = NONE
    
    cls.new_variable(name=name, type_=target_type, value=default)


@dataclasses.dataclass
class TokensBodyMethodFactory(bnf.ParallelGRVisitor[typing.Iterator[Statement]]):
    module: DynamicModule
    
    def _parallel(self, obj: bnf.Parallel) -> typing.Iterator[Statement]:
        raise NotImplementedError
    
    def _sequence(self, obj: bnf.Sequence) -> typing.Iterator[Statement]:
        for rule in obj.rules:
            yield from self(rule)
    
    def _enum0(self, obj: bnf.Enum0) -> typing.Iterator[Statement]:
        namespace = Namespace.from_bnf_rule(obj)
        attributes = list(namespace.items())
        assert len(attributes) == 1
        name, attr = attributes[0]
        assert attr.multiple
        
        yield For(
            args=[Variable('i'), Variable('e')],
            iter=Call(Variable('enumerate'), [
                GetAttr(Variable('self'), Variable(name))
            ]),
            block=Block(statements=[
                If(
                    test=Variable('i'),
                    block=Block(statements=list(self(obj.separator)))
                ),
                *self(obj.item)
            ])
        )
    
    def _enum1(self, obj: bnf.Enum1) -> typing.Iterator[Statement]:
        namespace = Namespace.from_bnf_rule(obj)
        attributes = list(namespace.items())
        assert len(attributes) == 1
        name, attr = attributes[0]
        assert attr.multiple
        
        yield For(
            args=[Variable('i'), Variable('e')],
            iter=Call(Variable('enumerate'), [GetAttr(Variable('self'), Variable(name))]),
            block=Block(statements=[
                If(
                    test=Variable('i'),
                    block=Block(statements=list(self(obj.separator)))
                ),
                *self(obj.item)
            ])
        )
    
    def _optional(self, obj: bnf.Optional) -> typing.Iterator[Statement]:
        namespace = Namespace.from_bnf_rule(obj.rule)
        attributes = list(namespace.items())
        
        required = [
            GetAttr(Variable('self'), Variable(name))
            for name, attr in attributes
            if not attr.optional
        ]
        if len(required) == 0:
            condition = None
        elif len(required) == 1:
            condition = required[0]
        else:
            condition = And(items=required)
        
        if condition is None:
            yield from self(obj.rule)
        else:
            yield If(
                test=condition,
                block=Block(statements=list(self(obj.rule)))
            )
    
    def _repeat0(self, obj: bnf.Repeat0) -> typing.Iterator[Statement]:
        namespace = Namespace.from_bnf_rule(obj)
        attributes = list(namespace.attributes.items())
        assert len(attributes) == 1
        name, attr = attributes[0]
        assert attr.multiple
        
        yield If(
            test=GetAttr(Variable('self'), Variable(name)),
            block=Block([
                For(
                    args=[Variable('e')],
                    iter=GetAttr(Variable('self'), Variable(name)),
                    block=Block(statements=list(self(obj.rule)))
                )
            ])
        )
    
    def _repeat1(self, obj: bnf.Repeat1) -> typing.Iterator[Statement]:
        namespace = Namespace.from_bnf_rule(obj)
        attributes = list(namespace.items())
        assert len(attributes) == 1
        name, attr = attributes[0]
        assert attr.multiple
        
        yield For(
            args=[Variable('e')],
            iter=GetAttr(Variable('self'), Variable(name)),
            block=Block(statements=list(self(obj.rule)))
        )
    
    def _grouping(self, obj: bnf.Grouping) -> typing.Iterator[Statement]:
        yield from self(obj.rule)
    
    def _canonical(self, obj: bnf.Canonical) -> typing.Iterator[Statement]:
        yield Yield([String(obj.expr.content)])
    
    def _literal(self, obj: bnf.Literal) -> typing.Iterator[Statement]:
        yield Yield([String(obj.expr.content)])
    
    def _match_as(self, obj: bnf.MatchAs) -> typing.Iterator[Statement]:
        ref = GetAttr(Variable('self'), Variable(obj.key.content))
        yield YieldFrom(expr=Call(left=self.module.imports.get('tok', from_='language.base.abstract'), args=[ref]))
    
    def _match_char(self, obj: bnf.MatchChar) -> typing.Iterator[Statement]:
        assert not obj.inverted
        assert len(obj.charset.content[1:-1]) == 1
        yield Yield([String(obj.charset.content)])
    
    def _match_in(self, obj: bnf.MatchIn) -> typing.Iterator[Statement]:
        ref = Variable('e')
        yield YieldFrom(expr=Call(left=self.module.imports.get('tok', from_='language.base.abstract'), args=[ref]))


def _build_class_method__tokens__(module: DynamicModule, cls: DynamicClass, obj: bnf.BuildGR) -> None:
    if isinstance(obj, bnf.BuildGroup):
        return
    
    function = (
        cls.new_function('__tokens__')
        .add_param('self')
        .set_returns(module.typing.iterator(Variable('str')))
    )
    
    if isinstance(obj, bnf.BuildToken):
        static_expr = get_static_token_expr(obj)
        if static_expr is None:
            # TODO : Find if the token is bound to a certain type (int, str, float, bool, ...) and use the correct
            #  writing function accordingly.
            statement = Yield([Call(Variable('str'), [GetAttr(left=Variable('self'), right=Variable('content'))])])
        else:
            statement = Yield([atom(static_expr)])
        
        function.add_statement(statement)
        return
    
    assert isinstance(obj, bnf.BuildLemma)
    
    tokens_body_method_factory: TokensBodyMethodFactory = TokensBodyMethodFactory(module=module)
    
    function.add_statements(tokens_body_method_factory(obj.rule))
    
    if obj.indented is bnf.INDENTED:
        function.add_decorator(module.imports.get('indented', from_='language.base.abstract'))


def build_class(module: DynamicModule, class_manager: ClassManager, class_name: str, definition: BaseClass):
    cls = module.new_class(class_name)
    
    decorator = module.imports.get('dataclass', from_='dataclasses')
    
    if module.env.lint(LintRule.DATACLASS_FROZEN):
        decorator = Call(decorator, [Kwarg(Variable('frozen'), TRUE)])
    
    cls.add_decorator(decorator)
    
    mro: list[str] = class_manager.mro_graph.get_origins(class_name)
    cls.add_supers(map(Variable, mro))
    
    # Build the class attributes.
    for attr_name, attr in sorted(definition.namespace.items(), key=_order_attribute):
        _build_class_attribute(module, cls, attr_name, attr)
    
    # Build the class methods
    _build_class_method__tokens__(module, cls, definition.rule)
    
    # Make the class inherit from `Writable` if it has no other super class.
    if not mro:
        cls.add_super(module.imports.get('Writable', from_='language.base.abstract'))
    
    # Make the class abstract when it's a `GroupClass`
    if isinstance(definition, GroupClass):
        cls.add_super(module.imports.get('ABC', from_='abc'))
    
    # Build the token constant when the class is a static token.
    if isinstance(definition, TokenClass) and get_static_token_expr(definition.rule) is not None:
        constant_name = _pascal_case_to_snake_case(class_name).upper().lstrip('_')
        module.new_variable(name=constant_name, type_=Variable(class_name), value=Call(Variable(class_name), []))


def build_models(package: DynamicPackage, class_manager: ClassManager) -> DynamicModule:
    module = package.new_module('models')
    
    # Build all the classes.
    for class_name, class_def in sorted(class_manager.classes.items(), key=_order_class(class_manager)):
        build_class(module, class_manager, class_name, class_def)
    
    import_future_annotations: bool = True  # TODO : set to true only when necessary.
    if import_future_annotations:
        module.future_import('annotations')
    
    return module


def _build_visitor_class_call(cls: DynamicClass, root_class: str, classes: list[str]) -> DynamicFunction:
    function = (
        cls.new_function('__call__')
        .add_param('self')
        .add_param('obj', Variable(root_class))
        .set_returns(Variable('_E'))
    )
    
    # Build the function body
    switch_builder = SwitchBuilder()
    for subclass_name in classes:
        method_name = _pascal_case_to_snake_case(subclass_name)
        switch_builder.add_case(
            Call(left=Variable('isinstance'), args=[Variable('obj'), Variable(subclass_name)]),
            [
                Return([Call(
                    left=GetAttr(left=Variable('self'), right=Variable(method_name)),
                    args=[Variable('obj')]
                )])
            ]
        )
    switch_builder.set_default([Raise(Variable('NotImplementedError'))])
    
    function.add_statements(switch_builder.build())
    
    return function


def _build_visitor_class(module: DynamicModule, class_manager: ClassManager, root_class: str) -> DynamicClass:
    children_classes = class_manager.mro_graph.get_all_targets(root_class)
    children_classes = filter(
        lambda subclass_name: not isinstance(class_manager.classes.get(subclass_name), GroupClass),
        children_classes
    )
    children_classes = sorted(
        children_classes,
        key=lambda subclass_name: (
            class_manager.mro_graph.get_origin_order(subclass_name),
            subclass_name
        )
    )
    
    cls = (
        module.new_class(root_class + 'Visitor')
        .add_super(module.typing.generic(Variable('_E')))
        .add_super(module.imports.get('ABC', from_='abc'))
    )
    
    _build_visitor_class_call(cls, root_class, children_classes)
    
    for class_name in children_classes:
        method_name = _pascal_case_to_snake_case(class_name)
        (
            cls.new_function(method_name)
            .add_decorator(module.imports.get('abstractmethod', from_='abc'))
            .add_param('self')
            .add_param('obj', Variable(class_name))
            .set_returns(Variable('_E'))
            .add_statement(PASS)
        )
    
    return cls


def build_visitors(package: DynamicPackage, class_manager: ClassManager, root_classes: list[str]) -> DynamicModule:
    module = package.new_module('visitors')
    
    module.imports.get_all('.models')
    
    module.new_variable(name='_E', value=Call(module.imports.get('TypeVar', from_='typing'), [atom('_E')]))
    
    for root_class in root_classes:
        _build_visitor_class(module, class_manager, root_class)
    
    return module
