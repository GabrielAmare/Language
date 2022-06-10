"""Auto generated module.Any manual changes might be overwritten."""
from website.language.bnf.lang.models import *

__all__ = [
    'reader'
]
# PATTERNS

_KEYWORD_KW_IGNORE = KeywordPattern(type=Variable(content='KW_IGNORE'), expr=String(content="'ignore'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_STRING = KeywordPattern(type=Variable(content='KW_STRING'), expr=String(content="'string'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LB = StringPattern(type=Variable(content='LB'), expr=String(content="'['"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RB = StringPattern(type=Variable(content='RB'), expr=String(content="']'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LEFT_PARENTHESIS = StringPattern(type=Variable(content='LEFT_PARENTHESIS'), expr=String(content="'('"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RIGHT_PARENTHESIS = StringPattern(type=Variable(content='RIGHT_PARENTHESIS'), expr=String(content="')'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_REGEX = KeywordPattern(type=Variable(content='KW_REGEX'), expr=String(content="'regex'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_KEYWORD = KeywordPattern(type=Variable(content='KW_KEYWORD'), expr=String(content="'keyword'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LV = StringPattern(type=Variable(content='LV'), expr=String(content="'<'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_AS = KeywordPattern(type=Variable(content='KW_AS'), expr=String(content="'as'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_RV = StringPattern(type=Variable(content='RV'), expr=String(content="'>'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_IN = KeywordPattern(type=Variable(content='KW_IN'), expr=String(content="'in'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_DOLLAR = StringPattern(type=Variable(content='DOLLAR'), expr=String(content="'$'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EXC = StringPattern(type=Variable(content='EXC'), expr=String(content="'!'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LS = StringPattern(type=Variable(content='LS'), expr=String(content="'{'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COMMA = StringPattern(type=Variable(content='COMMA'), expr=String(content="','"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RS = StringPattern(type=Variable(content='RS'), expr=String(content="'}'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_ASTERISK = StringPattern(type=Variable(content='ASTERISK'), expr=String(content="'*'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_PLUS = StringPattern(type=Variable(content='PLUS'), expr=String(content="'+'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_INT = StringPattern(type=Variable(content='INT'), expr=String(content="'?'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DOT = StringPattern(type=Variable(content='DOT'), expr=String(content="'.'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_VBAR = StringPattern(type=Variable(content='VBAR'), expr=String(content="'|'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_BRANCH = KeywordPattern(type=Variable(content='KW_BRANCH'), expr=String(content="'branch'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_COLON_EQ = StringPattern(type=Variable(content='COLON_EQ'), expr=String(content="':='"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_ALIAS = KeywordPattern(type=Variable(content='KW_ALIAS'), expr=String(content="'alias'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_GROUP = KeywordPattern(type=Variable(content='KW_GROUP'), expr=String(content="'group'"), priority=Integer(content='200'), cast=None, ignore_=None)
_REGEX_STRING = RegexPattern(type=Variable(content='String'), expr=String(content='\'\\"(?:\\"|[^\\"])*?(?<!\\\\\\\\)\\"|\\\'(?:\\\'|[^\\\'])*?(?<!\\\\\\\\)\\\'\''), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_INTEGER = RegexPattern(type=Variable(content='Integer'), expr=String(content="'\\-?\\d+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_VARIABLE = RegexPattern(type=Variable(content='Variable'), expr=String(content="'[a-zA-Z_]\\w*'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_WHITESPACE = RegexPattern(type=Variable(content='WHITESPACE'), expr=String(content="'\\s+'"), priority=None, cast=None, ignore_=Ignore(), flags=None)
_REGEX_COMMENT = RegexPattern(type=Variable(content='COMMENT'), expr=String(content="'#.*'"), priority=None, cast=None, ignore_=Ignore(), flags=None)

# BRANCHES

_BRANCH_IGNORE = Branch(type=Variable(content='Ignore'), rule=Match(type=Variable(content='KW_IGNORE')), priority=None, line_prefix=None)
_BRANCH_STRING_PATTERN = Branch(type=Variable(content='StringPattern'), rule=Sequence(rules=[Match(type=Variable(content='KW_STRING')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='Integer'), key=Variable(content='priority')), Match(type=Variable(content='RB'))]))), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='cast')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]))), MatchAs(type=Variable(content='String'), key=Variable(content='expr')), Optional(rule=MatchAs(type=Variable(content='Ignore'), key=Variable(content='ignore_')))]), priority=None, line_prefix=None)
_BRANCH_REGEX_PATTERN = Branch(type=Variable(content='RegexPattern'), rule=Sequence(rules=[Match(type=Variable(content='KW_REGEX')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='Integer'), key=Variable(content='priority')), Match(type=Variable(content='RB'))]))), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='cast')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]))), MatchAs(type=Variable(content='String'), key=Variable(content='expr')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='flags'))), Optional(rule=MatchAs(type=Variable(content='Ignore'), key=Variable(content='ignore_')))]), priority=None, line_prefix=None)
_BRANCH_KEYWORD_PATTERN = Branch(type=Variable(content='KeywordPattern'), rule=Sequence(rules=[Match(type=Variable(content='KW_KEYWORD')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='Integer'), key=Variable(content='priority')), Match(type=Variable(content='RB'))]))), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='cast')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]))), MatchAs(type=Variable(content='String'), key=Variable(content='expr')), Optional(rule=MatchAs(type=Variable(content='Ignore'), key=Variable(content='ignore_')))]), priority=None, line_prefix=None)
_BRANCH_LEXER = Branch(type=Variable(content='Lexer'), rule=Sequence(rules=[MatchIn(type=Variable(content='PatternGR'), key=Variable(content='patterns')), RepeatStar(rule=MatchIn(type=Variable(content='PatternGR'), key=Variable(content='patterns')))]), priority=None, line_prefix=None)
_BRANCH_MATCH_AS = Branch(type=Variable(content='MatchAs'), rule=Sequence(rules=[Match(type=Variable(content='LV')), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Match(type=Variable(content='KW_AS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='key')), Match(type=Variable(content='RV'))]), priority=None, line_prefix=None)
_BRANCH_MATCH_IN = Branch(type=Variable(content='MatchIn'), rule=Sequence(rules=[Match(type=Variable(content='LV')), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='Variable'), key=Variable(content='key')), Match(type=Variable(content='RV'))]), priority=None, line_prefix=None)
_BRANCH_MATCH = Branch(type=Variable(content='Match'), rule=Sequence(rules=[Match(type=Variable(content='LV')), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Match(type=Variable(content='RV'))]), priority=None, line_prefix=None)
_BRANCH_CANONICAL = Branch(type=Variable(content='Canonical'), rule=Sequence(rules=[Match(type=Variable(content='DOLLAR')), MatchAs(type=Variable(content='String'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_LITERAL = Branch(type=Variable(content='Literal'), rule=MatchAs(type=Variable(content='String'), key=Variable(content='expr')), priority=None, line_prefix=None)
_BRANCH_GROUPING = Branch(type=Variable(content='Grouping'), rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule')), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_NEGATIVE = Branch(type=Variable(content='Negative'), rule=Sequence(rules=[Match(type=Variable(content='EXC')), MatchAs(type=Variable(content='GroupingGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT = Branch(type=Variable(content='Repeat'), rule=Sequence(rules=[Match(type=Variable(content='LS')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='mn'))), Match(type=Variable(content='COMMA')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='mx'))), Match(type=Variable(content='RS')), MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT_STAR = Branch(type=Variable(content='RepeatStar'), rule=Sequence(rules=[Match(type=Variable(content='ASTERISK')), MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT_PLUS = Branch(type=Variable(content='RepeatPlus'), rule=Sequence(rules=[Match(type=Variable(content='PLUS')), MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_OPTIONAL = Branch(type=Variable(content='Optional'), rule=Sequence(rules=[Match(type=Variable(content='INT')), MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_ENUM0 = Branch(type=Variable(content='Enum0'), rule=Sequence(rules=[MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='separator')), Match(type=Variable(content='DOT')), MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='element'))]), priority=None, line_prefix=None)
_BRANCH_ENUM1 = Branch(type=Variable(content='Enum1'), rule=Sequence(rules=[MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='separator')), Match(type=Variable(content='DOT')), Match(type=Variable(content='DOT')), MatchAs(type=Variable(content='NegativeGR'), key=Variable(content='element'))]), priority=None, line_prefix=None)
_BRANCH_SEQUENCE = Branch(type=Variable(content='Sequence'), rule=Sequence(rules=[MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='rules')), MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='rules')), RepeatStar(rule=MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='rules')))]), priority=None, line_prefix=None)
_BRANCH_PARALLEL = Branch(type=Variable(content='Parallel'), rule=Sequence(rules=[MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='rules')), Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='rules')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='rules'))])))]), priority=None, line_prefix=None)
_BRANCH_BRANCH = Branch(type=Variable(content='Branch'), rule=Sequence(rules=[Match(type=Variable(content='KW_BRANCH')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='Integer'), key=Variable(content='priority')), Match(type=Variable(content='RB'))]))), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Optional(rule=MatchAs(type=Variable(content='String'), key=Variable(content='line_prefix'))), Match(type=Variable(content='COLON_EQ')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_ALIAS = Branch(type=Variable(content='Alias'), rule=Sequence(rules=[Match(type=Variable(content='KW_ALIAS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Optional(rule=MatchAs(type=Variable(content='String'), key=Variable(content='line_prefix'))), Match(type=Variable(content='COLON_EQ')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_GROUP = Branch(type=Variable(content='Group'), rule=Sequence(rules=[Match(type=Variable(content='KW_GROUP')), MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Match(type=Variable(content='COLON_EQ')), MatchIn(type=Variable(content='Variable'), key=Variable(content='types')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='Variable'), key=Variable(content='types'))])))]), priority=None, line_prefix=None)
_BRANCH_PARSER = Branch(type=Variable(content='Parser'), rule=Sequence(rules=[MatchIn(type=Variable(content='BranchGR'), key=Variable(content='branches')), RepeatStar(rule=MatchIn(type=Variable(content='BranchGR'), key=Variable(content='branches'))), Match(type=Variable(content='RV')), MatchAs(type=Variable(content='Variable'), key=Variable(content='start'))]), priority=None, line_prefix=None)
_BRANCH_READER = Branch(type=Variable(content='Reader'), rule=Sequence(rules=[MatchAs(type=Variable(content='Lexer'), key=Variable(content='lexer')), MatchAs(type=Variable(content='Parser'), key=Variable(content='parser'))]), priority=None, line_prefix=None)

# GROUPS

_GROUP_PATTERN_GR = Group(type=Variable('PatternGR'), types=[
    Variable('StringPattern'),
    Variable('RegexPattern'),
    Variable('KeywordPattern')
])
_GROUP_MATCH_KEY_GR = Group(type=Variable('MatchKeyGR'), types=[
    Variable('MatchAs'),
    Variable('MatchIn')
])
_GROUP_MATCH_GR = Group(type=Variable('MatchGR'), types=[
    Variable('MatchKeyGR'),
    Variable('Match')
])
_GROUP_ATOM_GR = Group(type=Variable('AtomGR'), types=[
    Variable('Canonical'),
    Variable('Literal'),
    Variable('MatchGR')
])
_GROUP_GROUPING_GR = Group(type=Variable('GroupingGR'), types=[
    Variable('Grouping'),
    Variable('AtomGR')
])
_GROUP_NEGATIVE_GR = Group(type=Variable('NegativeGR'), types=[
    Variable('Negative'),
    Variable('GroupingGR')
])
_GROUP_REPEAT_GR = Group(type=Variable('RepeatGR'), types=[
    Variable('Repeat'),
    Variable('RepeatStar'),
    Variable('RepeatPlus'),
    Variable('Optional'),
    Variable('Enum0'),
    Variable('Enum1'),
    Variable('NegativeGR')
])
_GROUP_SEQUENCE_GR = Group(type=Variable('SequenceGR'), types=[
    Variable('Sequence'),
    Variable('RepeatGR')
])
_GROUP_PARALLEL_GR = Group(type=Variable('ParallelGR'), types=[
    Variable('Parallel'),
    Variable('SequenceGR')
])
_GROUP_BRANCH_GR = Group(type=Variable('BranchGR'), types=[
    Variable('Branch'),
    Variable('Alias'),
    Variable('Group')
])
_GROUP_BUILDABLE = Group(type=Variable('Buildable'), types=[
    Variable('BranchGR'),
    Variable('ParallelGR')
])
_GROUP_TOP_LEVEL = Group(type=Variable('TopLevel'), types=[
    Variable('BranchGR'),
    Variable('PatternGR')
])
_GROUP_ALL = Group(type=Variable('All'), types=[
    Variable('String'),
    Variable('Variable'),
    Variable('Integer'),
    Variable('Ignore'),
    Variable('TopLevel'),
    Variable('Buildable'),
    Variable('Lexer'),
    Variable('Parser'),
    Variable('Reader')
])


reader = Reader(
    lexer=Lexer(
        patterns=[
            _KEYWORD_KW_IGNORE,
            _KEYWORD_KW_STRING,
            _STRING_LB,
            _STRING_RB,
            _STRING_LEFT_PARENTHESIS,
            _STRING_RIGHT_PARENTHESIS,
            _KEYWORD_KW_REGEX,
            _KEYWORD_KW_KEYWORD,
            _STRING_LV,
            _KEYWORD_KW_AS,
            _STRING_RV,
            _KEYWORD_KW_IN,
            _STRING_DOLLAR,
            _STRING_EXC,
            _STRING_LS,
            _STRING_COMMA,
            _STRING_RS,
            _STRING_ASTERISK,
            _STRING_PLUS,
            _STRING_INT,
            _STRING_DOT,
            _STRING_VBAR,
            _KEYWORD_KW_BRANCH,
            _STRING_COLON_EQ,
            _KEYWORD_KW_ALIAS,
            _KEYWORD_KW_GROUP,
            _REGEX_STRING,
            _REGEX_INTEGER,
            _REGEX_VARIABLE,
            _REGEX_WHITESPACE,
            _REGEX_COMMENT
        ]
    ),
    parser=Parser(
        branches=[
            _BRANCH_IGNORE,
            _BRANCH_STRING_PATTERN,
            _BRANCH_REGEX_PATTERN,
            _BRANCH_KEYWORD_PATTERN,
            _GROUP_PATTERN_GR,
            _BRANCH_LEXER,
            _BRANCH_MATCH_AS,
            _BRANCH_MATCH_IN,
            _GROUP_MATCH_KEY_GR,
            _BRANCH_MATCH,
            _GROUP_MATCH_GR,
            _BRANCH_CANONICAL,
            _BRANCH_LITERAL,
            _GROUP_ATOM_GR,
            _BRANCH_GROUPING,
            _GROUP_GROUPING_GR,
            _BRANCH_NEGATIVE,
            _GROUP_NEGATIVE_GR,
            _BRANCH_REPEAT,
            _BRANCH_REPEAT_STAR,
            _BRANCH_REPEAT_PLUS,
            _BRANCH_OPTIONAL,
            _BRANCH_ENUM0,
            _BRANCH_ENUM1,
            _GROUP_REPEAT_GR,
            _BRANCH_SEQUENCE,
            _GROUP_SEQUENCE_GR,
            _BRANCH_PARALLEL,
            _GROUP_PARALLEL_GR,
            _BRANCH_BRANCH,
            _BRANCH_ALIAS,
            _BRANCH_GROUP,
            _GROUP_BRANCH_GR,
            _GROUP_BUILDABLE,
            _GROUP_TOP_LEVEL,
            _BRANCH_PARSER,
            _BRANCH_READER,
            _GROUP_ALL
        ],
        start=Variable('Reader')
    )
)
