import dataclasses
import functools
import typing

from core.builder import options
from core.langs import bnf
from core.langs.python import *
from ._abc import TextBuilder
from .parts import *

__all__ = [
    'ModelsBuilder'
]


class LEX:
    FROZEN = Variable("frozen")
    ORDER = Variable("order")


@dataclasses.dataclass
class ModelsBuilder(TextBuilder):
    reader: bnf.Reader
    ctx: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.reader = self.reader.simplify(literals=True, aliases=True)

    @functools.cached_property
    def graph(self) -> bnf.Graph:
        """Return the Graph associated with `self.reader_proxy`. Also optimize it before returning."""
        return bnf.Graph.from_reader(self.reader)

    @functools.cached_property
    def models(self) -> DynamicModule:
        """Return the module where the models are stored."""
        return DynamicModule(
            docstring=('This module has been auto-generated. Do not change manually.\n'
                       'WARNING : Manual changes to this file are likely to be overwritten.'),
            import_future_annotations=True,
            version=self.config.python_version
        )

    @functools.cached_property
    def builders(self) -> list[PartBuilder]:
        result = []
        if self.option(options.Models.DATACLASS) or self.option(options.Models.ANNOTATIONS, default=True):
            # builds the class annotations.
            builder = DataclassBuilder(config=self.config, graph=self.graph, module=self.models)
            result.append(builder)

        if self.option(options.Models.STR, default=True):
            # build the __istr__ and __str__ methods.
            builder = StrMethodBuilder(config=self.config, graph=self.graph, module=self.models)
            result.append(builder)

        if self.option(options.Models.PARSE, default=True):
            # build the parse method that turn Element into correct instances.
            builder = ParseMethodBuilder(config=self.config, graph=self.graph, module=self.models)
            result.append(builder)

        return result

    def get_node_statements(self, node: bnf.Node) -> list[Statement]:
        packs: list[list[Statement]] = [
            list(builder.statements_for(node))
            for builder in self.builders
        ]

        packs = [pack for pack in packs if pack]  # remove empty packs

        statements: list[Statement] = []

        for index, pack in enumerate(packs):
            if index:
                # noinspection PyTypeChecker
                statements.append(EmptyLine())
            statements.extend(pack)

        return statements

    def get_class_decorators(self) -> typing.Iterator[Decorator]:
        if self.option(options.Models.DATACLASS, default=True):
            args = []

            if self.option(options.Models.DATACLASS_FROZEN):
                args.append(LEX.FROZEN.as_call_arg(TRUE))

            if self.option(options.Models.DATACLASS_ORDER):
                args.append(LEX.ORDER.as_call_arg(TRUE))

            self.models.imports('dataclasses')
            expr = DATACLASSES.DATACLASS

            if args:
                expr = expr.call(*args)

            yield Decorator(expr)

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

    def convert_node(self, node: bnf.Node) -> ClassGR:
        bases: list[Primary] = [Variable(base.content) for base in node.bases] if node.bases else []

        if isinstance(node.toplevel, bnf.Group):
            bases.append(self.models.imports('abc').getattr('ABC'))

            docstring = StatementExpr(expr=String.ml_docstring(
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
            docstring = StatementExpr(
                expr=String.ml_docstring(
                    f"This class has been generated automatically from the bnf rule :\n"
                    f"    {str_rule}", level=0
                )
            )
        statements = self.get_node_statements(node)
        return Class(
            decorators=list(self.get_class_decorators()),
            name=Variable(node.type.content),
            mro=Args(sorted(bases, key=str)) if bases else None,  # TODO : Improve sorting using mro info.
            block=Block(statements=[docstring, *statements]),
        )

    def build(self) -> DynamicModule:
        nodes = sorted(self.graph.nodes, key=bnf.Node.order)
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
