import dataclasses
import functools
import typing

from core.langs import bnf
from core.langs.python import *
from tools import style_case
from ._abc import TextBuilder

__all__ = [
    'ReaderBuilder'
]

_TYPE_PREFIXES: typing.Dict[typing.Type[bnf.TopLevel], str] = {
    bnf.StringPattern: 'STRING',
    bnf.KeywordPattern: 'KEYWORD',
    bnf.RegexPattern: 'REGEX',
    bnf.Group: 'GROUP',
    bnf.Branch: 'BRANCH',
    bnf.Alias: 'ALIAS',
}


def indented_call(left: Primary, args: list[CallArgumentGR]) -> IndentedCall:
    return IndentedCall(left=left, body=IndentedCallBody(args))


def indented_list(items: list[Expression]) -> IndentedList:
    return IndentedList(body=IndentedExprEnum(items))


def variable_for(__type: str) -> Primary:
    return Variable('Variable').call(String(repr(__type)))


@dataclasses.dataclass
class ReaderBuilder(TextBuilder):
    reader: bnf.Reader

    def __post_init__(self):
        self.reader = self.reader.simplify(literals=True, aliases=True, canonicals=True, repeats=True)

    @functools.cached_property
    def module(self) -> DynamicModule:
        return DynamicModule(
            docstring="Auto generated module."
                      "Any manual changes might be overwritten.",
            version=self.config.python_version
        )

    def get_name(self, obj: bnf.TopLevel) -> Variable:
        prefix = _TYPE_PREFIXES[obj.__class__]
        name = str(obj.type)
        if style_case.matches(name, style_case.Styles.PASCAL_CASE):
            name = style_case.convert(name, style_case.Styles.PASCAL_CASE, style_case.Styles.SCREAM_CASE)
        elif style_case.matches(name, style_case.Styles.SCREAM_CASE):
            name = style_case.convert(name, style_case.Styles.SCREAM_CASE, style_case.Styles.SCREAM_CASE)
        else:
            raise NotImplementedError(repr(name))
        return Variable(f"_{prefix}_{name}")

    def get_statements(self) -> typing.Generator[Statement, None, None]:
        # names = []
        yield Comment(content="# PATTERNS")
        yield EmptyLine()

        lexer_patterns = []
        for pattern in self.reader.lexer.patterns:
            name = self.get_name(pattern)
            lexer_patterns.append(name)
            yield AnnAssign(
                target=name,
                annotation=None,
                value=Variable(content=repr(pattern))  # TODO : should not be inside a Variable content
            )
            # print('--', name)
            # names.append(name)

        yield EmptyLine()
        yield Comment(content="# BRANCHES")
        yield EmptyLine()

        parser_branches = []
        group_statements = []
        for branch in self.reader.parser.branches:
            name = self.get_name(branch)
            parser_branches.append(name)
            if isinstance(branch, bnf.Group):
                stmt = AnnAssign(
                    target=name,
                    annotation=None,
                    value=Call(
                        left=Variable('Group'),
                        args=[
                            NamedArgument(name=Variable('type'), expr=variable_for(str(branch.type))),
                            NamedArgument(name=Variable('types'), expr=indented_list([
                                variable_for(str(_type))
                                for _type in branch.types
                            ]))
                        ]
                    )
                )
                group_statements.append(stmt)
            else:
                yield AnnAssign(
                    target=name,
                    annotation=None,
                    value=Variable(content=repr(branch))  # TODO : should not be inside a Variable content
                )
            # print('--', name)
            # names.append(name)

        yield EmptyLine()
        yield Comment(content="# GROUPS")
        yield EmptyLine()
        yield from group_statements

        # for name in set(names):
        #     if names.count(name) > 1:
        #         print('!', 'repeated name ' + repr(name))

        yield EmptyLine()
        yield EmptyLine()

        yield AnnAssign(
            target=Variable(self.config.reader_name),
            annotation=None,
            value=indented_call(
                left=Variable('Reader'),
                args=[
                    NamedArgument(
                        name=Variable('lexer'),
                        expr=indented_call(
                            left=Variable('Lexer'),
                            args=[
                                NamedArgument(
                                    name=Variable('patterns'),
                                    expr=indented_list([
                                        *lexer_patterns
                                    ])
                                )
                            ]
                        )
                    ),
                    NamedArgument(
                        name=Variable('parser'),
                        expr=indented_call(
                            left=Variable('Parser'),
                            args=[
                                NamedArgument(
                                    name=Variable('branches'),
                                    expr=indented_list([
                                        *parser_branches
                                    ])
                                ),
                                NamedArgument(
                                    name=Variable('start'),
                                    expr=variable_for(str(self.reader.parser.start))
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def build(self) -> str:
        self.module.imports_all('website.language.bnf.lang.models')
        self.module.statements.extend(self.get_statements())
        return str(self.module.to_module())
