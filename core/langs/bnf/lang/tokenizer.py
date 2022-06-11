import re
from functools import singledispatch

from base.processing import Token
from .base import *


def tokenizer(lexer: Lexer, make_list: bool = False, single_line_errors: bool = False):
    def i_tokenize(text: str):
        index = 0
        at_row = -1
        at_col = -1

        def build(__type: str, content: str) -> Token:
            return Token(type=__type, at=index, to=index + len(content), content=content, at_row=at_row, at_col=at_col)

        @singledispatch
        def match(pattern: PatternGR):
            raise NotImplementedError(type(pattern))

        @match.register
        def _(pattern: StringPattern) -> Token:
            if text.startswith(String.to_str(pattern.expr), index):
                return build(str(pattern.type), String.to_str(pattern.expr))
            else:
                raise ValueError

        @match.register
        def _(pattern: KeywordPattern) -> Token:
            regex = re.compile(
                pattern=String.to_str(pattern.expr) + r"(?!\w)"
            )
            if result := regex.match(string=text, pos=index):
                return build(str(pattern.type), result.group())
            else:
                raise ValueError

        @match.register
        def _(pattern: RegexPattern) -> Token:
            regex = re.compile(
                pattern=String.to_str(pattern.expr),
                flags=Integer.to_int(pattern.flags)
            )
            if result := regex.match(string=text, pos=index):
                return build(str(pattern.type), result.group())
            else:
                raise ValueError

        def do_ignore(pattern: PatternGR) -> bool:
            if isinstance(pattern, (StringPattern, KeywordPattern, RegexPattern)):
                return Ignore.to_bool(pattern.ignore_)
            else:
                raise NotImplementedError(type(pattern))

        def next_token() -> tuple[Token, bool]:
            for pattern in lexer.patterns:
                try:
                    return match(pattern), do_ignore(pattern)
                except ValueError:
                    continue
            else:
                if single_line_errors:
                    return build("!SL_ERROR", content=text[index: text.index('\n', index)]), False
                else:
                    return build("!ML_ERROR", content=text[index:]), False

        at_row, at_col = 0, 0
        while index < len(text):
            token, ignore = next_token()
            index = token.to

            if '\n' in token.content:
                at_row += token.content.count('\n')
                at_col = token.content.rindex('\n')
            else:
                at_col += len(token.content)

            if not ignore:
                yield token

    if make_list:
        def tokenize(text: str):
            return list(i_tokenize(text))

        return tokenize
    else:
        return i_tokenize
