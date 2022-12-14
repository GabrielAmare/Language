import dataclasses
import typing

from .configs import Environment
from .linting import LintRule
from .models import *

__all__ = [
    'ImportsHelper',
    'TypingHelper',
]


@dataclasses.dataclass
class ImportsHelper:
    env: Environment
    _definitions: dict[str, set[str]] = dataclasses.field(default_factory=dict)
    
    @staticmethod
    def _path_to_getattr(*parts: str) -> Primary:
        assert all(map(str.isidentifier, parts))
        ref = Variable(parts[0])
        for part in parts[1:]:
            ref = GetAttr(ref, Variable(part))
        return ref
    
    def _import_all_from(self, origin: str):
        self._definitions.setdefault(origin, set())
        self._definitions[origin].add('*')
    
    def _import_from(self, target: str, origin: str):
        if self.env.lint(LintRule.MODULE_NO_MIXED_IMPORTS):
            if '' in self._definitions and origin in self._definitions['']:
                raise ValueError("No mixed imports allowed with the given code style.")
        
        self._definitions.setdefault(origin, set())
        self._definitions[origin].add(target)
    
    def _import(self, origin: str) -> None:
        if self.env.lint(LintRule.MODULE_NO_MIXED_IMPORTS):
            if origin in self._definitions and self._definitions[origin]:
                raise ValueError("No mixed imports allowed with the given code style.")
        
        self._definitions.setdefault('', set())
        self._definitions[''].add(origin)
    
    def get_all(self, __from: str) -> None:
        """This function can be used to import all the content of the `__from` resource."""
        if self.env.lint(LintRule.MODULE_NO_IMPORT_ALL):
            raise ValueError("Cannot use the `from ... import *` syntax with the given code style.")
        
        self._import_from(target='*', origin=__from)
    
    def get(self, __target: str, /, *, from_: str = '') -> Primary:
        """This function can be used to import `__target` in the module."""
        if not from_:
            # import `__target` as a module.
            self._import(__target)
            return self._path_to_getattr(*__target.split('.'))
        
        if self.env.lint(LintRule.MODULE_NO_IMPORT_FROM):
            # import `from_` as a module from which we grab the `__target`.
            self._import(from_)
            return self._path_to_getattr(*from_.split('.'), *__target.split('.'))
        
        # import `__target` from the `from_`
        self._import_from(target=__target, origin=from_)
        assert __target.isidentifier()
        return self._path_to_getattr(__target)
    
    @property
    def i_statements(self) -> typing.Iterator[Statement]:
        builtin_imports_abs = []
        project_imports_abs = []
        builtin_imports_rel = []
        project_imports_rel = []
        
        for origin in self._definitions.keys():
            if origin != '':
                if self.env and origin in self.env.builtins:
                    builtin_imports_rel.append(origin)
                else:
                    project_imports_rel.append(origin)
        
        for origin in self._definitions.get('', []):
            if self.env and origin in self.env.builtins:
                builtin_imports_abs.append(origin)
            else:
                project_imports_abs.append(origin)
        
        def gen_rel_imports(origins: list[str]) -> typing.Iterator[Statement]:
            for origin in sorted(origins):
                targets = self._definitions[origin]
                yield ImportFrom(
                    origin=ImportPath(parts=list(map(Variable, origin.split('.')))),
                    targets=[
                        ImportPath(parts=[Variable(name)])
                        for name in sorted(targets)
                    ]
                )
        
        def gen_abs_imports(origins: list[str]) -> typing.Iterator[Statement]:
            for origin in sorted(origins):
                yield Import(targets=[
                    ImportPath(parts=list(map(Variable, origin.split('.'))))
                ])
        
        if builtin_imports_abs:
            yield from gen_abs_imports(builtin_imports_abs)
        if builtin_imports_rel:
            yield from gen_rel_imports(builtin_imports_rel)
        if (builtin_imports_abs or builtin_imports_rel) and (project_imports_abs or project_imports_rel):
            yield EMPTY_LINE
        if project_imports_abs:
            yield from gen_abs_imports(project_imports_abs)
        if project_imports_rel:
            yield from gen_rel_imports(project_imports_rel)


T = typing.TypeVar('T', bound=Expression)


def _cast(__type: type | T) -> T:
    if isinstance(__type, Expression):
        return __type
    elif __type is int:
        return Variable('int')
    elif __type is str:
        return Variable('str')
    elif __type is bool:
        return Variable('bool')
    elif __type is float:
        return Variable('float')
    else:
        raise TypeError(type(__type))


@dataclasses.dataclass
class TypingHelper:
    env: Environment
    imports: ImportsHelper
    
    def union(self, *types: type | BitwiseXorGR) -> BitwiseOrGR:
        types = tuple(map(_cast, types))
        
        if len(types) == 1:
            return types[0]
        
        if self.env.version >= (3, 10, 0):
            # https://peps.python.org/pep-0604/ : `A | B | ...` from python 3.10
            result = None
            for _type in types:
                if result is None:
                    result = _type
                else:
                    result = BitwiseOr(left=result, right=_type)
            return result
        
        return GetItem(self.imports.get('Union', from_='typing'), list(types))
    
    def list(self, expr: type | Expression) -> GetItem:
        expr = _cast(expr)
        
        if self.env.version >= (3, 9, 0):
            # https://peps.python.org/pep-0585/ : `list[...]` from python 3.9
            return GetItem(left=Variable('list'), items=[expr])
        
        return GetItem(self.imports.get('List', from_='typing'), [expr])
    
    def set(self, expr: type | Expression) -> GetItem:
        expr = _cast(expr)
        
        if self.env.version >= (3, 9, 0):
            # https://peps.python.org/pep-0585/ : `set[...]` from python 3.9
            return GetItem(Variable('set'), [expr])
        
        return GetItem(self.imports.get('Set', from_='typing'), [expr])
    
    def frozenset(self, expr: type | Expression) -> GetItem:
        expr = _cast(expr)
        
        if self.env.version >= (3, 9, 0):
            # https://peps.python.org/pep-0585/ : `frozenset[...]` from python 3.9
            return GetItem(Variable('frozenset'), [expr])
        
        return GetItem(self.imports.get('Frozenset', from_='typing'), [expr])
    
    def tuple(self, *types: type | Expression) -> GetItem:
        types = tuple(map(_cast, types))
        
        if self.env.version >= (3, 9, 0):
            # https://peps.python.org/pep-0585/ : `tuple[T, ...]` from python 3.9
            return GetItem(Variable('tuple'), [*types])
        
        return GetItem(self.imports.get('Tuple', from_='typing'), [*types])
    
    def optional(self, expr: type | Expression) -> Expression:
        expr = _cast(expr)
        
        if self.env.version >= (3, 10, 0):
            # https://peps.python.org/pep-0604/ : `... | None` from python 3.10
            return BitwiseOr(left=expr, right=NONE)
        
        return GetItem(self.imports.get('Optional', from_='typing'), [expr])
    
    def iterator(self, expr: type | Expression) -> GetItem:
        expr = _cast(expr)
        
        return GetItem(self.imports.get('Iterator', from_='typing'), [expr])
    
    def generic(self, *expressions: Expression) -> GetItem:
        return GetItem(
            left=self.imports.get('Generic', from_='typing'),
            items=list(expressions)
        )
    
    def type_var(self, variable: Variable, bound: Expression | None = None) -> Assign:
        args = [String(repr(str(variable)))]
        
        if bound is not None:
            args.append(Kwarg(name=Variable('bound'), value=bound))
        
        return Assign(target=variable, value=Call(left=self.imports.get('TypeVar', from_='typing'), args=args))
