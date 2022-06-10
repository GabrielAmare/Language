import dataclasses
import functools
import typing

import website.console
from website.language import python as py, classmodule as cm, bnf
from website.language.base.models import Attribute, Descriptor
from ._abc import Builder

__all__ = [
    'ParseBuilder'
]


class LEX:
    OBJ = py.Variable('obj')
    ITEM = py.Variable('item')
    DATA = py.Variable('data')
    PARSE = py.Variable('parse')


@dataclasses.dataclass
class ParseBuilder(Builder):
    """Builder for the `from_element` method depending on the object."""

    @functools.cached_property
    def var_element(self) -> py.Primary:
        return self.module.imports(path='website.language.base.processing', name='Element')

    @functools.cached_property
    def var_lemma(self) -> py.Primary:
        return self.module.imports(path='website.language.base.processing', name='Lemma')

    @functools.cached_property
    def var_token(self) -> py.Primary:
        return self.module.imports(path='website.language.base.processing', name='Token')

    def make_function(self, obj_type: typing.Optional[py.Expression], return_type: py.Expression,
                      statements: list[py.Statement]) -> py.Def:
        if obj_type:
            statements = [
                py.Assert(test=py.FUNCS.ISINSTANCE.call(LEX.OBJ, obj_type)),
                *statements
            ]

        return py.Def(
            decorators=[py.DECORATORS.CLASSMETHOD],
            name=LEX.PARSE,
            rtype=return_type,
            args=[
                py.Argument(name=py.Variable('cls')),
                py.Argument(name=LEX.OBJ, type=self.var_element)
            ],
            block=py.Block(statements=statements)
        )

    def from_attribute(self, attribute: Attribute) -> py.Expression:
        name = attribute.name

        types = [py.Variable(attr_type) for attr_type in sorted(attribute.types)]

        if len(types) != 1:
            raise NotImplementedError

        attr_type = types[0]

        # TODO : handle the __from_element__ case of groups
        func = attr_type.getattr(LEX.PARSE)

        obj_data = LEX.OBJ.getattr('data')
        arg_key = py.String(content=repr(name))
        arg = obj_data.subscript(arg_key)

        if attribute.multiple:
            # list-map version
            'list(map([$func$], [$arg$]))'
            # value = py.Call(left=py.TYPES.LIST, args=[
            #     py.Call(left=py.FUNCS.MAP, args=[func, arg])
            # ])

            # list comprehension version
            '[[$func$](item) for item in [$arg$]]'
            value = py.ListComp(
                elt=func.call(LEX.ITEM),
                generators=[py.ForIfClause(target=LEX.ITEM, iter=arg)]
            )
        else:
            value = func.call(arg)

        if not attribute.required:
            value = py.IfExp(body=value, test=py.In(left=arg_key, right=obj_data), or_else=py.NoneClass())
            # value = py.IfExp(body=py.NoneClass(), test=py.Is(arg, py.NoneClass()), or_else=value)

        return value

    def from_descriptor(self, descriptor: Descriptor) -> list[py.Statement]:
        attributes = sorted(descriptor.attributes.values(), key=lambda a: not a.required)
        __version = 1
        if __version == 1:
            # single statement version
            return [
                py.Return(
                    expr=py.IndentedCall(
                        left=py.Variable('cls'),
                        body=py.IndentedCallBody(args=[
                            py.NamedArgument(
                                name=py.Variable(attribute.name),
                                expr=self.from_attribute(attribute)
                            )
                            for attribute in attributes
                        ])
                    )
                )
            ]
        elif __version == 2:
            # multi statement version
            return [
                py.AnnAssign(target=LEX.DATA, value=py.Dict(items=[])),
                *[
                    py.AnnAssign(
                        target=LEX.DATA.subscript(py.String(content=repr(attribute.name))),
                        value=self.from_attribute(attribute)
                    )
                    for attribute in attributes
                ],
                py.Return(py.Variable('cls').call(py.SSArgument(expr=LEX.DATA)))
            ]
        else:
            raise NotImplementedError

    @staticmethod
    def _group_return_statement(__type: typing.Optional[bnf.Variable]) -> py.Statement:
        if __type is None:
            return py.Raise(py.Variable("ValueError").call(
                py.Variable('cls').getattr('__name__'),
                py.String(repr(LEX.PARSE.content)),
                py.Variable('repr').call(LEX.OBJ.getattr('type'))
            ))
        else:
            return py.Return(py.Variable(__type.content).getattr(LEX.PARSE).call(LEX.OBJ))

    @classmethod
    def _group_if(cls, __type: bnf.Variable) -> py.If:
        return py.If(
            condition=py.Eq(LEX.OBJ.getattr('type'), py.String(repr(__type.content))),
            block=py.Block([cls._group_return_statement(__type)])
        )

    def statement_for_group(self, group: bnf.Group) -> py.Statement:
        raw_types, ref_types = [], []

        for sub_type in group.types:
            toplevel = self.get(sub_type)
            if isinstance(toplevel, (bnf.Branch, bnf.PatternGR)):
                raw_types.append(toplevel.type)
            elif isinstance(toplevel, bnf.Group):
                ref_types.append(toplevel.type)
            else:
                raise ValueError

        if len(ref_types) == 0:
            statement = self._group_return_statement(None)
        elif len(ref_types) == 1:
            statement = self._group_return_statement(ref_types[0])
        else:
            raise ValueError

        if len(raw_types) > 0:
            statement = py.If.switch(if_list=list(map(self._group_if, raw_types)), default=py.Block([statement]))

        return statement

    def statement_for(self, node: cm.Node) -> py.Def:
        if isinstance(node.toplevel, bnf.Branch):
            obj_type = self.var_lemma
            statements = self.from_descriptor(node.descriptor)
        elif isinstance(node.toplevel, bnf.PatternGR):
            obj_type = self.var_token
            statements = [
                py.Return(py.Variable('cls').call(
                    py.NamedArgument(py.Variable('content'), LEX.OBJ.getattr('content')),
                ))
            ]
        elif isinstance(node.toplevel, bnf.Group):
            obj_type = None
            statements = [self.statement_for_group(node.toplevel)]
        else:
            raise NotImplementedError

        return_type = py.Variable(node.toplevel.type.to_str())
        return self.make_function(obj_type=obj_type, return_type=return_type, statements=statements)

    def statements_for(self, node: cm.Node) -> list[py.Statement]:
        try:
            yield self.statement_for(node)

        except ValueError:
            website.console.warning(f"Failed to create `{node.type!s}.{LEX.PARSE!s}` method.")
            yield from []

    def include_requirements(self, requirements: list[py.Statement]) -> None:
        pass
