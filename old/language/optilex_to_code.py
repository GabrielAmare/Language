import typing

from website.language import code_generator as cg
from website.language import optilex

__all__ = [
    'origin_select_to_module'
]

CONTENT = cg.Variable("content")
STATE = cg.Variable("state")
TOKENS = cg.Variable("tokens")
INDEX = cg.Variable("index")
CHAR = cg.Variable("char")
TEXT = cg.Variable("text")
STAY = cg.Variable("stay")
FUNC_INNER = cg.Variable("on_char")


def _convert_integer(self: optilex.Integer) -> cg.Integer:
    return cg.Integer(content=self.content)


def _convert_string(self: optilex.String) -> cg.String:
    return cg.String(content=self.content)


def _convert_charset(self: optilex.Charset) -> typing.Union[cg.Eq, cg.In, cg.__True]:
    chars = eval(self.items.content)
    if len(chars) == 1:
        return cg.Eq(CHAR, _convert_string(self.items))
    elif len(chars) > 1:
        return cg.In(CHAR, _convert_string(self.items))
    else:
        return cg.TRUE


def _convert_action(self: optilex.Action) -> cg.Block:
    assert self.include_ or self.goto
    statements = []

    if self.build and not self.clear:
        if self.include_ or self.goto:
            statements += [
                cg.Append(
                    TOKENS,
                    cg.Dict({
                        "t": cg.String(repr(self.build.content)),  # type
                        "s": cg.Sub(INDEX, cg.Length(CONTENT)),  # start (index)
                        "e": cg.Add(INDEX, cg.Integer('1')) if self.include_ else INDEX,  # end (index)
                        "c": cg.Add(CONTENT, CHAR) if self.include_ else CONTENT  # content
                    })
                )
            ]

    if self.include_:
        statements += [
            cg.ReturnList([
                cg.FALSE,
                cg.String("''") if self.build or self.clear else cg.Add(CONTENT, CHAR),
                _convert_integer(self.goto) if self.goto else STATE
            ])
        ]

    elif self.goto:
        statements += [
            cg.ReturnList([
                cg.TRUE,
                cg.String("''") if self.build or self.clear else CONTENT,
                _convert_integer(self.goto)
            ])
        ]

    else:
        raise Exception("infinite loop !")

    return cg.Block(statements)


def _convert_action_list(self: optilex.ActionList) -> cg.Block:
    if len(self.items) == 1:
        return _convert_action(self.items[0])
    else:
        raise NotImplementedError


def _convert_outcome(self: optilex.Outcome) -> cg.If:
    return cg.If(
        condition=_convert_charset(self.charset),
        block=_convert_action_list(self.actions)
    )


def _convert_block(self: optilex.Block) -> cg.Block:
    if self.outcomes:
        return cg.Block([
            cg.Conditional(
                cases=list(map(_convert_outcome, self.outcomes)),
                default=_convert_action_list(self.default) if self.default else None
            )
        ])
    elif self.default:
        return _convert_action_list(self.default)
    else:
        return cg.Block([])


def _convert_group_select(self: optilex.GroupSelect) -> cg.If:
    return cg.If(
        condition=cg.Eq(STATE, _convert_integer(self.origin)),
        block=_convert_block(self.block)
    )


def _convert_origin_select(self: optilex.OriginSelect) -> cg.Module:
    assert self.cases

    ON_CHAR = cg.Function(
        name=FUNC_INNER.name,
        args=[INDEX, CHAR, CONTENT, STATE],
        block=cg.Block([
            cg.Conditional(
                cases=list(map(_convert_group_select, self.cases)),
                default=cg.Block([
                    cg.Raise(
                        cg.Call(
                            obj=cg.Variable("SyntaxError"),
                            args=[STATE, INDEX, TOKENS]
                        )
                    )
                ])
            )
        ])
    )

    TOKENIZE = cg.Function(
        name="tokenize",
        args=[TEXT],
        block=cg.Block([
            cg.VarAssign(TOKENS.name, cg.List([])),

            ON_CHAR,

            cg.VarAssign(CONTENT.name, cg.String("''")),
            cg.VarAssign(STATE.name, cg.Integer('0')),
            cg.VarAssign(INDEX.name, cg.Integer('0')),

            cg.ForEnumerate(
                index=INDEX.name,
                item=CHAR.name,
                iterable=TEXT,
                block=cg.Block([
                    cg.VarAssign(STAY.name, cg.TRUE),
                    cg.While(
                        condition=STAY,
                        block=cg.Block([
                            cg.AssignList(
                                vars=[STAY.name, CONTENT.name, STATE.name],
                                expr=cg.Call(
                                    obj=FUNC_INNER,
                                    args=[INDEX, CHAR, CONTENT, STATE]
                                )
                            )
                        ])
                    )

                ])
            ),

            cg.TryCatch(
                try_block=cg.Block([
                    cg.Call(
                        obj=FUNC_INNER,
                        args=[
                            cg.Add(INDEX, cg.Integer('1')),
                            cg.String("'\x04'"),  # End-Of-Transmission character.
                            CONTENT,
                            STATE
                        ]
                    )
                ]),
                excepts={
                    "SyntaxError": cg.Block([])
                },
                error_name="e"
            ),
            cg.Return(TOKENS)

        ])
    )

    return cg.Module(
        # docstring=cg.MultiLineString('"""\n'
        #                              '    This module has been auto generated. Do not change manually.\n'
        #                              '"""'),
        statements=[
            TOKENIZE,
            cg.Export([TOKENIZE.name])
        ]
    )


origin_select_to_module = _convert_origin_select
