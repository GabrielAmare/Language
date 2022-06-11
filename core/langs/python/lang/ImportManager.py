import collections
import re
import typing

from .base import *

__all__ = [
    'ImportManager'
]

_ABSOLUTE_PATH_REGEX = re.compile(r"[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*")
_RELATIVE_PATH_REGEX = re.compile(r"\.+(?:[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*)?")


def _is_absolute_path(__value: str) -> bool:
    return bool(_ABSOLUTE_PATH_REGEX.match(__value))


def _is_relative_path(__value: str) -> bool:
    return bool(_RELATIVE_PATH_REGEX.match(__value))


def _is_path(__value: str) -> bool:
    return _is_absolute_path(__value) or _is_relative_path(__value)


def _get_target_from_path(path: str) -> Primary:
    assert _is_absolute_path(path)
    variables = list(map(Variable, path.split('.')))
    target = variables[-1]
    for var in reversed(variables[:-1]):
        target = GetAttr(left=var, right=target)
    return target


_RelativeImports = typing.DefaultDict[str, typing.Set[tuple[str, typing.Optional[str]]]]
_AbsoluteImports = typing.DefaultDict[str, typing.Set[typing.Optional[str]]]


class ImportManager:
    """Use this to handle clean imports."""

    def __init__(self):
        self._rel_imports: _RelativeImports = collections.defaultdict(set)
        self._abs_imports: _AbsoluteImports = collections.defaultdict(set)
        self._all_imports: typing.Set[str] = set()

    def include_all(self, path: str) -> None:
        assert _is_path(path)
        self._all_imports.add(path)

    def include(self, path: str, name: typing.Optional[str] = None, as_name: typing.Optional[str] = None) -> Primary:
        """Return the variable to import and include it into the imports."""
        assert as_name is None or as_name.isidentifier()

        if name is None:
            assert _is_absolute_path(path)
            if as_name is None:
                target = _get_target_from_path(path)
            else:
                assert as_name.isidentifier()
                target = Variable(as_name)
            self._abs_imports[path].add(as_name)
        else:
            assert _is_path(path), repr(path)
            assert name.isidentifier(), repr(name)
            if as_name is None:
                target = Variable(name)
            else:
                assert as_name.isidentifier()
                target = Variable(as_name)
            self._rel_imports[path].add((name, as_name))

        return target

    def include_stmt(self, stmt: ImportGR) -> None:
        if isinstance(stmt, ImportFrom):
            path = str(stmt.path)
            if isinstance(stmt.targets, ImportAll):
                self.include_all(path=path)
            elif isinstance(stmt.targets, ImportAliases):
                for alias in stmt.targets.names:
                    self.include(
                        path=path,
                        name=alias.name.content,
                        as_name=alias.as_name.content if alias.as_name else None
                    )
            else:
                raise NotImplementedError

        elif isinstance(stmt, Import):
            for dotted_as_name in stmt.targets:
                self.include(
                    path='.'.join(name.content for name in dotted_as_name.names),
                    name=None,
                    as_name=dotted_as_name.as_name.content if dotted_as_name.as_name else None
                )

        else:
            raise NotImplementedError

    def get_absolute_imports(self) -> list[Import]:
        return [
            Import(targets=[
                DottedAsName(
                    names=list(map(Variable, path.split('.'))),
                    as_name=Variable(as_name) if as_name else None
                )
            ])
            for path, values in self._abs_imports.items()
            for as_name in values  # should be warned when more than 1 item in as_names !
        ]

    def get_relative_imports(self) -> list[ImportFrom]:
        return [
            *(
                ImportFrom(
                    path=ImportPath.from_str(path),
                    targets=ImportAliases(names=sorted([
                        Alias(
                            name=Variable(name),
                            as_name=Variable(as_name) if as_name else None
                        )
                        for name, as_name in values
                    ], key=str))
                )
                for path, values in self._rel_imports.items()
            ),
            *(
                ImportFrom(
                    path=ImportPath.from_str(path),
                    targets=ImportAll()
                )
                for path in self._all_imports
            )
        ]

    def get_all(self) -> typing.Generator[ImportGR, None, None]:
        """Return the defined imports."""
        yield from self.get_absolute_imports()
        yield from self.get_relative_imports()
