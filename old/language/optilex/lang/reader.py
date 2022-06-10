"""Auto generated module.Any manual changes might be overwritten."""
from website.language.bnf.lang.models import *

__all__ = [
    'reader'
]
# PATTERNS

_KEYWORD_KW_INCLUDE = KeywordPattern(type=Variable(content='KW_INCLUDE'), expr=String(content="'INCLUDE'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_NOT = KeywordPattern(type=Variable(content='KW_NOT'), expr=String(content="'NOT'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_CLEAR = KeywordPattern(type=Variable(content='KW_CLEAR'), expr=String(content="'CLEAR'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_BUILD = KeywordPattern(type=Variable(content='KW_BUILD'), expr=String(content="'BUILD'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LEFT_PARENTHESIS = StringPattern(type=Variable(content='LEFT_PARENTHESIS'), expr=String(content="'('"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RIGHT_PARENTHESIS = StringPattern(type=Variable(content='RIGHT_PARENTHESIS'), expr=String(content="')'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_GOTO = KeywordPattern(type=Variable(content='KW_GOTO'), expr=String(content="'GOTO'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_AMPERSAND = StringPattern(type=Variable(content='AMPERSAND'), expr=String(content="'&'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COLON = StringPattern(type=Variable(content='COLON'), expr=String(content="':'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_DEFAULT = KeywordPattern(type=Variable(content='KW_DEFAULT'), expr=String(content="'DEFAULT'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LS = StringPattern(type=Variable(content='LS'), expr=String(content="'{'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RS = StringPattern(type=Variable(content='RS'), expr=String(content="'}'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_INDENT = StringPattern(type=Variable(content='INDENT'), expr=String(content="'    '"), priority=None, cast=None, ignore_=Ignore())
_REGEX_INTEGER = RegexPattern(type=Variable(content='Integer'), expr=String(content="'\\-?\\d+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_VARIABLE = RegexPattern(type=Variable(content='Variable'), expr=String(content="'[a-zA-Z_]\\w*'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_STRING = RegexPattern(type=Variable(content='String'), expr=String(content='\'\\"(?:\\\\\\"|[^\\"])*?\\"|\\\'(?:\\\\\\\'|[^\\\'])*?\\\'\''), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_WHITESPACE = RegexPattern(type=Variable(content='WHITESPACE'), expr=String(content="'\\s+'"), priority=None, cast=None, ignore_=Ignore(), flags=None)

# BRANCHES

_BRANCH_INCLUDE = Branch(type=Variable(content='Include'), rule=Match(type=Variable(content='KW_INCLUDE')), priority=None, line_prefix=None)
_BRANCH_INVERTED = Branch(type=Variable(content='Inverted'), rule=Match(type=Variable(content='KW_NOT')), priority=None, line_prefix=None)
_BRANCH_CLEAR = Branch(type=Variable(content='Clear'), rule=Match(type=Variable(content='KW_CLEAR')), priority=None, line_prefix=None)
_BRANCH_ACTION = Branch(type=Variable(content='Action'), rule=Sequence(rules=[Optional(rule=MatchAs(type=Variable(content='Include'), key=Variable(content='include_'))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_BUILD')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='build')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_GOTO')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Integer'), key=Variable(content='goto')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]))), Optional(rule=MatchAs(type=Variable(content='Clear'), key=Variable(content='clear')))]), priority=None, line_prefix=None)
_BRANCH_ACTION_LIST = Branch(type=Variable(content='ActionList'), rule=Sequence(rules=[MatchIn(type=Variable(content='Action'), key=Variable(content='items')), Match(type=Variable(content='AMPERSAND')), MatchIn(type=Variable(content='Action'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='AMPERSAND')), MatchIn(type=Variable(content='Action'), key=Variable(content='items'))])))]), priority=None, line_prefix=None)
_BRANCH_CHARSET = Branch(type=Variable(content='Charset'), rule=Sequence(rules=[Optional(rule=MatchAs(type=Variable(content='Inverted'), key=Variable(content='inverted'))), MatchAs(type=Variable(content='String'), key=Variable(content='items'))]), priority=None, line_prefix=None)
_BRANCH_OUTCOME = Branch(type=Variable(content='Outcome'), rule=Sequence(rules=[MatchAs(type=Variable(content='Charset'), key=Variable(content='charset')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='ActionList'), key=Variable(content='actions'))]), priority=None, line_prefix=None)
_BRANCH_BLOCK = Branch(type=Variable(content='Block'), rule=Sequence(rules=[RepeatStar(rule=MatchIn(type=Variable(content='Outcome'), key=Variable(content='outcomes'))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_DEFAULT')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='ActionList'), key=Variable(content='default'))])))]), priority=None, line_prefix=String(content="'    '"))
_BRANCH_GROUP_SELECT = Branch(type=Variable(content='GroupSelect'), rule=Sequence(rules=[MatchAs(type=Variable(content='Integer'), key=Variable(content='origin')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_ORIGIN_SELECT = Branch(type=Variable(content='OriginSelect'), rule=Sequence(rules=[MatchIn(type=Variable(content='GroupSelect'), key=Variable(content='cases')), RepeatStar(rule=MatchIn(type=Variable(content='GroupSelect'), key=Variable(content='cases')))]), priority=None, line_prefix=None)

# GROUPS

_GROUP_ALL = Group(type=Variable('All'), types=[
    Variable('ActionList'),
    Variable('Action'),
    Variable('Charset'),
    Variable('Outcome'),
    Variable('Block'),
    Variable('GroupSelect'),
    Variable('OriginSelect'),
    Variable('Include'),
    Variable('Inverted'),
    Variable('Clear'),
    Variable('Integer'),
    Variable('Variable'),
    Variable('String')
])


reader = Reader(
    lexer=Lexer(
        patterns=[
            _KEYWORD_KW_INCLUDE,
            _KEYWORD_KW_NOT,
            _KEYWORD_KW_CLEAR,
            _KEYWORD_KW_BUILD,
            _STRING_LEFT_PARENTHESIS,
            _STRING_RIGHT_PARENTHESIS,
            _KEYWORD_KW_GOTO,
            _STRING_AMPERSAND,
            _STRING_COLON,
            _KEYWORD_KW_DEFAULT,
            _STRING_LS,
            _STRING_RS,
            _STRING_INDENT,
            _REGEX_INTEGER,
            _REGEX_VARIABLE,
            _REGEX_STRING,
            _REGEX_WHITESPACE
        ]
    ),
    parser=Parser(
        branches=[
            _BRANCH_INCLUDE,
            _BRANCH_INVERTED,
            _BRANCH_CLEAR,
            _BRANCH_ACTION,
            _BRANCH_ACTION_LIST,
            _BRANCH_CHARSET,
            _BRANCH_OUTCOME,
            _BRANCH_BLOCK,
            _BRANCH_GROUP_SELECT,
            _BRANCH_ORIGIN_SELECT,
            _GROUP_ALL
        ],
        start=Variable('OriginSelect')
    )
)
