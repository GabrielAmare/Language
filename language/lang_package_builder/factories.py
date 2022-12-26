from .cardinality_tracker import Cardinality
from .case_converting import pascal_case_to_snake_case
from .classes import ClassManager, TokenClass, LemmaClass, GroupClass, get_static_token_expr
from .dependencies import bnf
from .dependencies.python import *
from .namespaces import Namespace, Attribute

__all__ = [
    'build_models',
    'build_visitors',
]

MATERIALS_PATH = 'language.base.abstract'


def _order_attribute(attr: Attribute) -> tuple[bool, bool]:
    return (
        attr.optional,  # sort the optional fields in the end
        attr.multiple,  # sort the multiple fields in the end
        # name,  # sort by name in alphabetical order
    )


def _on_multiple_attributes(scope: Container, type_: BitwiseOrGR) -> tuple[GetItem, Variable]:
    if scope.env.lint(LintRule.DATACLASS_FROZEN):
        if scope.env.lint(LintRule.DATACLASS_MULTIPLE_NO_REPEATS):
            return scope.typing.frozenset(type_), Variable('frozenset')
        else:
            return scope.typing.tuple(type_, ELLIPSIS), Variable('tuple')
    else:
        if scope.env.lint(LintRule.DATACLASS_MULTIPLE_NO_REPEATS):
            return scope.typing.set(type_), Variable('set')
        else:
            return scope.typing.list(type_), Variable('list')


def _get_single_multiple_attribute(obj: bnf.ParallelGR) -> Attribute:
    namespace = Namespace.from_bnf_rule(obj)
    attributes = namespace.attrs
    assert len(attributes) == 1
    attr = attributes[0]
    assert attr.multiple
    return attr


def implement_tokens_method_body(initial_scope: Container, definition: LemmaClass):
    cardinality = Cardinality()
    
    def self(scope: Container, obj: bnf.ParallelGR) -> None:
        if isinstance(obj, bnf.Parallel):
            raise NotImplementedError
        elif isinstance(obj, bnf.Sequence):
            for rule in obj.rules:
                self(scope, rule)
        elif isinstance(obj, (bnf.Enum0, bnf.Enum1)):
            attr = _get_single_multiple_attribute(obj)
            with cardinality(multiple=True):
                with scope.FOR(
                        args=[Variable('i'), Variable('e')],
                        iter=Call(Variable('enumerate'), [GetAttr(Variable('self'), Variable(attr.name))])
                ) as for_block:
                    with for_block.IF(Variable('i')) as if_block:
                        self(if_block, obj.separator)
                    
                    self(for_block, obj.item)
        elif isinstance(obj, bnf.Optional):
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
            
            with cardinality(optional=True):
                if condition is None:
                    self(scope, obj.rule)
                else:
                    with scope.IF(condition) as if_block:
                        self(if_block, obj.rule)
        elif isinstance(obj, bnf.Repeat0):
            attr = _get_single_multiple_attribute(obj)
            with cardinality(optional=True, multiple=True):
                with scope.IF(GetAttr(Variable('self'), Variable(attr.name))) as if_block:
                    with if_block.FOR(
                            args=[Variable('e')],
                            iter=GetAttr(Variable('self'), Variable(attr.name))
                    ) as for_block:
                        self(for_block, obj.rule)
        elif isinstance(obj, bnf.Repeat1):
            attr = _get_single_multiple_attribute(obj)
            with cardinality(multiple=True):
                with scope.FOR(
                        args=[Variable('e')],
                        iter=GetAttr(Variable('self'), Variable(attr.name))
                ) as for_block:
                    self(for_block, obj.rule)
        elif isinstance(obj, bnf.Grouping):
            self(scope, obj.rule)
        elif isinstance(obj, bnf.Canonical):
            scope.YIELD(String(obj.expr))
        elif isinstance(obj, bnf.Literal):
            scope.YIELD(String(obj.expr))
        elif isinstance(obj, bnf.Store):
            _type = str(obj.type)
            target = definition.manager.classes.get(_type)
            if isinstance(target, TokenClass) and (static_expr := get_static_token_expr(target.rule)) is not None:
                scope.YIELD(atom(static_expr))
            else:
                if cardinality.multiple:
                    ref = Variable('e')
                else:
                    ref = GetAttr(Variable('self'), Variable(obj.key))
                
                scope.YIELD_FROM(
                    Call(left=scope.imports.get('tok', from_=MATERIALS_PATH), args=[ref])
                )
        elif isinstance(obj, bnf.Match):
            assert len(eval(obj.charset)) == 1 and not obj.inverted
            scope.YIELD(String(obj.charset))
    
    self(initial_scope, definition.rule.rule)


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

                # Make the class inherit from `Writable` if it has no other super class.
                mro = [Variable(superclass.name) for superclass in definition.mro]
                if mro:
                    cls.inherits(*mro)
                else:
                    cls.inherits(module.imports.get('Writable', from_=MATERIALS_PATH))
                
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
                        function.returns(module.typing.iterator(str))
                        
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
                            implement_tokens_method_body(function, definition)
                            
                            if definition.rule.indented:
                                function.decorate(module.imports.get('indented', from_=MATERIALS_PATH))
                        
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
