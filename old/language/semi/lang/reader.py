"""Auto generated module.Any manual changes might be overwritten."""
from website.language.bnf.lang.models import *

__all__ = [
    'reader'
]
# PATTERNS

_STRING_WAVE = StringPattern(type=Variable(content='WAVE'), expr=String(content="'~'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_PLUS = StringPattern(type=Variable(content='PLUS'), expr=String(content="'+'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_IGNORE = KeywordPattern(type=Variable(content='KW_IGNORE'), expr=String(content="'ignore'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_VALID = KeywordPattern(type=Variable(content='KW_VALID'), expr=String(content="'VALID'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_EXCLUDED = KeywordPattern(type=Variable(content='KW_EXCLUDED'), expr=String(content="'EXCLUDED'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_ERROR = KeywordPattern(type=Variable(content='KW_ERROR'), expr=String(content="'ERROR'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LB = StringPattern(type=Variable(content='LB'), expr=String(content="'['"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RB = StringPattern(type=Variable(content='RB'), expr=String(content="']'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LS = StringPattern(type=Variable(content='LS'), expr=String(content="'{'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COMMA = StringPattern(type=Variable(content='COMMA'), expr=String(content="','"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RS = StringPattern(type=Variable(content='RS'), expr=String(content="'}'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_VBAR = StringPattern(type=Variable(content='VBAR'), expr=String(content="'|'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_NEWLINE = StringPattern(type=Variable(content='NEWLINE'), expr=String(content="'\\n'"), priority=Integer(content='100'), cast=None, ignore_=None)
_REGEX_VARIABLE = RegexPattern(type=Variable(content='Variable'), expr=String(content="'[a-zA-Z_]\\w+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_INTEGER = RegexPattern(type=Variable(content='Integer'), expr=String(content="'\\d+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_STRING = RegexPattern(type=Variable(content='String'), expr=String(content='\'\\".*?\\"\''), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_WHITESPACE = RegexPattern(type=Variable(content='WHITESPACE'), expr=String(content="'\\s+'"), priority=None, cast=None, ignore_=Ignore(), flags=None)
_STRING_SPACE = StringPattern(type=Variable(content='SPACE'), expr=String(content="' '"), priority=None, cast=None, ignore_=Ignore())

# BRANCHES

_BRANCH_INVERTED = Branch(type=Variable(content='Inverted'), rule=Match(type=Variable(content='WAVE')), priority=None, line_prefix=None)
_BRANCH_INCLUDE = Branch(type=Variable(content='Include'), rule=Match(type=Variable(content='PLUS')), priority=None, line_prefix=None)
_BRANCH_IGNORE = Branch(type=Variable(content='Ignore'), rule=Match(type=Variable(content='KW_IGNORE')), priority=None, line_prefix=None)
_BRANCH_GROUP = Branch(type=Variable(content='Group'), rule=Sequence(rules=[Optional(rule=MatchAs(type=Variable(content='Inverted'), key=Variable(content='inverted'))), MatchAs(type=Variable(content='String'), key=Variable(content='items'))]), priority=None, line_prefix=None)
_BRANCH_VALID = Branch(type=Variable(content='Valid'), rule=Match(type=Variable(content='KW_VALID')), priority=None, line_prefix=None)
_BRANCH_EXCLUDED = Branch(type=Variable(content='Excluded'), rule=Match(type=Variable(content='KW_EXCLUDED')), priority=None, line_prefix=None)
_BRANCH_ERROR = Branch(type=Variable(content='Error'), rule=Match(type=Variable(content='KW_ERROR')), priority=None, line_prefix=None)
_BRANCH_MATCH = Branch(type=Variable(content='Match'), rule=MatchAs(type=Variable(content='Group'), key=Variable(content='group_')), priority=None, line_prefix=None)
_BRANCH_GROUPING = Branch(type=Variable(content='Grouping'), rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule')), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT = Branch(type=Variable(content='Repeat'), rule=Sequence(rules=[Match(type=Variable(content='LS')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='mn'))), Match(type=Variable(content='COMMA')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='mx'))), Match(type=Variable(content='RS')), MatchAs(type=Variable(content='GroupingGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_SEQUENCE = Branch(type=Variable(content='Sequence'), rule=Sequence(rules=[MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='rules')), MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='rules')), RepeatStar(rule=MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='rules')))]), priority=None, line_prefix=None)
_BRANCH_PARALLEL = Branch(type=Variable(content='Parallel'), rule=Sequence(rules=[MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='rules')), Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='rules')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='rules'))])))]), priority=None, line_prefix=None)
_BRANCH_BRANCH = Branch(type=Variable(content='Branch'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='type')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='Integer'), key=Variable(content='priority')), Match(type=Variable(content='RB'))]))), Optional(rule=MatchAs(type=Variable(content='Ignore'), key=Variable(content='ignore_'))), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule'))]), priority=None, line_prefix=None)
_BRANCH_BRANCH_SET = Branch(type=Variable(content='BranchSet'), rule=Sequence(rules=[MatchIn(type=Variable(content='Branch'), key=Variable(content='branches')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='NEWLINE')), MatchIn(type=Variable(content='Branch'), key=Variable(content='branches'))])))]), priority=None, line_prefix=None)

