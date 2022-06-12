import dataclasses
import functools
import itertools
import typing

from base.models import Attribute
from core.langs import bnf
from core.langs.python import *
from ._abc import PartBuilder

__all__ = [
    'StrMethodBuilder'
]

StmtG = typing.Iterator[Statement]
StmtL = list[Statement]


class LEX:
    INDENTED = Variable("_indented")  # decorator
    FLAT_STR = Variable("_flat_str")  # decorator

    PREFIX = Variable("prefix")
    WRAPPER = Variable("wrapper")
    WRAPPED = Variable("wrapped")
    SELF = Variable("self")
    ITEM = Variable("e")
    INDEX = Variable("i")
    METHOD = Variable("method")


def call_istr(__base: Primary) -> Expression:
    return TYPES.STR.call(__base)


def _loop_attribute(attribute: Attribute, statements: StmtG) -> StmtG:
    yield Block(statements=list(statements)).do_for(
        args=[LEX.ITEM],
        iterator=LEX.SELF.getattr(attribute.name)
    )


def _enum_attribute(attribute: Attribute, separator: StmtG, element: StmtG) -> StmtG:
    yield Block([
        Block(statements=list(separator)).do_if(
            test=LEX.INDEX
        ),
        *element
    ]).do_for(
        args=[LEX.INDEX, LEX.ITEM],
        iterator=FUNCS.ENUMERATE.call(
            LEX.SELF.getattr(attribute.name)
        )
    )


def _if_optional_attributes(attributes: list[Attribute], statements: StmtG) -> StmtG:
    variables = [LEX.SELF.getattr(Variable(attribute.name)) for attribute in attributes]

    if len(variables) == 0:
        yield from statements
        return

    elif len(variables) == 1:
        condition = variables[0]

    else:
        first, second, *remain = variables
        condition = And(first, second)
        for variable in remain:
            condition = And(condition, variable)

    yield Block(statements=list(statements)).do_if(condition)


def _get_repeat_attribute(rule: bnf.ParallelGR) -> Attribute:
    # TODO[1]
    descriptor = rule.descriptor
    attribute, *remaining = descriptor.attributes.values()
    assert not remaining, "Cannot repeat multiple attributes at a time !"
    assert attribute.multiple, "Cannot repeat a non-multiple attribute !"
    return attribute


def _merge_inners(*all_statements: list[StmtL]) -> StmtL:
    statements = []

    for row in itertools.zip_longest(*all_statements):
        if all(s1 == s2 for s1 in row for s2 in row):
            statements.append(row[0])
        else:
            raise NotImplementedError(row)

    return statements


def _get_flat_str_wrapper():
    """
        Build the following model.
        >>> def flat_istr(method: typing.Callable[[object], typing.Iterator[str]]) -> typing.Callable[[object], str]:
        >>>     def wrapped(self) -> str:
        >>>         return ''.join(method(self))
        >>>
        >>>     return wrapped
    """
    # TODO : import typing for the duck types
    return Def(
        name=LEX.FLAT_STR,
        args=[
            Argument(name=LEX.METHOD, type=None)  # TODO : include duck type
        ],
        rtype=None,  # TODO :include duck type
        block=Block([
            Def(
                name=LEX.WRAPPED,
                args=[
                    Argument(name=LEX.SELF)
                ],
                rtype=TYPES.STR,
                block=Block([
                    Return(String("''").getattr('join').call(LEX.METHOD.call(LEX.SELF)))
                ])
            ),
            Return(LEX.WRAPPED)
        ])
    )


