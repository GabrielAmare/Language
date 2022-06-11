from __future__ import annotations

import dataclasses
import typing

from .ImportManager import ImportManager
from .base import *

__all__ = [
    'DynamicModule'
]

_IMPORT_FUTURE_ANNOTATIONS = ImportFrom(
    path=AbsoluteImportPath([Variable("__future__")]),
    targets=ImportAliases(names=[Alias(name=Variable("annotations"))])
)


@dataclasses.dataclass
class DynamicModule:
    """
        Equivalent to a Module, but with convenient methods to dynamically change a module.

        >>> module: Module = ...
        >>> dynamic_module = DynamicModule.from_module(module, version=...)
        >>> ... # apply your changes on the dynamic module
        >>> module = dynamic_module.to_module()
    """
    version: tuple[int, int, int]
    docstring: typing.Optional[str] = None
    statements: list[Statement] = dataclasses.field(default_factory=list)
    _imports: ImportManager = dataclasses.field(default_factory=ImportManager)
    import_future_annotations: bool = False
    build_all_list: bool = True

    def add_import(self, statement: ImportGR) -> None:
        self._imports.include_stmt(statement)

    def get_imports(self) -> typing.Iterator[ImportGR]:
        yield from self._imports.get_all()

    @classmethod
    def from_module(cls, module: Module, version: tuple[int, int, int]) -> 'DynamicModule':
        """Return the Docstring, Imports and Body of a module separately."""
        self = cls(version=version)

        for index, statement in enumerate(module.statements):
            if index == 0 and isinstance(statement, StatementExpr) and isinstance(statement.expr, String):
                self.docstring = statement.expr.to_str()

            elif statement == _IMPORT_FUTURE_ANNOTATIONS:
                self.import_future_annotations = True

            elif isinstance(statement, ImportGR):
                self.add_import(statement)

            elif isinstance(statement, EmptyLine):
                continue

            elif isinstance(statement, AnnAssign) and statement.target == Variable('__all__'):
                continue  # TODO : maybe keeps the __all__ defined in the module.

            else:
                self.statements.append(statement)

        return self

    def to_module(self) -> Module:
        return Module(statements=list(self._i_statements))

    def _all_definitions(self) -> AnnAssign:
        """Return the __all__ variable assign."""
        variables: typing.Set[Variable] = set()

        for statement in self.statements:
            if isinstance(statement, Class):
                variables.add(statement.name)

            elif isinstance(statement, Def):
                variables.add(statement.name)

            elif isinstance(statement, AnnAssign):
                if isinstance(statement.target, Variable):
                    variables.add(statement.target)

                elif isinstance(statement.target, Tuple):
                    for target in statement.target.items:
                        if isinstance(target, Variable):
                            variables.add(target)

                else:
                    continue

            else:
                continue

        exports = sorted([
            String(content=repr(variable.content))
            for variable in variables
            if not variable.content.startswith('_')
        ], key=lambda s: s.content)

        return AnnAssign(
            target=Variable("__all__"),
            value=IndentedList(IndentedExprEnum(exports))
        )

    @property
    def _i_statements(self) -> typing.Iterator[Statement]:
        if self.docstring:
            if '\n' in self.docstring:
                yield String.ml_docstring(self.docstring)
            else:
                yield String.sl_docstring(self.docstring)

        if self.import_future_annotations:
            yield _IMPORT_FUTURE_ANNOTATIONS
            yield EmptyLine()

        absolute_imports = self._imports.get_absolute_imports()
        if absolute_imports:
            for statement in sorted(absolute_imports, key=Import.order):
                yield statement
            yield EmptyLine()

        relative_imports = self._imports.get_relative_imports()
        if relative_imports:
            for statement in sorted(relative_imports, key=ImportFrom.order):
                yield statement
            yield EmptyLine()

        if self.build_all_list:
            yield self._all_definitions()

        for statement in self.statements:
            if isinstance(statement, (Class, Def)):
                # PEP8(E305) : Expected 2 blank lines after end of function or class
                yield EmptyLine()
                yield EmptyLine()
            yield statement

        # a module must always end with an empty line.
        yield EmptyLine()

    @property
    def functions(self) -> list[Def]:
        return [
            statement
            for statement in self.statements
            if isinstance(statement, Def)
        ]

    @property
    def methods(self) -> list[Def]:
        return [
            function
            for function in self.functions
            if function.is_method()
        ]

    @property
    def classes(self) -> list[Class]:
        return [
            statement
            for statement in self.statements
            if isinstance(statement, Class)
        ]

    @property
    def assigns(self) -> list[AnnAssign]:
        return [
            statement
            for statement in self.statements
            if isinstance(statement, AnnAssign)
        ]

    def get_class(self, name: Variable) -> Class | None:
        """Return the corresponding class if it exists, defaults to None."""
        for cls in self.classes:
            if cls.name == name:
                return cls

    def get_function(self, name: Variable) -> Def | None:
        """Return the corresponding class if it exists, defaults to None."""
        for function in self.functions:
            if function.name == name:
                return function

    def imports(self, path: str, name: str = None, as_name: str = None) -> Primary:
        return self._imports.include(path, name, as_name)

    def imports_all(self, path: str) -> None:
        self._imports.include_all(path)

    def duck_type_list(self, expr: Expression) -> Primary:
        """Return the duck-type for a list of `expr`."""
        if self.version >= (3, 9, 0):
            return Variable('list').subscript(expr)

        if self.version >= (3, 5, 0):
            return self.imports('typing').getattr('List').subscript(expr)

        raise ValueError("No way to duck type a list before `python_3_5_0` !")

    def duck_type_union(self, args: list[BitwiseXorGR]) -> BitwiseOrGR:
        """Return the duck-type for a list of `expr`."""
        if self.version >= (3, 9, 0):
            return BitwiseOr.from_list(args)

        if self.version >= (3, 5, 0):
            return self.imports('typing').getattr('Union').subscript(ExprEnum(args))

        raise ValueError("No way to duck type unions before `python_3_5_0` !")

    def duck_type_iterator(self, expr: Expression) -> Expression:
        """Return the duck-type for a list of `expr`."""
        if self.version >= (3, 9, 0):
            return self.imports('collections.abc').getattr('Iterator').subscript(expr)

        if self.version >= (3, 5, 0):
            return self.imports('typing').getattr('Iterator').subscript(expr)

        raise ValueError("No way to duck type an iterator before `python_3_5_0` !")

    def duck_type_optional(self, expr: BitwiseOrGR) -> Expression:
        """Return the duck-type for a list of `expr`."""
        if self.version >= (3, 9, 0):
            return BitwiseOr(expr, NONE)

        if self.version >= (3, 5, 0):
            return self.imports('typing').getattr('Optional').subscript(expr)

        raise ValueError("No way to duck type an iterator before `python_3_5_0` !")

    def make_duck_type(self, types: list[Variable]) -> typing.Optional[BitwiseOrGR]:
        """
        Make duck typing for a given list of types while including the imports required to make the duck typing.
        :param types: the list of types to resume into duck typing.
        :return: the duck typing corresponding to the list of types.
        """
        if not types:
            return NONE

        if len(types) == 1:
            return types[0]

        return self.duck_type_union(types)

    def make_annotation(self, name: Variable, type_: BitwiseOrGR, optional: bool, multiple: bool) -> AnnAssign:
        """
        Create an annotation for a class while including the imports required to create the annotation.
        :param name: the name of the attribute.
        :param type_: the type of the attribute.
        :param optional: is the attribute optional ? (default value will be None in this case)
        :param multiple: is the attribute multiple ? (a list of the given type)
        :return: the correct attribute annotation
        """
        if multiple:
            type_ = self.duck_type_list(type_)

        expr = None

        if optional:
            type_ = self.duck_type_optional(type_)
            expr = NoneClass()

        return AnnAssign(target=name, annotation=type_, value=expr)
