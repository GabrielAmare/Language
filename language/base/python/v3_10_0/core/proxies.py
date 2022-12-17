from __future__ import annotations

import abc
import dataclasses
import functools
import typing

from .configs import *
from .factories import *
from .helpers import *
from .models import *
from .pep import *

T = typing.TypeVar('T')

__all__ = [
    'Proxy',
    'StatementProxy',
    'SwitchProxy',
    'Container',
    'Contained',
    'BlockProxy',
    'ModuleProxy',
    'ClassProxy',
    'ParamProxy',
    'FunctionProxy',
]


@dataclasses.dataclass
class Proxy(typing.Generic[T], abc.ABC):
    @abc.abstractmethod
    def render(self) -> T:
        pass


def render(obj: Proxy[T] | T) -> T:
    if isinstance(obj, Proxy):
        return obj.render()
    else:
        return obj


@dataclasses.dataclass
class StatementProxy(Proxy[Statement], abc.ABC):
    pass


@dataclasses.dataclass
class Container(abc.ABC):
    _parts: list[Proxy[Statement] | Statement]
    
    @functools.cached_property
    @abc.abstractmethod
    def imports(self) -> ImportsHelper:
        pass
    
    @functools.cached_property
    @abc.abstractmethod
    def typing(self) -> TypingHelper:
        pass
    
    def _render_parts(self) -> typing.Iterator[Statement]:
        yield from map(render, self._parts)
    
    def CLASS(self, name: str) -> ClassProxy:  # NOQA
        sub_ctx = ClassProxy(root=self, name=name, _parts=[])
        self._parts.append(sub_ctx)
        return sub_ctx
    
    def FUNCTION(self, name: str) -> FunctionProxy:  # NOQA
        sub_ctx = FunctionProxy(root=self, name=name, _parts=[])
        self._parts.append(sub_ctx)
        return sub_ctx
    
    def SWITCH(self) -> SwitchProxy:  # NOQA
        proxy = SwitchProxy(root=self, _cases=[], _default=None)
        self._parts.append(proxy)
        return proxy
    
    def IF(self, test: Expression) -> BlockProxy:  # NOQA
        proxy = IfProxy(root=self, test=test, block_proxy=BlockProxy(root=self, _parts=[]))
        self._parts.append(proxy)
        return proxy.block_proxy
    
    def FOR(self, args: list[Variable], iter: Expression) -> BlockProxy:  # NOQA
        proxy = ForProxy(root=self, args=args, iter=iter, block_proxy=BlockProxy(root=self, _parts=[]))
        self._parts.append(proxy)
        return proxy.block_proxy
    
    def METHOD(self, name: str) -> FunctionProxy:  # NOQA
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
        self._parts.append(Raise(exc=render(exc), cause=render(cause)))

    def ASSIGN(self, name: str, type_: Expression | None = None, value: Expression | None = None) -> None:  # NOQA
        self._parts.append(Assign(target=Variable(name), type=type_, value=value))


@dataclasses.dataclass
class Contained:
    root: Container
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    @functools.cached_property
    def imports(self) -> ImportsHelper:
        return self.root.imports
    
    @functools.cached_property
    def typing(self) -> TypingHelper:
        return self.root.typing


@dataclasses.dataclass
class SwitchProxy(StatementProxy, Contained):
    _cases: list[tuple[Expression, BlockProxy]]
    _default: BlockProxy | None
    
    def render(self) -> If:
        if isinstance(self._default, BlockProxy):
            alt = Else(block=self._default.render())
        else:
            alt = None
        
        for test, block_proxy in reversed(self._cases[1:]):
            alt = Elif(test=test, block=block_proxy.render(), alt=alt)
        
        test, block_proxy = self._cases[0]
        return If(test=test, block=block_proxy.render(), alt=alt)
    
    def IF(self, test: Expression) -> BlockProxy:  # NOQA
        proxy = BlockProxy(root=self.root, _parts=[])
        self._cases.append((test, proxy))
        return proxy
    
    def ELSE(self) -> BlockProxy:  # NOQA
        proxy = BlockProxy(root=self.root, _parts=[])
        self._default = proxy
        return proxy


@dataclasses.dataclass
class BlockProxy(Proxy[Block], Contained, Container):
    def render(self) -> Block:
        return block(statements=self._render_parts())


@dataclasses.dataclass
class ModuleProxy(Proxy[Module], Container):
    env: Environment = None
    
    @functools.cached_property
    def imports(self) -> ImportsHelper:
        return ImportsHelper(env=self.env)
    
    @functools.cached_property
    def typing(self) -> TypingHelper:
        return TypingHelper(env=self.env, imports=self.imports)
    
    def render(self) -> Module:
        body_statements = list(self._render_parts())
        import_statements = list(self.imports.i_statements)
        return Module(statements=list(pep8_e302((
            *import_statements,
            *body_statements,
        ))))


@dataclasses.dataclass
class ClassProxy(StatementProxy, Contained, Container):
    root: Container = None
    name: str = None
    _mro: list[Expression] = dataclasses.field(default_factory=list)
    _decorators: list[Expression] = dataclasses.field(default_factory=list)
    
    def decorate(self, expr: Expression) -> None:
        self._decorators.append(expr)
    
    def inherits(self, *supers: Expression) -> None:
        self._mro.extend(supers)
    
    def render(self) -> DecoratorGR:
        result = Class(
            name=Variable(self.name),
            mro=self._mro,
            block=block(pep8_e301(self._render_parts()))
        )
        
        for decorator in self._decorators:
            result = Decorator(expr=decorator, target=result)
        
        return result


@dataclasses.dataclass
class IfProxy(StatementProxy, Contained):
    test: Expression
    block_proxy: BlockProxy
    
    def render(self) -> If:
        return If(
            test=self.test,
            block=render(self.block_proxy)
        )


@dataclasses.dataclass
class ForProxy(StatementProxy, Contained):
    args: list[Variable]
    iter: Expression
    block_proxy: BlockProxy
    
    def render(self) -> For:
        return For(
            args=self.args,
            iter=self.iter,
            block=render(self.block_proxy)
        )


@dataclasses.dataclass
class ParamProxy(Proxy[Param]):
    _name: str
    _type: Expression | None = None
    _default: Expression | None = None
    
    def type(self, __type: type | Expression) -> ParamProxy:
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
    
    def render(self) -> Param:
        return Param(name=Variable(self._name), type=self._type, default=self._default)


@dataclasses.dataclass
class FunctionProxy(StatementProxy, Contained, Container):
    root: Container = None
    name: str = None
    _params: list[ParamProxy] = dataclasses.field(default_factory=list)
    _returns: Expression | None = None
    _decorators: list[Expression] = dataclasses.field(default_factory=list)
    
    def decorate(self, expr: Expression) -> None:
        self._decorators.append(expr)
    
    def param(self, name: str) -> ParamProxy:
        proxy = ParamProxy(name)
        self._params.append(proxy)
        return proxy
    
    def returns(self, expr: Expression) -> None:
        self._returns = expr
    
    def render(self) -> DecoratorGR:
        result = Function(
            name=Variable(self.name),
            args=list(map(render, self._params)),
            block=block(self._render_parts()),
            returns=self._returns,
        )
        
        for decorator in self._decorators:
            result = Decorator(expr=decorator, target=result)
        
        return result
