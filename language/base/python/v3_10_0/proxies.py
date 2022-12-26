from __future__ import annotations

import abc
import dataclasses
import functools
import os
import typing

from .configs import *
from .factories import *
from .helpers import *
from .models import *
from .pep import *

T = typing.TypeVar('T')

__all__ = [
    'Builder',
    'StatementBuilder',
    'SwitchProxy',
    'Container',
    'Contained',
    'BlockBuilder',
    'ModuleBuilder',
    'ClassBuilder',
    'ParamBuilder',
    'FunctionBuilder',
    'HasPythonImplementation',
    'Package',
]


class Resource(abc.ABC):
    name: str
    
    @abc.abstractmethod
    def save(self, root: str) -> None:
        pass


class Context:
    __opened: list[Context] = []
    
    def __enter__(self):
        Context.__opened.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        Context.__opened.pop(-1)


@dataclasses.dataclass
class Package(Context, Resource):
    name: str
    env: Environment
    resources: dict[str, Resource] = dataclasses.field(default_factory=dict)
    
    def save(self, root: str = os.curdir) -> None:
        path: str = os.path.join(root, self.name)
        if not os.path.exists(path):
            os.mkdir(path)
        
        assert os.path.isdir(path)
        for resource in self.resources.values():
            resource.save(root=path)
    
    def MODULE(self, name: str) -> ModuleBuilder:  # NOQA
        assert name not in self.resources
        module = ModuleBuilder(name=name, env=self.env, _parts=[])
        self.resources[name] = module
        return module
    
    def PACKAGE(self, name: str) -> Package:  # NOQA
        assert name not in self.resources
        package = Package(name=name, env=self.env)
        self.resources[name] = package
        return package


@dataclasses.dataclass
class Builder(typing.Generic[T], abc.ABC):
    @abc.abstractmethod
    def build(self) -> T:
        pass


def build(obj: Builder[T] | T) -> T:
    if isinstance(obj, Builder):
        return obj.build()
    else:
        return obj


@dataclasses.dataclass
class StatementBuilder(Builder[Statement], abc.ABC):
    pass


@dataclasses.dataclass
class Container(Context, abc.ABC):
    _parts: list[Builder[Statement] | Statement]
    
    @functools.cached_property
    @abc.abstractmethod
    def imports(self) -> ImportsHelper:
        pass
    
    @functools.cached_property
    @abc.abstractmethod
    def typing(self) -> TypingHelper:
        pass
    
    def _render_parts(self) -> typing.Iterator[Statement]:
        yield from map(build, self._parts)
    
    def CLASS(self, name: str) -> ClassBuilder:  # NOQA
        sub_ctx = ClassBuilder(root=self, name=name, _parts=[])
        self._parts.append(sub_ctx)
        return sub_ctx
    
    def FUNCTION(self, name: str) -> FunctionBuilder:  # NOQA
        sub_ctx = FunctionBuilder(root=self, name=name, _parts=[])
        self._parts.append(sub_ctx)
        return sub_ctx
    
    def SWITCH(self) -> SwitchProxy:  # NOQA
        proxy = SwitchProxy(root=self, _cases=[], _default=None)
        self._parts.append(proxy)
        return proxy
    
    def IF(self, test: Expression) -> BlockBuilder:  # NOQA
        proxy = IfBuilder(root=self, test=test, block_proxy=BlockBuilder(root=self, _parts=[]))
        self._parts.append(proxy)
        return proxy.block_proxy
    
    def FOR(self, args: list[Variable], iter: Expression) -> BlockBuilder:  # NOQA
        proxy = ForBuilder(root=self, args=args, iter=iter, block_proxy=BlockBuilder(root=self, _parts=[]))
        self._parts.append(proxy)
        return proxy.block_proxy
    
    def METHOD(self, name: str) -> FunctionBuilder:  # NOQA
        sub_ctx = self.FUNCTION(name)
        sub_ctx.param('self')
        return sub_ctx
    
    def YIELD(self, *expressions: Expression) -> None:  # NOQA
        self._parts.append(Yield(expressions=list(expressions)))
    
    def YIELD_FROM(self, expression: Expression) -> None:  # NOQA
        self._parts.append(YieldFrom(expr=expression))
    
    def RETURN(self, *expressions: Expression) -> None:  # NOQA
        self._parts.append(Return(expressions=list(expressions)))
    
    def RAISE(self, exc: Expression, cause: Expression | None = None) -> None:  # NOQA
        self._parts.append(Raise(exc=build(exc), cause=build(cause)))
    
    def ASSIGN(self, name: str, type_: Expression | None = None, value: Expression | None = None) -> None:  # NOQA
        self._parts.append(Assign(target=Variable(name), type=type_, value=value))
    
    def STATEMENT(self, stmt: Statement) -> None:  # NOQA
        self._parts.append(stmt)
    
    def __iadd__(self, stmt: Statement):
        self._parts.append(stmt)
        return self
    
    def implement(self, obj: HasPythonImplementation) -> None:
        return obj.implement_in(self)


@dataclasses.dataclass
class Contained:
    root: Container
    
    @functools.cached_property
    def imports(self) -> ImportsHelper:
        return self.root.imports
    
    @functools.cached_property
    def typing(self) -> TypingHelper:
        return self.root.typing


