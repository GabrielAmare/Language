from core.langs.bnf.lang.models import *
from .lexing import *
from .parsing import *
from .patterns import *

__all__ = [
    'reader'
]

Group_TopLevel = Group(Variable('TopLevel'), [
    Group_BranchGR.type,
    Group_PatternGR.type
])


# READING
Branch_Reader = Branch(Variable('Reader'), Sequence([
    MatchAs(Branch_Lexer.type, Variable('lexer')),
    Canonical(String("'\\n'")),
    Canonical(String("'\\n'")),
    MatchAs(Branch_Parser.type, Variable('parser'))
]))

Group_All = Group(Variable('All'), [
    Regex_String.type,
    Regex_Variable.type,
    Regex_Integer.type,
    Branch_IGNORE.type,
    Group_TopLevel.type,
    Group_Buildable.type,
    Branch_Lexer.type,
    Branch_Parser.type,
    Branch_Reader.type
])

reader = Reader(
    lexer=Lexer(
        patterns=[
            Regex_String,
            Regex_Integer,
            Regex_Variable,
            Regex_WHITESPACE,
            Regex_COMMENT
        ]
    ),
    parser=Parser(
        branches=[
            # LEXING
            Alias_Priority,
            Alias_Ignore,
            Alias_BasePattern,
            Branch_IGNORE,
            Branch_StringPattern,
            Branch_RegexPattern,
            Branch_KeywordPattern,
            Group_PatternGR,
            Branch_Lexer,
            # PARSING
            Branch_MatchAs,
            Branch_MatchIn,
            Group_MatchKeyGR,
            Branch_Match,
            Group_MatchGR,
            Branch_Canonical,
            Branch_Literal,
            Group_AtomGR,
            Branch_Grouping,
            Group_GroupingGR,
            Branch_Negative,
            Group_NegativeGR,
            Branch_Repeat,
            Branch_RepeatStar,
            Branch_RepeatPlus,
            Branch_Optional,
            Branch_Enum0,
            Branch_Enum1,
            Group_RepeatGR,
            Branch_Sequence,
            Group_SequenceGR,
            Branch_Parallel,
            Group_ParallelGR,
            Alias_LinePrefix,
            Branch_Branch,
            Branch_Alias,
            Branch_Group,
            Group_BranchGR,
            Group_Buildable,
            Group_TopLevel,
            Branch_Parser,
            # READING
            Branch_Reader,
            # ALL
            Group_All,
        ],
        start=Branch_Reader.type
    )
)
