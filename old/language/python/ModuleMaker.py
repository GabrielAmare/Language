import abc
import functools
import typing

from website.language.python.lang.models import *


class ModuleMaker(abc.ABC):
    docstring: str
    import_future_annotations: bool

    def get_docstring(self) -> Statement:
        """"""
        return StatementExpr(expr=String.ml_docstring(self.docstring))

    @abc.abstractmethod
    def get_import_statements(self) -> typing.Iterator[Statement]:
        """"""

    @abc.abstractmethod
    def get_all_exports(self) -> list[String]:
        """"""

    def get_head_statements(self) -> typing.Iterator[Statement]:
        """"""
        yield self.get_docstring()

        if self.import_future_annotations:
            yield ImportFrom(
                path=AbsoluteImportPath([Variable("__future__")]),
                targets=ImportAliases(names=[Alias(name=Variable("annotations"))])
            )
            yield EmptyLine()

        yield from self.get_import_statements()
        yield EmptyLine()

        yield AnnAssign(
            target=Variable("__all__"),
            value=IndentedList(IndentedExprEnum(sorted(self.get_all_exports(), key=lambda s: s.content)))
        )
        yield EmptyLine()

    @abc.abstractmethod
    def get_body_statements(self) -> typing.Iterator[Statement]:
        """"""

    @functools.cached_property
    def module(self) -> Module:
        """"""
        # the order is important here because we may want to define imports from the body statements !
        module_body = list(self.get_body_statements())
        module_head = list(self.get_head_statements())

        return Module(statements=module_head + module_body)
