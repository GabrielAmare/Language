import abc
import dataclasses
import enum
import typing

from core.langs.python.lang.shortcuts import *
from .DynamicDef import DynamicDef
from .DynamicModule import DynamicModule
from .TypeSwitch import TypeSwitch
from .base import *

__all__ = [
    'ImportExternalMethods',
]

_RAISE_NOT_IMPLEMENTED_ERROR = Raise(expr=EXCEPTIONS.NOT_IMPLEMENTED_ERROR)

_TRUE_PROPERTY_DECORATOR = Decorator(expr=Variable('property'))
_TRUE_CLASSMETHOD_DECORATOR = Decorator(expr=Variable('classmethod'))
_TRUE_ABSTRACTMETHOD_DECORATOR = Decorator(expr=ABC.ABSTRACT_METHOD)

_METHOD_DECORATOR = Decorator(expr=Variable('__method__'))
_PROPERTY_DECORATOR = Decorator(expr=Variable('__property__'))
_CACHED_PROPERTY_DECORATOR = Decorator(expr=Variable('__cached_property__'))
_CLASS_METHOD_DECORATOR = Decorator(expr=Variable('__class_method__'))
_STATIC_METHOD_DECORATOR = Decorator(expr=Variable('__static_method__'))

_PLACEHOLDER_DECORATORS = [
    _METHOD_DECORATOR,
    _PROPERTY_DECORATOR,
    _CACHED_PROPERTY_DECORATOR,
    _CLASS_METHOD_DECORATOR,
    _STATIC_METHOD_DECORATOR,
]


class FunctionKind(str, enum.Enum):
    FUNCTION = "FUNCTION"
    METHOD = "METHOD"
    PROPERTY = "PROPERTY"
    CACHED_PROPERTY = "CACHED_PROPERTY"
    CLASS_METHOD = "CLASS_METHOD"


@dataclasses.dataclass
class AbstractFunctionParser(abc.ABC):
    module: DynamicModule
    function: DynamicDef

    def require_first_arg(self) -> Argument:
        if len(self.function.args) == 0:
            raise Warning("The function must have at least 1 argument.")

        arg = self.function.args[0]

        if not isinstance(arg, Argument):
            raise Warning("The function first argument must be an Argument object.", arg)

        return arg

    @staticmethod
    def require_argument_type(arg: Argument) -> Expression:
        if arg.type is None:
            raise Warning(f"The function first argument must be typed.")

        return arg.type

    def _new(self, statements: list[Statement]) -> DynamicDef:
        return DynamicDef(
            name=self.function.name,
            docstring=self.function.docstring,
            rtype=self.function.rtype,
            args=self.function.args[:],
            statements=statements,
            decorators=self.function.decorators[:]
        )

    @abc.abstractmethod
    def new(self, statements: list[Statement]) -> DynamicDef:
        """"""

    @abc.abstractmethod
    def build(self) -> typing.Iterator[tuple[Variable, DynamicDef]]:
        """"""

    @abc.abstractmethod
    def get_class_target(self) -> Variable:
        """"""


@dataclasses.dataclass
class ClassMethodParser(AbstractFunctionParser):
    def new(self, statements: list[Statement]) -> DynamicDef:
        result = self._new(statements)
        result.add_decorator(_TRUE_CLASSMETHOD_DECORATOR)
        return result

    def get_class_target(self) -> Variable:
        arg = self.require_first_arg()

        if arg.name != Variable('cls'):
            raise Warning("The function first argument must be cls.", arg.name)

        type_ = self.require_argument_type(arg)

        if not isinstance(type_, GetAttr):
            raise Warning  # TODO : write a meaningful error message.

        if type_.right != Variable('__class__'):
            raise Warning  # TODO : write a meaningful error message.

        if not isinstance(type_.left, Variable):
            raise Warning  # TODO : write a meaningful error message.

        return type_.left

    def build(self) -> typing.Iterator[tuple[Variable, DynamicDef]]:
        target_class = self.get_class_target()
        output_function = self.new(statements=self.function.statements)
        yield target_class, output_function


@dataclasses.dataclass
class SelfParser(AbstractFunctionParser, abc.ABC):
    def get_class_target(self) -> Variable:
        arg = self.require_first_arg()

        if arg.name != Variable('self'):
            raise Warning(f"The function first argument must be self.", arg.name)

        type_ = self.require_argument_type(arg)

        if not isinstance(type_, Variable):
            raise Warning(f"The function first argument type must be a variable.", type_)

        return type_

    @classmethod
    def get_types(cls, expr: Expression) -> list[Variable]:
        if isinstance(expr, Variable):
            return [expr]
        elif isinstance(expr, Tuple):
            items = []
            for item in expr.items:
                if not isinstance(item, Variable):
                    raise Warning("One of its types is not handled.", expr)
                items.append(item)
            return items
        else:
            raise Warning("Expression not handled.", expr)

    def build(self) -> typing.Iterator[tuple[Variable, DynamicDef]]:
        class_name: Variable = self.get_class_target()

        if self.function.is_type_switch():
            switch: TypeSwitch = self.function.as_type_switch()

            if switch.arg != Variable('self'):
                raise Warning("Function switch argument must be self.", switch.arg)

            for type_expr, case in switch.items():
                for type_item in self.get_types(type_expr):
                    output_function: DynamicDef = self.new(statements=case.statements)
                    yield type_item, output_function

            default_method: DynamicDef = self.new(statements=switch.default.statements)
            yield class_name, default_method

        else:
            default_method: DynamicDef = self.new(statements=self.function.statements)
            yield class_name, default_method


