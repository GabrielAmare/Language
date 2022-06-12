import dataclasses
import functools
import typing

from base.models import Attribute, Descriptor
from core.langs import bnf
from core.langs.python import *
from tools import console
from ._abc import PartBuilder

__all__ = [
    'ParseMethodBuilder'
]


class LEX:
    OBJ = Variable('obj')
    ITEM = Variable('item')
    DATA = Variable('data')
    PARSE = Variable('parse')


@dataclasses.dataclass
class ParseMethodBuilder(PartBuilder):
    """Builder for the `from_element` method depending on the object."""

    @functools.cached_property
    def var_element(self) -> Primary:
        return self.module.imports(path='website.language.base.processing', name='Element')

    @functools.cached_property
    def var_lemma(self) -> Primary:
        return self.module.imports(path='website.language.base.processing', name='Lemma')

    @functools.cached_property
    def var_token(self) -> Primary:
        return self.module.imports(path='website.language.base.processing', name='Token')

    def make_function(self, obj_type: typing.Optional[Expression], return_type: Expression,
                      statements: list[Statement]) -> Def:
        if obj_type:
            statements = [
                Assert(test=FUNCS.ISINSTANCE.call(LEX.OBJ, obj_type)),
                *statements
            ]

        return Def(
            decorators=[DECORATORS.CLASSMETHOD],
            name=LEX.PARSE,
            rtype=return_type,
            args=[
                Argument(name=Variable('cls')),
                Argument(name=LEX.OBJ, type=self.var_element)
            ],
            block=Block(statements=statements)
        )

    def from_attribute(self, attribute: Attribute) -> Expression:
        name = attribute.name

        types = [Variable(attr_type) for attr_type in sorted(attribute.types)]

        if len(types) != 1:
            raise NotImplementedError

        attr_type = types[0]

        # TODO : handle the __from_element__ case of groups
        func = attr_type.getattr(LEX.PARSE)

        obj_data = LEX.OBJ.getattr('data')
        arg_key = String(content=repr(name))
        arg = obj_data.subscript(arg_key)

        if attribute.multiple:
            # list-map version
            'list(map([$func$], [$arg$]))'
            # value = Call(left=TYPES.LIST, args=[
            #     Call(left=FUNCS.MAP, args=[func, arg])
            # ])

            # list comprehension version
            '[[$func$](item) for item in [$arg$]]'
            value = ListComp(
                elt=func.call(LEX.ITEM),
                generators=[ForIfClause(target=LEX.ITEM, iter=arg)]
            )
        else:
            value = func.call(arg)

        if not attribute.required:
            value = IfExp(body=value, test=In(left=arg_key, right=obj_data), or_else=NoneClass())
            # value = IfExp(body=NoneClass(), test=Is(arg, NoneClass()), or_else=value)

        return value

    def from_descriptor(self, descriptor: Descriptor) -> list[Statement]:
        attributes = sorted(descriptor.attributes.values(), key=lambda a: not a.required)
        __version = 1
        if __version == 1:
            # single statement version
            return [
                Return(
                    expr=IndentedCall(
                        left=Variable('cls'),
                        body=IndentedCallBody(args=[
                            NamedArgument(
                                name=Variable(attribute.name),
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
                AnnAssign(target=LEX.DATA, value=Dict(items=[])),
                *[
                    AnnAssign(
                        target=LEX.DATA.subscript(String(content=repr(attribute.name))),
                        value=self.from_attribute(attribute)
                    )
                    for attribute in attributes
                ],
                Return(Variable('cls').call(SSArgument(expr=LEX.DATA)))
            ]
        else:
            raise NotImplementedError

    @staticmethod
    def _group_return_statement(__type: typing.Optional[bnf.Variable]) -> Statement:
        if __type is None:
            return Raise(Variable("ValueError").call(
                Variable('cls').getattr('__name__'),
                String(repr(LEX.PARSE.content)),
                Variable('repr').call(LEX.OBJ.getattr('type'))
            ))
        else:
            return Return(Variable(__type.content).getattr(LEX.PARSE).call(LEX.OBJ))

    @classmethod
    def _group_if(cls, __type: bnf.Variable) -> If:
        return If(
            condition=Eq(LEX.OBJ.getattr('type'), String(repr(__type.content))),
            block=Block([cls._group_return_statement(__type)])
        )

    def statement_for_group(self, group: bnf.Group) -> Statement:
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
            statement = If.switch(if_list=list(map(self._group_if, raw_types)), default=Block([statement]))

        return statement

    def statement_for(self, node: bnf.Node) -> Def:
        if isinstance(node.toplevel, bnf.Branch):
            obj_type = self.var_lemma
            statements = self.from_descriptor(node.descriptor)
        elif isinstance(node.toplevel, bnf.PatternGR):
            obj_type = self.var_token
            statements = [
                Return(Variable('cls').call(
                    NamedArgument(Variable('content'), LEX.OBJ.getattr('content')),
                ))
            ]
        elif isinstance(node.toplevel, bnf.Group):
            obj_type = None
            statements = [self.statement_for_group(node.toplevel)]
        else:
            raise NotImplementedError

        return_type = Variable(node.toplevel.type.to_str())
        return self.make_function(obj_type=obj_type, return_type=return_type, statements=statements)

    def statements_for(self, node: bnf.Node) -> list[Statement]:
        try:
            yield self.statement_for(node)

        except ValueError:
            console.warning(f"Failed to create `{node.type!s}.{LEX.PARSE!s}` method.")
            yield from []

    def include_requirements(self, requirements: list[Statement]) -> None:
        pass
