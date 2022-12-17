from __future__ import annotations

import abc
import dataclasses
import functools
import os.path
import typing

from .configs import *
from .factories import *
from .helpers import *
from .models import *
from .pep import *

__all__ = [
    'Environment',
    'DynamicPackage',
    'Contained',
    'Container',
    'DynamicModule',
    'DynamicClass',
    'DynamicFunction',
]


def _indent(text: str, prefix: str = '    ') -> str:
    return '\n'.join(prefix + line for line in text.split('\n'))


def _get_definition_name(statement: DecoratorGR | Assign) -> str | None:
    if isinstance(statement, Assign):
        if isinstance(statement.target, Variable):
            return str(statement.target)
        else:
            return None
    elif isinstance(statement, (Class, Function)):
        return str(statement.name)
    elif isinstance(statement, Decorator):
        return _get_definition_name(statement.target)
    else:
        raise NotImplementedError


@dataclasses.dataclass
class DynamicPackage:
    """Representation of a python package."""
    name: str
    env: Environment | None = None
    _modules: dict[str, DynamicModule] = dataclasses.field(default_factory=dict)
    
    def new_module(self, name: str) -> DynamicModule:
        """Create a new module in the package."""
        assert name.isidentifier()
        assert name not in self._modules, f"The module {name!r} already exists in the package."
        module = DynamicModule(parent=self, name=name)
        self._modules[name] = module
        return module
    
    def save(self, root: str = '.') -> None:
        assert os.path.exists(root)
        assert os.path.isdir(root)
        
        path = os.path.join(root, self.name)
        
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise NotADirectoryError(path)
        else:
            os.mkdir(path)
        
        for module in self._modules.values():
            module.save(path)


T = typing.TypeVar('T')


@dataclasses.dataclass
class Contained(typing.Generic[T], abc.ABC):
    parent: T | None = None
    
    @property
    def env(self) -> Environment | None:
        if self.parent is None:
            return
        
        return self.parent.env


@dataclasses.dataclass
class Container(abc.ABC):
    name: str
    _names: list[str] = dataclasses.field(default_factory=list)
    _attrs: list[DynamicClass | DynamicFunction | Assign] = dataclasses.field(default_factory=list)
    
    def new_class(self, name: str) -> DynamicClass:
        """Create a new class in the container."""
        assert name.isidentifier()
        assert name not in self._names, f"{name!r} already exists in the container."
        attr = DynamicClass(parent=self, name=name)
        self._names.append(name)
        self._attrs.append(attr)
        return attr
    
    def new_function(self, name: str) -> DynamicFunction:
        """Create a new function in the container."""
        assert name.isidentifier()
        assert name not in self._names, f"{name!r} already exists in the container."
        attr = DynamicFunction(parent=self, name=name)
        self._names.append(name)
        self._attrs.append(attr)
        return attr
    
    def new_variable(self, name: str, value: Expression, type_: Expression | None = None):
        self._names.append(name)
        self._attrs.append(Assign(target=Variable(name), type=type_, value=value))
    
    def _body_statements(self) -> typing.Iterator[Statement]:
        for attr in self._attrs:
            if isinstance(attr, Assign):
                yield attr
            elif isinstance(attr, (DynamicFunction, DynamicClass)):
                yield attr.build()
            else:
                raise NotImplementedError


