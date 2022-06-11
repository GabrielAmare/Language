"""Auto generated module.Any manual changes might be overwritten."""
from core.langs.bnf.lang.base.models import *

__all__ = [
    'reader'
]
# PATTERNS

_STRING_LB = StringPattern(type=Variable(content='LB'), expr=String(content="'['"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RB = StringPattern(type=Variable(content='RB'), expr=String(content="']'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_HAT = StringPattern(type=Variable(content='HAT'), expr=String(content="'^'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LEFT_PARENTHESIS = StringPattern(type=Variable(content='LEFT_PARENTHESIS'), expr=String(content="'('"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_INT = StringPattern(type=Variable(content='INT'), expr=String(content="'?'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EQ = StringPattern(type=Variable(content='EQ'), expr=String(content="'='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RIGHT_PARENTHESIS = StringPattern(type=Variable(content='RIGHT_PARENTHESIS'), expr=String(content="')'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EXC = StringPattern(type=Variable(content='EXC'), expr=String(content="'!'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LV = StringPattern(type=Variable(content='LV'), expr=String(content="'<'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COLON = StringPattern(type=Variable(content='COLON'), expr=String(content="':'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_ASTERISK = StringPattern(type=Variable(content='ASTERISK'), expr=String(content="'*'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_PLUS = StringPattern(type=Variable(content='PLUS'), expr=String(content="'+'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LS = StringPattern(type=Variable(content='LS'), expr=String(content="'{'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COMMA = StringPattern(type=Variable(content='COMMA'), expr=String(content="','"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RS = StringPattern(type=Variable(content='RS'), expr=String(content="'}'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_VBAR = StringPattern(type=Variable(content='VBAR'), expr=String(content="'|'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_ANY_DIGIT = StringPattern(type=Variable(content='AnyDigit'), expr=String(content="'\\d'"), priority=Integer(content='5'), cast=None, ignore_=None)
_STRING_ANY_NON_DIGIT = StringPattern(type=Variable(content='AnyNonDigit'), expr=String(content="'\\D'"), priority=Integer(content='5'), cast=None, ignore_=None)
_STRING_ANY_WHITESPACE = StringPattern(type=Variable(content='AnyWhitespace'), expr=String(content="'\\s'"), priority=Integer(content='5'), cast=None, ignore_=None)
_STRING_ANY_NON_WHITESPACE = StringPattern(type=Variable(content='AnyNonWhitespace'), expr=String(content="'\\S'"), priority=Integer(content='5'), cast=None, ignore_=None)
_STRING_ANY_WORD = StringPattern(type=Variable(content='AnyWord'), expr=String(content="'\\w'"), priority=Integer(content='5'), cast=None, ignore_=None)
_STRING_ANY_NON_WORD = StringPattern(type=Variable(content='AnyNonWord'), expr=String(content="'\\W'"), priority=Integer(content='5'), cast=None, ignore_=None)
_STRING_DASH = StringPattern(type=Variable(content='Dash'), expr=String(content="'-'"), priority=Integer(content='4'), cast=None, ignore_=None)
_STRING_DOT = StringPattern(type=Variable(content='Dot'), expr=String(content="'.'"), priority=Integer(content='4'), cast=None, ignore_=None)
_REGEX_CHARACTER = RegexPattern(type=Variable(content='Character'), expr=String(content="'.'"), priority=Integer(content='3'), cast=None, ignore_=None, flags=None)
_REGEX_DIGIT = RegexPattern(type=Variable(content='Digit'), expr=String(content="'\\d'"), priority=Integer(content='2'), cast=None, ignore_=None, flags=None)
_REGEX_ESCAPED_CHARACTER = RegexPattern(type=Variable(content='EscapedCharacter'), expr=String(content="'\\\\\\\\.'"), priority=Integer(content='1'), cast=None, ignore_=None, flags=None)
_REGEX_WHITESPACE = RegexPattern(type=Variable(content='WHITESPACE'), expr=String(content="'\\s+'"), priority=Integer(content='10'), cast=None, ignore_=Ignore(), flags=None)

# BRANCHES

_BRANCH_INTEGER = Branch(type=Variable(content='Integer'), rule=Sequence(rules=[MatchIn(type=Variable(content='Digit'), key=Variable(content='digits')), RepeatStar(rule=MatchIn(type=Variable(content='Digit'), key=Variable(content='digits')))]), priority=None, line_prefix=None)
_BRANCH_RANGE = Branch(type=Variable(content='Range'), rule=Sequence(rules=[MatchAs(type=Variable(content='CharacterGR'), key=Variable(content='start')), Match(type=Variable(content='Dash')), MatchAs(type=Variable(content='CharacterGR'), key=Variable(content='end'))]), priority=None, line_prefix=None)
_BRANCH_GROUP_INNER = Branch(type=Variable(content='GroupInner'), rule=Sequence(rules=[Match(type=Variable(content='LB')), RepeatStar(rule=MatchIn(type=Variable(content='RangeGR'), key=Variable(content='items'))), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_GROUP_INNER_NOT = Branch(type=Variable(content='GroupInnerNot'), rule=Sequence(rules=[Match(type=Variable(content='LB')), Match(type=Variable(content='HAT')), RepeatStar(rule=MatchIn(type=Variable(content='RangeGR'), key=Variable(content='items'))), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_POSITIVE_LOOK_AHEAD = Branch(type=Variable(content='PositiveLookAhead'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), Match(type=Variable(content='INT')), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_NEGATIVE_LOOK_AHEAD = Branch(type=Variable(content='NegativeLookAhead'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), Match(type=Variable(content='INT')), Match(type=Variable(content='EXC')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_POSITIVE_LOOK_BEHIND = Branch(type=Variable(content='PositiveLookBehind'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), Match(type=Variable(content='INT')), Match(type=Variable(content='LV')), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_NEGATIVE_LOOK_BEHIND = Branch(type=Variable(content='NegativeLookBehind'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), Match(type=Variable(content='INT')), Match(type=Variable(content='LV')), Match(type=Variable(content='EXC')), MatchAs(type=Variable(content='ParallelGR'), key=Variable(content='rule')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_GROUP_IGNORE = Branch(type=Variable(content='GroupIgnore'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), Match(type=Variable(content='INT')), Match(type=Variable(content='COLON')), RepeatStar(rule=MatchIn(type=Variable(content='ParallelGR'), key=Variable(content='items'))), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_GROUP_OUTER = Branch(type=Variable(content='GroupOuter'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), RepeatStar(rule=MatchIn(type=Variable(content='ParallelGR'), key=Variable(content='items'))), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_LAZY_REPEAT_STAR = Branch(type=Variable(content='LazyRepeatStar'), rule=Sequence(rules=[MatchAs(type=Variable(content='GroupOuterGR'), key=Variable(content='item')), Match(type=Variable(content='ASTERISK')), Match(type=Variable(content='INT'))]), priority=None, line_prefix=None)
_BRANCH_LAZY_REPEAT_PLUS = Branch(type=Variable(content='LazyRepeatPlus'), rule=Sequence(rules=[MatchAs(type=Variable(content='GroupOuterGR'), key=Variable(content='item')), Match(type=Variable(content='PLUS')), Match(type=Variable(content='INT'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT_STAR = Branch(type=Variable(content='RepeatStar'), rule=Sequence(rules=[MatchAs(type=Variable(content='GroupOuterGR'), key=Variable(content='item')), Match(type=Variable(content='ASTERISK'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT_PLUS = Branch(type=Variable(content='RepeatPlus'), rule=Sequence(rules=[MatchAs(type=Variable(content='GroupOuterGR'), key=Variable(content='item')), Match(type=Variable(content='PLUS'))]), priority=None, line_prefix=None)
_BRANCH_REPEAT = Branch(type=Variable(content='Repeat'), rule=Sequence(rules=[MatchAs(type=Variable(content='GroupOuterGR'), key=Variable(content='item')), Match(type=Variable(content='LS')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='mn'))), Match(type=Variable(content='COMMA')), Optional(rule=MatchAs(type=Variable(content='Integer'), key=Variable(content='mx'))), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_OPTIONAL = Branch(type=Variable(content='Optional'), rule=Sequence(rules=[MatchAs(type=Variable(content='GroupOuterGR'), key=Variable(content='item')), Match(type=Variable(content='INT'))]), priority=None, line_prefix=None)
_BRANCH_SEQUENCE = Branch(type=Variable(content='Sequence'), rule=Sequence(rules=[MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='items')), MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='items')), RepeatStar(rule=MatchIn(type=Variable(content='RepeatGR'), key=Variable(content='items')))]), priority=None, line_prefix=None)
_BRANCH_PARALLEL = Branch(type=Variable(content='Parallel'), rule=Sequence(rules=[MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='items')), Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='VBAR')), MatchIn(type=Variable(content='SequenceGR'), key=Variable(content='items'))])))]), priority=None, line_prefix=None)

# GROUPS

_GROUP_CHARACTER_GR = Group(type=Variable('CharacterGR'), types=[
    Variable('Dot'),
    Variable('Dash'),
    Variable('Digit'),
    Variable('Character')
])
_GROUP_ATOM_GR = Group(type=Variable('AtomGR'), types=[
    Variable('AnyDigit'),
    Variable('AnyWhitespace'),
    Variable('AnyWord'),
    Variable('AnyNonDigit'),
    Variable('AnyNonWhitespace'),
    Variable('AnyNonWord'),
    Variable('EscapedCharacter'),
    Variable('CharacterGR')
])
_GROUP_RANGE_GR = Group(type=Variable('RangeGR'), types=[
    Variable('Range'),
    Variable('AtomGR')
])
_GROUP_GROUP_INNER_GR = Group(type=Variable('GroupInnerGR'), types=[
    Variable('GroupInner'),
    Variable('GroupInnerNot'),
    Variable('AtomGR')
])
_GROUP_GROUP_OUTER_GR = Group(type=Variable('GroupOuterGR'), types=[
    Variable('PositiveLookAhead'),
    Variable('NegativeLookAhead'),
    Variable('PositiveLookBehind'),
    Variable('NegativeLookBehind'),
    Variable('GroupIgnore'),
    Variable('GroupOuter'),
    Variable('GroupInnerGR')
])
_GROUP_REPEAT_GR = Group(type=Variable('RepeatGR'), types=[
    Variable('LazyRepeatStar'),
    Variable('LazyRepeatPlus'),
    Variable('RepeatStar'),
    Variable('RepeatPlus'),
    Variable('Repeat'),
    Variable('Optional'),
    Variable('GroupOuterGR')
])
_GROUP_SEQUENCE_GR = Group(type=Variable('SequenceGR'), types=[
    Variable('Sequence'),
    Variable('RepeatGR')
])
_GROUP_PARALLEL_GR = Group(type=Variable('ParallelGR'), types=[
    Variable('Parallel'),
    Variable('SequenceGR')
])
_GROUP_ALL_GR = Group(type=Variable('AllGR'), types=[
    Variable('ParallelGR'),
    Variable('Integer')
])


reader = Reader(
    lexer=Lexer(
        patterns=[
            _STRING_LB,
            _STRING_RB,
            _STRING_HAT,
            _STRING_LEFT_PARENTHESIS,
            _STRING_INT,
            _STRING_EQ,
            _STRING_RIGHT_PARENTHESIS,
            _STRING_EXC,
            _STRING_LV,
            _STRING_COLON,
            _STRING_ASTERISK,
            _STRING_PLUS,
            _STRING_LS,
            _STRING_COMMA,
            _STRING_RS,
            _STRING_VBAR,
            _STRING_ANY_DIGIT,
            _STRING_ANY_NON_DIGIT,
            _STRING_ANY_WHITESPACE,
            _STRING_ANY_NON_WHITESPACE,
            _STRING_ANY_WORD,
            _STRING_ANY_NON_WORD,
            _STRING_DASH,
            _STRING_DOT,
            _REGEX_CHARACTER,
            _REGEX_DIGIT,
            _REGEX_ESCAPED_CHARACTER,
            _REGEX_WHITESPACE
        ]
    ),
    parser=Parser(
        branches=[
            _BRANCH_INTEGER,
            _GROUP_CHARACTER_GR,
            _GROUP_ATOM_GR,
            _BRANCH_RANGE,
            _GROUP_RANGE_GR,
            _BRANCH_GROUP_INNER,
            _BRANCH_GROUP_INNER_NOT,
            _GROUP_GROUP_INNER_GR,
            _BRANCH_POSITIVE_LOOK_AHEAD,
            _BRANCH_NEGATIVE_LOOK_AHEAD,
            _BRANCH_POSITIVE_LOOK_BEHIND,
            _BRANCH_NEGATIVE_LOOK_BEHIND,
            _BRANCH_GROUP_IGNORE,
            _BRANCH_GROUP_OUTER,
            _GROUP_GROUP_OUTER_GR,
            _BRANCH_LAZY_REPEAT_STAR,
            _BRANCH_LAZY_REPEAT_PLUS,
            _BRANCH_REPEAT_STAR,
            _BRANCH_REPEAT_PLUS,
            _BRANCH_REPEAT,
            _BRANCH_OPTIONAL,
            _GROUP_REPEAT_GR,
            _BRANCH_SEQUENCE,
            _GROUP_SEQUENCE_GR,
            _BRANCH_PARALLEL,
            _GROUP_PARALLEL_GR,
            _GROUP_ALL_GR
        ],
        start=Variable('ParallelGR')
    )
)
