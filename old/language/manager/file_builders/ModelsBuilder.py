import dataclasses
import functools
import typing

from website.language import python as py, bnf, classmodule as cm
from ._abc import TextBuilder
from .part_builders import *
from ..constants import OPTIONS as OPT

__all__ = [
    'ModelsBuilder'
]


class LEX:
    FROZEN = py.Variable("frozen")
    ORDER = py.Variable("order")


@dataclasses.dataclass
class ModelsBuilder(TextBuilder):
    reader: bnf.Reader
    ctx: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.reader = self.reader.simplify(literals=True, aliases=True)

    @functools.cached_property
    def graph(self) -> cm.Graph:
        """Return the Graph associated with `self.reader_proxy`. Also optimize it before returning."""
        return cm.Graph.from_reader(self.reader)

    @functools.cached_property
    def models(self) -> py.DynamicModule:
        """Return the module where the models are stored."""
        return py.DynamicModule(
            docstring=('This module has been auto-generated. Do not change manually.\n'
                       'WARNING : Manual changes to this file are likely to be overwritten.'),
            import_future_annotations=True,
            version=self.config.python_version
        )

    @functools.cached_property
    def builders(self) -> list[Builder]:
        result = []
        if self.option(OPT.MODELS_DATACLASS) or self.option(OPT.MODELS_ANNOTATIONS, default=True):
            # builds the class annotations.
            builder = AnnotationsBuilder(config=self.config, graph=self.graph, module=self.models)
            result.append(builder)

        if self.option(OPT.MODELS_STR, default=True):
            # build the __istr__ and __str__ methods.
            builder = StrBuilder(config=self.config, graph=self.graph, module=self.models)
            result.append(builder)

        if self.option(OPT.MODELS_PARSE, default=True):
            # build the parse method that turn Element into correct instances.
            builder = ParseBuilder(config=self.config, graph=self.graph, module=self.models)
            result.append(builder)

        return result

    def get_node_statements(self, node: cm.Node) -> list[py.Statement]:
        packs: list[list[py.Statement]] = [
            list(builder.statements_for(node))
            for builder in self.builders
        ]

        packs = [pack for pack in packs if pack]  # remove empty packs

        statements: list[py.Statement] = []

        for index, pack in enumerate(packs):
            if index:
                # noinspection PyTypeChecker
                statements.append(py.EmptyLine())
            statements.extend(pack)

        return statements

    def get_class_decorators(self) -> typing.Iterator[py.Decorator]:
        if self.option(OPT.MODELS_DATACLASS, default=True):
            args = []

            if self.option(OPT.MODELS_DATACLASS_FROZEN):
                args.append(LEX.FROZEN.as_call_arg(py.TRUE))

            if self.option(OPT.MODELS_DATACLASS_ORDER):
                args.append(LEX.ORDER.as_call_arg(py.TRUE))

            self.models.imports('dataclasses')
            expr = py.DATACLASSES.DATACLASS

            if args:
                expr = expr.call(*args)

            yield py.Decorator(expr)

    def _label_for_class(self, __type: bnf.Variable) -> str:
        if not self.reader.has(__type):
            return 'undefined'

        target = self.reader.get(__type)

        if isinstance(target, bnf.Branch):
            return 'concrete'

        elif isinstance(target, bnf.Group):
            return 'abstract'

        elif isinstance(target, bnf.PatternGR):
            return 'atomic'

        else:
            raise TypeError(type(target))

    def convert_node(self, node: cm.Node) -> py.ClassGR:
        bases: list[py.Variable] = [py.Variable(base.content) for base in node.bases] if node.bases else []

        if isinstance(node.toplevel, bnf.Group):
            bases.append(self.models.imports('abc').getattr('ABC'))

            docstring = py.StatementExpr(expr=py.String.ml_docstring(
                "\n".join(
                    f">>> {sub_type!s}  # {self._label_for_class(sub_type)}"
                    for sub_type in node.toplevel.types
                ),
                level=0
            ))
        else:
            str_rule = str(node.toplevel).replace('\\', '\\\\')
            max_size = 120
            available = max_size - 8
            if len(str_rule) > available:
                str_rule = str_rule[:available - 1] + '…'
            docstring = py.StatementExpr(
                expr=py.String.ml_docstring(
                    f"This class has been generated automatically from the bnf rule :\n"
                    f"    {str_rule}", level=0
                )
            )
        statements = self.get_node_statements(node)
        return py.Class(
            decorators=list(self.get_class_decorators()),
            name=py.Variable(node.type.content),
            mro=py.Args(sorted(bases, key=str)) if bases else None,  # TODO : Improve sorting using mro info.
            block=py.Block(statements=[docstring, *statements]),
        )

    def build(self) -> py.DynamicModule:
        nodes = sorted(self.graph.nodes, key=cm.Node.order)
        module_statements = [
            self.convert_node(node)
            for node in nodes
        ]

        requirements = []

        for builder in self.builders:
            builder.include_requirements(requirements)

        self.models.statements.extend(requirements)

        self.models.statements.extend(module_statements)

        return self.models