@dataclasses.dataclass
class DynamicModule(Contained[DynamicPackage], Container):
    """Representation of a python module."""
    _future_imports: set[str] = dataclasses.field(default_factory=set)
    _imports: list[ImportStatement] = dataclasses.field(default_factory=list)
    _import_statements: list[Statement] = dataclasses.field(default_factory=list)
    _docstring: str = ''
    
    @functools.cached_property
    def imports(self) -> ImportsHelper:
        return ImportsHelper(env=self.env)
    
    @functools.cached_property
    def typing(self) -> TypingHelper:
        return TypingHelper(env=self.env, imports=self.imports)
    
    def add_docstring(self, value: str) -> DynamicModule:
        self._docstring = value
        return self
    
    def future_import(self, name: str) -> DynamicModule:
        """Add a future import to the module."""
        self._future_imports.add(name)
        return self
    
    def add_imports(self, statements: typing.Iterator[Statement]) -> DynamicModule:
        self._import_statements.extend(statements)
        return self
    
    def _statements(self) -> typing.Iterator[Statement]:
        body_statements = list(self._body_statements())
        
        if self._future_imports:
            yield ImportFrom(
                origin=ImportPath(parts=[Variable('__future__')]),
                targets=[
                    ImportPath(parts=[Variable(name)])
                    for name in sorted(self._future_imports)
                ]
            )
        
        if self._docstring:
            yield String('"""\n' + _indent(self._docstring) + '\n"""')
        
        yield from self.imports.i_statements
        
        if self._names:
            yield Assign(
                target=Variable('__all__'),
                value=indented_list(*map(atom, sorted(filter(lambda name: not name.startswith('_'), self._names))))
            )
        
        yield from body_statements
    
    def build(self) -> Module:
        return Module(statements=list(pep8_e302(self._statements())))
    
    def save(self, root: str) -> None:
        assert os.path.exists(root)
        assert os.path.isdir(root)
        
        path = os.path.join(root, self.name + '.py')
        
        # if os.path.exists(path):
        #     if input(f'Allow to overwrite {path!r} ? (Y/N)') != 'Y':
        #         raise FileExistsError(path)
        
        with open(path, mode="w", encoding="utf-8") as file:
            file.write(str(self.build()))


@dataclasses.dataclass
class DynamicClass(Contained[Container], Container):
    """Representation of a python class."""
    mro: list[Expression] = dataclasses.field(default_factory=list)
    decorators: list[Expression] = dataclasses.field(default_factory=list)
    is_abstract: bool = False
    
    def add_super(self, value: Expression) -> DynamicClass:
        self.mro.append(value)
        return self
    
    def add_supers(self, values: typing.Iterator[Expression]) -> DynamicClass:
        self.mro.extend(values)
        return self
    
    def add_decorator(self, expression: Expression) -> DynamicClass:
        self.decorators.append(expression)
        return self
    
    def build(self) -> Class:
        result = Class(
            name=Variable(self.name),
            mro=self.mro,
            block=block(pep8_e301(self._body_statements()))
        )
        
        for expression in self.decorators:
            result = Decorator(expr=expression, target=result)
        
        return result


@dataclasses.dataclass
class DynamicFunction(Contained[Container], Container):
    """Representation of a python function."""
    params: list[ParamGR] = dataclasses.field(default_factory=list)
    statements: list[Statement] = dataclasses.field(default_factory=list)  # BUG : mixin with inner definition :/
    decorators: list[Expression] = dataclasses.field(default_factory=list)
    returns: Expression | None = None
    
    def set_returns(self, value: Expression | None) -> DynamicFunction:
        self.returns = value
        return self
    
    def add_param(self, name: str, type_: Expression | None = None,
                  default: Expression | None = None) -> DynamicFunction:
        self.params.append(Param(name=Variable(name), type=type_, default=default))
        return self
    
    def add_statement(self, statement: Statement) -> DynamicFunction:
        self.statements.append(statement)
        return self
    
    def add_statements(self, statements: typing.Iterator[Statement]) -> DynamicFunction:
        self.statements.extend(statements)
        return self
    
    def add_decorator(self, expression: Expression) -> DynamicFunction:
        self.decorators.append(expression)
        return self
    
    def build(self) -> Function:
        params = list(sorted(self.params, key=lambda param: (
                param.default is not None  # params with default value are put in the end.
        )))
        
        result = Function(
            name=Variable(self.name),
            args=params,
            block=block(self.statements),
            returns=self.returns
        )
        
        for expression in self.decorators:
            result = Decorator(expr=expression, target=result)
        
        return result
