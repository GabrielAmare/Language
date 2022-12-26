import dataclasses
import typing

from .cardinality_tracker import Cardinality
from .case_converting import pascal_case_to_snake_case
from .classes import ClassManager, BaseClass, TokenClass, LemmaClass, GroupClass, get_static_token_expr
from .dependencies import bnf
from .dependencies.python import *
from .namespaces import Namespace, Attribute

__all__ = [
    'build_models',
    'build_visitors',
]


def _order_attribute(attr: Attribute) -> tuple[bool, bool]:
    return (
        attr.optional,  # sort the optional fields in the end
        attr.multiple,  # sort the multiple fields in the end
        # name,  # sort by name in alphabetical order
    )


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




def _get_single_multiple_attribute(obj: bnf.ParallelGR) -> Attribute:
    namespace = Namespace.from_bnf_rule(obj)
    attributes = namespace.attrs
    assert len(attributes) == 1
    attr = attributes[0]
    assert attr.multiple
    return attr


@dataclasses.dataclass
class TokensBodyMethodFactory(bnf.ParallelGRVisitor[typing.Iterator[Statement]]):
    module: DynamicModule
    definition: BaseClass
    class_manager: ClassManager
    cardinality: Cardinality = dataclasses.field(default_factory=Cardinality)
    
    def _parallel(self, obj: bnf.Parallel) -> typing.Iterator[Statement]:
        raise NotImplementedError
    
    def _sequence(self, obj: bnf.Sequence) -> typing.Iterator[Statement]:
        for rule in obj.rules:
            yield from self(rule)
    
    def _on_enum(self, obj: bnf.Enum0 | bnf.Enum1) -> typing.Iterator[Statement]:
        attr = _get_single_multiple_attribute(obj)
        with self.cardinality(multiple=True):
            yield For(
                args=[Variable('i'), Variable('e')],
                iter=Call(Variable('enumerate'), [GetAttr(Variable('self'), Variable(attr.name))]),
                block=Block(statements=[
                    If(
                        test=Variable('i'),
                        block=Block(statements=list(self(obj.separator)))
                    ),
                    *self(obj.item)
                ])
            )
    
    def _enum0(self, obj: bnf.Enum0) -> typing.Iterator[Statement]:
        yield from self._on_enum(obj)
    
    def _enum1(self, obj: bnf.Enum1) -> typing.Iterator[Statement]:
        yield from self._on_enum(obj)
    
    def _optional(self, obj: bnf.Optional) -> typing.Iterator[Statement]:
        namespace = Namespace.from_bnf_rule(obj.rule)
        attributes = namespace.attrs
        
        required = [
            GetAttr(Variable('self'), Variable(attr.name))
            for attr in attributes
            if not attr.optional
        ]
        
        if len(required) == 0:
            condition = None
        elif len(required) == 1:
            condition = required[0]
        else:
            condition = And(items=required)
        
        with self.cardinality(optional=True):
            if condition is None:
                yield from self(obj.rule)
            else:
                yield If(
                    test=condition,
                    block=Block(statements=list(self(obj.rule)))
                )
    
    def _repeat0(self, obj: bnf.Repeat0) -> typing.Iterator[Statement]:
        attr = _get_single_multiple_attribute(obj)
        with self.cardinality(optional=True, multiple=True):
            yield If(
                test=GetAttr(Variable('self'), Variable(attr.name)),
                block=Block([
                    For(
                        args=[Variable('e')],
                        iter=GetAttr(Variable('self'), Variable(attr.name)),
                        block=Block(statements=list(self(obj.rule)))
                    )
                ])
            )
    
    def _repeat1(self, obj: bnf.Repeat1) -> typing.Iterator[Statement]:
        attr = _get_single_multiple_attribute(obj)
        with self.cardinality(multiple=True):
            yield For(
                args=[Variable('e')],
                iter=GetAttr(Variable('self'), Variable(attr.name)),
                block=Block(statements=list(self(obj.rule)))
            )
    
    def _grouping(self, obj: bnf.Grouping) -> typing.Iterator[Statement]:
        yield from self(obj.rule)
    
    def _canonical(self, obj: bnf.Canonical) -> typing.Iterator[Statement]:
        yield Yield([String(obj.expr)])
    
    def _literal(self, obj: bnf.Literal) -> typing.Iterator[Statement]:
        yield Yield([String(obj.expr)])
    
    def _store(self, obj: bnf.Store) -> typing.Iterator[Statement]:
        _type = str(obj.type)
        definition = self.class_manager.classes.get(_type)
        if isinstance(definition, TokenClass) and (static_expr := get_static_token_expr(definition.rule)) is not None:
            yield Yield(expressions=[
                atom(static_expr)
            ])
        else:
            if self.cardinality.multiple:
                ref = Variable('e')
            else:
                ref = GetAttr(Variable('self'), Variable(obj.key))
            
            yield YieldFrom(expr=Call(left=self.module.imports.get('tok', from_='language.base.abstract'), args=[ref]))
    
    def _match(self, obj: bnf.Match) -> typing.Iterator[Statement]:
        assert len(eval(obj.charset)) == 1 and not obj.inverted
        yield Yield([String(obj.charset)])