def _get_indented_wrapper() -> Def:
    """
        Build the following model.
        >>> def _indented(prefix: str):
        >>>     def wrapper(method):
        >>>         def wrapped(self) -> str:
        >>>             return method(self).replace('\\n', '\\n' + prefix)
        >>>         return wrapped
        >>>     return wrapper
    """
    newline = String(repr('\n'))
    wrapped_func = Def(
        name=LEX.WRAPPED,
        args=[LEX.SELF.as_def_arg()],
        rtype=TYPES.STR,
        block=Block([
            Return(
                LEX.METHOD.call(LEX.SELF).getattr('replace').call(newline, Add(newline, LEX.PREFIX))
            )
        ])
    )
    wrapper_func = Def(
        name=LEX.WRAPPER,
        args=[LEX.METHOD.as_def_arg()],
        block=Block([
            wrapped_func,
            LEX.WRAPPED.as_return
        ])
    )
    return Def(
        name=LEX.INDENTED,
        args=[LEX.PREFIX.as_def_arg(type_=TYPES.STR)],
        block=Block([
            wrapper_func,
            LEX.WRAPPER.as_return
        ])
    )


@dataclasses.dataclass
class StrMethodBuilder(PartBuilder):
    """Builder for the __str__ method depending on the object."""
    build_flat_istr: bool = False  # indicate if its required to build the flat_istr wrapper
    build_indented: bool = False  # indicate if its required to build the indenting_wrapper

    def flat_str_decorator(self) -> Decorator:
        self.build_flat_istr = True
        return Decorator(expr=LEX.FLAT_STR)

    def indented_wrapper_decorator(self, arg: String) -> Decorator:
        self.build_indented = True
        return Decorator(expr=LEX.INDENTED.call(arg))

    @staticmethod
    def sub_call(__type: bnf.Variable, ref: Primary) -> Yield:
        return Yield(expr=call_istr(ref))

    def make_function(self, decorators: list[Decorator], statements: list[Statement]) -> Def:
        return Def(
            decorators=decorators,
            name=Variable("__str__"),
            args=[LEX.SELF.as_def_arg()],
            rtype=self.module.imports('typing').getattr('Iterator').subscript(TYPES.STR),
            block=Block(statements=statements)
        )

    def get_function(self, __type: bnf.Variable, statements: StmtL, prefix: bnf.String = None) -> Def:
        decorators = []

        if prefix:
            decorators.append(self.indented_wrapper_decorator(String(content=prefix.content)))

        decorators.append(self.flat_str_decorator())

        return self.make_function(decorators=decorators, statements=statements)

    ####################################################################################################################
    # CONVERT ParallelGR
    ####################################################################################################################

    @functools.singledispatchmethod
    def __call__(self, obj: bnf.ParallelGR) -> StmtG:
        raise NotImplementedError(f"build(...: {obj.__class__.__name__}) not defined !")

    # noinspection PyUnusedLocal
    @__call__.register
    def _(self, obj: bnf.Negative) -> StmtG:
        yield from ()

    # noinspection PyUnusedLocal
    @__call__.register
    def _(self, obj: bnf.MatchIn) -> StmtG:
        yield self.sub_call(obj.type, LEX.ITEM)

    @__call__.register
    def _(self, obj: bnf.Grouping) -> StmtG:
        yield from self(obj.rule)

    @__call__.register
    def _(self, obj: bnf.Canonical) -> StmtG:
        yield String(content=obj.expr.content).as_yield

    @__call__.register
    def _(self, obj: bnf.MatchAs) -> StmtG:
        yield self.sub_call(obj.type, LEX.SELF.getattr(obj.key.to_str()))

    @__call__.register
    def _(self, obj: bnf.Match) -> StmtG:
        toplevel = self.get(obj.type)
        if isinstance(toplevel, bnf.Alias):
            yield from self(toplevel.rule)

        elif isinstance(toplevel, (bnf.Branch, bnf.Group)):
            raise Exception(f"cannot build writer for {str(obj.type)!r}")

        elif isinstance(toplevel, bnf.PatternGR):
            expr: bnf.String = toplevel.canonical
            yield Yield(String(expr.content))

        else:
            raise NotImplementedError

    @__call__.register
    def _(self, obj: bnf.Sequence) -> StmtG:
        for rule in obj.rules:
            yield from self(rule)

    @__call__.register
    def _(self, obj: bnf.Parallel) -> StmtG:
        if len(obj.rules) == 1:
            yield from self(obj.rules[0])
        else:
            yield from _merge_inners(*map(self, obj.rules))

    @__call__.register
    def _(self, obj: bnf.Repeat) -> StmtG:
        attribute = _get_repeat_attribute(obj)
        statements = _loop_attribute(attribute=attribute, statements=self(obj.rule))
        if attribute.required:
            yield from statements
        else:
            yield from _if_optional_attributes(
                attributes=[attribute],
                statements=statements
            )

    @__call__.register
    def _(self, obj: bnf.RepeatStar) -> StmtG:
        attribute = _get_repeat_attribute(obj)
        assert not attribute.required, "RepeatStar attribute should be optional !"
        yield from _if_optional_attributes(
            attributes=[attribute],
            statements=_loop_attribute(
                attribute=attribute,
                statements=self(obj.rule)
            )
        )

    @__call__.register
    def _(self, obj: bnf.RepeatPlus) -> StmtG:
        attribute = _get_repeat_attribute(obj)
        assert attribute.required, "RepeatPlus attribute should be required !"
        yield from _loop_attribute(
            attribute=attribute,
            statements=self(obj.rule)
        )

    @__call__.register
    def _(self, obj: bnf.Optional) -> StmtG:
        model = obj.descriptor
        attributes = list(model.attributes.values())
        yield from _if_optional_attributes(
            attributes=[
                attribute
                for attribute in attributes
                if not attribute.required
            ],
            statements=self(obj.rule)
        )

    @__call__.register
    def _(self, obj: bnf.Enum0) -> StmtG:
        attribute = _get_repeat_attribute(obj.element)
        yield from _if_optional_attributes(
            attributes=[
                attribute
            ],
            statements=_enum_attribute(
                attribute=attribute,
                separator=self(obj.separator),
                element=self(obj.element)
            )
        )

    @__call__.register
    def _(self, obj: bnf.Enum1) -> StmtG:
        attribute = _get_repeat_attribute(obj.element)
        yield from _enum_attribute(
            attribute=attribute,
            separator=self(obj.separator),
            element=self(obj.element)
        )

    ####################################################################################################################
    # CONVERT TopLevel
    ####################################################################################################################

    @functools.singledispatchmethod
    def convert_toplevel(self, toplevel: bnf.TopLevel) -> Def:
        """Return the __str__ function associated with the given `toplevel`."""
        raise NotImplementedError(f"convert_toplevel(...: {toplevel.__class__.__name__}) not defined !")

    @convert_toplevel.register
    def _(self, toplevel: bnf.Branch) -> Def:
        return self.get_function(
            toplevel.type,
            statements=list(self(toplevel.rule)),
            prefix=toplevel.line_prefix
        )

    @convert_toplevel.register
    def _(self, toplevel: bnf.PatternGR) -> Def:
        return self.get_function(
            toplevel.type,
            statements=[Yield(LEX.SELF.getattr("content"))],
            prefix=None
        )

    # noinspection PyUnusedLocal
    @convert_toplevel.register
    def _(self, toplevel: bnf.Group) -> Def:
        return self.make_function(
            decorators=[Decorator(self.module.imports('abc').getattr('abstractmethod'))],
            statements=[PassClass()]
        )

    def statements_for(self, node: bnf.Node) -> StmtL:
        if isinstance(node.toplevel, bnf.Group) and node.origin_order != 0:
            return []

        return [self.convert_toplevel(node.toplevel)]

    def include_requirements(self, requirements: StmtL) -> None:
        if self.build_flat_istr:
            requirements.append(_get_flat_str_wrapper())

        if self.build_indented:
            requirements.append(_get_indented_wrapper())