@dataclasses.dataclass
class MethodParser(SelfParser):
    def new(self, statements: list[Statement]) -> DynamicDef:
        result = self._new(statements)
        return result

    def build(self) -> typing.Iterator[tuple[Variable, DynamicDef]]:
        yield from super().build()


@dataclasses.dataclass
class PropertyParser(SelfParser):
    def new(self, statements: list[Statement]) -> DynamicDef:
        result = self._new(statements)
        result.add_decorator(_TRUE_PROPERTY_DECORATOR)
        return result

    def build(self) -> typing.Iterator[tuple[Variable, DynamicDef]]:
        if len(self.function.args) > 1:
            raise Warning(f"property must have only 1 argument.")

        yield from super().build()


@dataclasses.dataclass
class CachedPropertyParser(SelfParser):
    def new(self, statements: list[Statement]) -> DynamicDef:
        result = self._new(statements)
        result.add_decorator(Decorator(expr=self.module.imports('functools').getattr('cached_property')))
        return result

    def build(self) -> typing.Iterator[tuple[Variable, DynamicDef]]:
        if len(self.function.args) > 1:
            raise Warning(f"property must have only 1 argument.")

        yield from super().build()


@dataclasses.dataclass
class ImportExternalMethods:
    """Import the methods from the ``methods_module`` to their corresponding classes in the ``classes_module``."""
    classes: DynamicModule
    keep_absolute_imports: bool = True

    def get_class(self, __type: Variable) -> Class:
        """Find a class using its name."""
        cls = self.classes.get_class(__type)

        if not isinstance(cls, Class):
            raise Warning(f"the class {__type.to_str()!r} was not found !")

        return cls

    def get_function_parser(self, function: DynamicDef) -> typing.Optional[AbstractFunctionParser]:
        is_property = function.has_decorator(_PROPERTY_DECORATOR)
        is_cached_property = function.has_decorator(_CACHED_PROPERTY_DECORATOR)
        is_method = function.has_decorator(_METHOD_DECORATOR)
        is_class_method = function.has_decorator(_CLASS_METHOD_DECORATOR)

        n_function_types = is_method + is_property + is_class_method

        if n_function_types > 1:
            raise Warning(f"the function `{function.name!s}` have too many model decorator !")

        if is_method:
            return MethodParser(module=self.classes, function=function)
        elif is_property:
            return PropertyParser(module=self.classes, function=function)
        elif is_cached_property:
            return CachedPropertyParser(module=self.classes, function=function)
        elif is_class_method:
            return ClassMethodParser(module=self.classes, function=function)
        else:
            return None

    def store_method(self, class_name: Variable, function: DynamicDef) -> None:
        class_ = self.get_class(class_name)

        function.args[0] = Argument(name=function.args[0].name, type=None)
        function.remove_decorators(_PLACEHOLDER_DECORATORS)

        # remove the empty lines
        function.remove_empty_lines()

        if len(function.statements) == 1 and function.statements[0] == _RAISE_NOT_IMPLEMENTED_ERROR:
            function.statements = []

            if _TRUE_PROPERTY_DECORATOR in function.decorators:
                index = function.decorators.index(_TRUE_PROPERTY_DECORATOR)
            else:
                index = -1

            function.decorators.insert(index + 1, _TRUE_ABSTRACTMETHOD_DECORATOR)

            # TODO : implement a warning when the docstring is missing.
        else:
            function.docstring = None

        class_.append_method(function.to_def())

    def build(self, methods: DynamicModule):
        if self.keep_absolute_imports:
            # import the absolute imports used in the `methods` module.
            for import_stmt in methods.get_imports():
                if isinstance(import_stmt, ImportFrom) and isinstance(import_stmt.path, RelativeImportPath):
                    continue  # skip import from relative paths.

                if isinstance(import_stmt, ImportFrom) and isinstance(import_stmt.targets, ImportAll):
                    continue  # skip import all

                self.classes.add_import(import_stmt)

        # import the methods
        for function in methods.functions:
            dynamic = DynamicDef.from_def(function)
            parser = self.get_function_parser(dynamic)

            if parser is None:
                # simple function case (not attached to a class)
                self.classes.statements.append(EmptyLine())
                self.classes.statements.append(dynamic.to_def())

            try:
                for class_name, output_function in parser.build():
                    self.store_method(class_name, output_function)

            except Warning as w:
                if w.args:
                    print(w)
                continue

        # import the constants.
        for assign in methods.assigns:
            if isinstance(assign.target, Variable):
                if str(assign.target).isupper():
                    self.classes.statements.append(EmptyLine())
                    self.classes.statements.append(assign)