# GROUPS

_GROUP_EMPTY_GR = Group(type=Variable('EmptyGR'), types=[
    Variable('Valid'),
    Variable('Excluded'),
    Variable('Error')
])
_GROUP_MATCH_GR = Group(type=Variable('MatchGR'), types=[
    Variable('Match'),
    Variable('EmptyGR')
])
_GROUP_GROUPING_GR = Group(type=Variable('GroupingGR'), types=[
    Variable('Grouping'),
    Variable('MatchGR')
])
_GROUP_REPEAT_GR = Group(type=Variable('RepeatGR'), types=[
    Variable('Repeat'),
    Variable('GroupingGR')
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
    Variable('BranchSet'),
    Variable('Branch')
])
_GROUP_BUILDABLE = Group(type=Variable('Buildable'), types=[
    Variable('BranchGR'),
    Variable('ParallelGR')
])
_GROUP_ALL_GR = Group(type=Variable('AllGR'), types=[
    Variable('Buildable'),
    Variable('Group'),
    Variable('Ignore'),
    Variable('Include'),
    Variable('Inverted'),
    Variable('Integer'),
    Variable('String'),
    Variable('Variable')
])


reader = Reader(
    lexer=Lexer(
        patterns=[
            _STRING_WAVE,
            _STRING_PLUS,
            _KEYWORD_KW_IGNORE,
            _KEYWORD_KW_VALID,
            _KEYWORD_KW_EXCLUDED,
            _KEYWORD_KW_ERROR,
            _STRING_LB,
            _STRING_RB,
            _STRING_LS,
            _STRING_COMMA,
            _STRING_RS,
            _STRING_VBAR,
            _STRING_NEWLINE,
            _REGEX_VARIABLE,
            _REGEX_INTEGER,
            _REGEX_STRING,
            _REGEX_WHITESPACE,
            _STRING_SPACE
        ]
    ),
    parser=Parser(
        branches=[
            _BRANCH_INVERTED,
            _BRANCH_INCLUDE,
            _BRANCH_IGNORE,
            _BRANCH_GROUP,
            _BRANCH_VALID,
            _BRANCH_EXCLUDED,
            _BRANCH_ERROR,
            _GROUP_EMPTY_GR,
            _BRANCH_MATCH,
            _GROUP_MATCH_GR,
            _BRANCH_GROUPING,
            _GROUP_GROUPING_GR,
            _BRANCH_REPEAT,
            _GROUP_REPEAT_GR,
            _BRANCH_SEQUENCE,
            _GROUP_SEQUENCE_GR,
            _BRANCH_PARALLEL,
            _GROUP_PARALLEL_GR,
            _BRANCH_BRANCH,
            _BRANCH_BRANCH_SET,
            _GROUP_BRANCH_GR,
            _GROUP_BUILDABLE,
            _GROUP_ALL_GR
        ],
        start=Variable('BranchSet')
    )
)