@dataclasses.dataclass
class SwitchProxy(StatementBuilder, Contained, Context):
    _cases: list[tuple[Expression, BlockBuilder]]
    _default: BlockBuilder | None
    
    def build(self) -> If:
        if isinstance(self._default, BlockBuilder):
            alt = Else(block=self._default.build())
        else:
            alt = None
        
        for test, block_proxy in reversed(self._cases[1:]):
            alt = Elif(test=test, block=block_proxy.build(), alt=alt)
        
        test, block_proxy = self._cases[0]
        return If(test=test, block=block_proxy.build(), alt=alt)
    
    def IF(self, test: Expression) -> BlockBuilder:  # NOQA
        proxy = BlockBuilder(root=self.root, _parts=[])
        self._cases.append((test, proxy))
        return proxy
    
    def ELSE(self) -> BlockBuilder:  # NOQA
        proxy = BlockBuilder(root=self.root, _parts=[])
        self._default = proxy
        return proxy


@dataclasses.dataclass
class BlockBuilder(Builder[Block], Contained, Container):
    def build(self) -> Block:
        return block(statements=self._render_parts())


@dataclasses.dataclass
class ModuleBuilder(Builder[Module], Container, Resource):
    name: str
    env: Environment = None
    _future_imports: set[str] = dataclasses.field(default_factory=set)
    
    @functools.cached_property
    def imports(self) -> ImportsHelper:
        return ImportsHelper(env=self.env)
    
    @functools.cached_property
    def typing(self) -> TypingHelper:
        return TypingHelper(env=self.env, imports=self.imports)
    
    @property
    def _exports(self) -> list[str]:
        exports = []
        
        for part in self._parts:
            if isinstance(part, ClassBuilder):
                name = part.name
            elif isinstance(part, FunctionBuilder):
                name = part.name
            elif isinstance(part, Assign) and isinstance(part.target, Variable):
                name = part.target.content
            else:
                continue
            
            if not name.startswith('_'):
                exports.append(name)
        
        return list(sorted(set(exports)))
    
    def build(self) -> Module:
        statements = []
        if self._future_imports:
            statements.append(
                ImportFrom(
                    origin=ImportPath(parts=[Variable('__future__')]),
                    targets=[
                        ImportPath(parts=[Variable(name)])
                        for name in sorted(self._future_imports)
                    ]
                )
            )
        statements.extend(self.imports.i_statements)
        
        if exports := self._exports:
            statements.append(
                Assign(
                    target=Variable('__all__'),
                    value=indented_list(*map(atom, exports))
                )
            )
        
        statements.extend(self._render_parts())
        
        return Module(statements=list(pep8_e302(statements)))
    
    def save(self, root: str) -> None:
        filepath = os.path.join(root, self.name + '.py')
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(str(self.build()))
    
    def future_import(self, name: str) -> None:
        self._future_imports.add(name)


@dataclasses.dataclass
class ClassBuilder(StatementBuilder, Contained, Container):
    root: Container = None
    name: str = None
    _mro: list[Expression] = dataclasses.field(default_factory=list)
    _decorators: list[Expression] = dataclasses.field(default_factory=list)
    
    def decorate(self, expr: Expression) -> None:
        self._decorators.append(expr)
    
    def inherits(self, *supers: Expression) -> None:
        self._mro.extend(supers)
    
    def build(self) -> DecoratorGR:
        result = Class(
            name=Variable(self.name),
            mro=self._mro,
            block=block(pep8_e301(self._render_parts()))
        )
        
        for decorator in self._decorators:
            result = Decorator(expr=decorator, target=result)
        
        return result


@dataclasses.dataclass
class IfBuilder(StatementBuilder, Contained):
    test: Expression
    block_proxy: BlockBuilder
    
    def build(self) -> If:
        return If(
            test=self.test,
            block=build(self.block_proxy)
        )


@dataclasses.dataclass
class ForBuilder(StatementBuilder, Contained):
    args: list[Variable]
    iter: Expression
    block_proxy: BlockBuilder
    
    def build(self) -> For:
        return For(
            args=self.args,
            iter=self.iter,
            block=build(self.block_proxy)
        )


@dataclasses.dataclass
class ParamBuilder(Builder[Param]):
    _name: str
    _type: Expression | None = None
    _default: Expression | None = None
    
    def type(self, __type: type | Expression) -> ParamBuilder:
        if __type is int:
            __type = Variable('int')
        elif __type is str:
            __type = Variable('str')
        elif __type is bool:
            __type = Variable('bool')
        elif __type is float:
            __type = Variable('float')
        elif isinstance(__type, Expression):
            pass
        else:
            raise ValueError(__type)
        self._type = __type
        return self
    
    def build(self) -> Param:
        return Param(name=Variable(self._name), type=self._type, default=self._default)


@dataclasses.dataclass
class FunctionBuilder(StatementBuilder, Contained, Container):
    root: Container = None
    name: str = None
    _params: list[ParamBuilder] = dataclasses.field(default_factory=list)
    _returns: Expression | None = None
    _decorators: list[Expression] = dataclasses.field(default_factory=list)
    
    def decorate(self, expr: Expression) -> None:
        self._decorators.append(expr)
    
    def param(self, name: str) -> ParamBuilder:
        proxy = ParamBuilder(name)
        self._params.append(proxy)
        return proxy
    
    def returns(self, expr: Expression) -> None:
        self._returns = expr
    
    def build(self) -> DecoratorGR:
        result = Function(
            name=Variable(self.name),
            args=list(map(build, self._params)),
            block=block(self._render_parts()),
            returns=self._returns,
        )
        
        for decorator in self._decorators:
            result = Decorator(expr=decorator, target=result)
        
        return result


class HasPythonImplementation(abc.ABC):
    @abc.abstractmethod
    def implement_in(self, scope: Container) -> None:
        """"""
