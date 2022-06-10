from __future__ import annotations

import dataclasses
import typing

from website.language.python.lang.models import *
from .TypeSwitch import TypeSwitch

__all__ = [
    'DynamicDef'
]


@dataclasses.dataclass
class DynamicDef:
    name: Variable
    docstring: typing.Optional[str] = None
    rtype: typing.Optional[Expression] = None
    args: list[DefArgumentGR] = dataclasses.field(default_factory=list)
    statements: list[Statement] = dataclasses.field(default_factory=list)
    decorators: list[Decorator] = dataclasses.field(default_factory=list)

    @classmethod
    def from_def(cls, function: Def) -> DynamicDef:
        self = cls(
            name=function.name,
            args=function.args[:] if function.args else [],
            rtype=function.rtype,
            decorators=function.decorators[:] if function.decorators else [],
        )

        for index, statement in enumerate(function.block.statements):
            if index == 0 and isinstance(statement, StatementExpr) and isinstance(statement.expr, String):
                self.docstring = statement.expr.to_str()

            elif not isinstance(statement, EmptyLine):
                self.statements.append(statement)

        return self

    @property
    def _i_statements(self) -> typing.Iterator[Statement]:
        if self.docstring:
            if '\n' in self.docstring:
                yield String.ml_docstring(self.docstring)
            else:
                yield String.sl_docstring(self.docstring)

        yield from self.statements

    def to_def(self) -> Def:
        return Def(
            decorators=self.decorators or None,
            name=self.name,
            args=self.args or None,
            rtype=self.rtype or None,
            block=Block(statements=list(self._i_statements) or [PassClass()]),
        )

    def has_decorator(self, decorator: Decorator) -> bool:
        """Return True if `self` has the given `decorator`."""
        return decorator in self.decorators

    def add_decorator(self, decorator: Decorator) -> None:
        """Add the `decorator` to `self` (on top)."""
        self.decorators.insert(0, decorator)

    def remove_decorators(self, decorators: list[Decorator]) -> None:
        """Remove the given `decorators` from `self` if they are present."""
        self.decorators = [
            decorator
            for decorator in self.decorators
            if decorator not in decorators
        ]

    def is_type_switch(self) -> bool:
        if len(self.statements) != 1:
            return False

        return self.statements[0].is_type_switch()

    def as_type_switch(self) -> TypeSwitch:
        if len(self.statements) != 1:
            raise ValueError

        arg, types, cases, default = self.statements[0].as_type_switch()

        return TypeSwitch(
            arg=arg,
            types=types,
            cases=cases,
            default=default
        )

    def remove_empty_lines(self):
        self.statements = [statement for statement in self.statements if not isinstance(statement, EmptyLine)]