def _get_constant_name(name: str) -> str:
    return pascal_case_to_snake_case(name).upper().lstrip('_')


def build_models(package: Package, class_manager: ClassManager) -> None:
    with package.MODULE('models') as module:
        # Build all the classes.
        for definition in sorted(class_manager.classes.values(), key=class_manager.order_class):
            if isinstance(definition, TokenClass) and definition.caster is not None:
                # in this case we don't build the class as the token should be turned into an external class.
                continue
            
            decorator = module.imports.get('dataclass', from_='dataclasses')
            
            if module.env.lint(LintRule.DATACLASS_FROZEN):
                decorator = Call(decorator, [Kwarg(Variable('frozen'), TRUE)])
            
            with module.CLASS(definition.name) as cls:
                cls.decorate(decorator)
                
                mro: list[str] = class_manager.mro_graph.get_mro(definition.name)
                cls.inherits(*map(Variable, mro))
                
                # Make the class inherit from `Writable` if it has no other super class.
                if not mro:
                    cls.inherits(module.imports.get('Writable', from_='language.base.abstract'))
                
                # Make the class abstract when it's a `GroupClass`
                if isinstance(definition, GroupClass):
                    cls.inherits(module.imports.get('ABC', from_='abc'))
                
                # Build the class attributes.
                for attr in sorted(definition.namespace, key=_order_attribute):
                    default: BitwiseXorGR | None = None
                    
                    if attr.default is not None:
                        default = atom(attr.default)
                    
                    target_type = module.typing.union(*map(Variable, sorted(attr.types)))
                    
                    if attr.multiple:
                        target_type, default_factory = _on_multiple_attributes(module, target_type)
                        
                        if attr.optional:
                            default = Call(
                                left=module.imports.get('field', from_='dataclasses'),
                                args=[Kwarg(name=Variable('default_factory'), value=default_factory)]
                            )
                    
                    if attr.optional:
                        if not attr.multiple or module.env.lint(LintRule.DATACLASS_MULTIPLE_CAN_BE_NONE):
                            if attr.default is None:
                                target_type = module.typing.optional(target_type)
                                default = NONE
                    
                    cls.ASSIGN(name=attr.name, type_=target_type, value=default)
                
                # Build the class `__tokens__` method.
                if not isinstance(definition, GroupClass):
                    with cls.METHOD('__tokens__') as function:
                        function.returns(module.typing.iterator(Variable('str')))
                        
                        if isinstance(definition, TokenClass):
                            static_expr = get_static_token_expr(definition.rule)
                            if static_expr is None:
                                # TODO : Find if the token is bound to a certain type (int, str, float, bool, ...) and use the correct
                                #  writing function accordingly.
                                to_yield = [
                                    Call(Variable('str'), [GetAttr(left=Variable('self'), right=Variable('content'))])]
                            else:
                                to_yield = [atom(static_expr)]
                            
                            function.YIELD(*to_yield)
                        elif isinstance(definition, LemmaClass):
                            tokens_body_method_factory: TokensBodyMethodFactory = TokensBodyMethodFactory(
                                module=module,
                                definition=definition,
                                class_manager=class_manager,
                            )
                            
                            for statement in tokens_body_method_factory(definition.rule.rule):
                                function += statement
                            
                            if definition.rule.indented:
                                function.decorate(module.imports.get('indented', from_='language.base.abstract'))
                        
                        else:
                            raise NotImplementedError
            
            # Build the token constant when the class is a static token.
            if isinstance(definition, TokenClass) and get_static_token_expr(definition.rule) is not None:
                constant_name = _get_constant_name(definition.name)
                module.ASSIGN(
                    name=constant_name,
                    type_=Variable(definition.name),
                    value=Call(Variable(definition.name), [])
                )
        
        # add `from __future__ import annotations` to avoid reference order errors.
        import_future_annotations: bool = True  # TODO : set to true only when necessary.
        if import_future_annotations:
            module.future_import('annotations')


def build_visitors(package: Package, class_manager: ClassManager, root_classes: list[str]) -> None:
    with package.MODULE('visitors') as module:
        module.imports.get_all('.models')
        
        module.ASSIGN(name='_E', value=Call(module.imports.get('TypeVar', from_='typing'), [atom('_E')]))
        
        for root_class in root_classes:
            children_classes = class_manager.mro_graph.get_all_targets(root_class)
            
            children_classes = filter(
                lambda subclass_name: not isinstance(class_manager.classes.get(subclass_name), GroupClass),
                children_classes
            )
            children_classes = sorted(
                children_classes,
                key=lambda subclass_name: (
                    0 if class_manager.is_private_constant_token(subclass_name) else 1,
                    class_manager.mro_graph.get_origin_order(subclass_name),
                    subclass_name
                )
            )
            
            with module.CLASS(f"{root_class}Visitor") as cls:
                cls.inherits(module.typing.generic(Variable('_E')))
                cls.inherits(module.imports.get('ABC', from_='abc'))
                
                with cls.METHOD('__call__') as function:
                    function.param('obj').type(Variable(root_class))
                    function.returns(Variable('_E'))
                    
                    if children_classes:
                        with function.SWITCH() as switch:
                            for subclass_name in children_classes:
                                method_name = pascal_case_to_snake_case(subclass_name)
                                
                                if class_manager.is_private_constant_token(subclass_name):
                                    method_name = method_name[1:]
                                    constant_name = _get_constant_name(subclass_name)
                                    condition = Is(left=Variable('obj'), right=Variable(constant_name))
                                else:
                                    condition = Call(
                                        left=Variable('isinstance'),
                                        args=[Variable('obj'), Variable(subclass_name)]
                                    )
                                
                                with switch.IF(condition) as if_block:
                                    if_block.RETURN(
                                        Call(
                                            left=GetAttr(left=Variable('self'), right=Variable(method_name)),
                                            args=[Variable('obj')]
                                        )
                                    )
                            
                            with switch.ELSE() as else_block:
                                else_block += Raise(Variable('NotImplementedError'))
                
                for class_name in children_classes:
                    method_name = pascal_case_to_snake_case(class_name)
                    
                    if class_manager.is_private_constant_token(class_name):
                        method_name = method_name[1:]
                        constant_name = _get_constant_name(class_name)
                        type_hint = Variable(constant_name)
                    else:
                        type_hint = Variable(class_name)
                    
                    with cls.METHOD(method_name) as function:
                        function.decorate(module.imports.get('abstractmethod', from_='abc'))
                        function.param('obj').type(type_hint)
                        function.returns(Variable('_E'))
