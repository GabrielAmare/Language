from website.language.bnf.lang.models import *
from .patterns import *

__all__ = [
    'Branch_IGNORE',
    'Alias_Priority',
    'Alias_Ignore',
    'Alias_BasePattern',
    'Branch_StringPattern',
    'Branch_RegexPattern',
    'Branch_KeywordPattern',
    'Group_PatternGR',
    'Branch_Lexer',
]

Branch_IGNORE = Branch(Variable('Ignore'), Literal(String("'ignore'")))
Alias_Priority = Alias(Variable('PriorityAL'), Optional(Grouping(Sequence([
    Literal(String("'['")),
    MatchAs(Regex_Integer.type, Variable('priority')),
    Literal(String("']'"))
]))))
Alias_Ignore = Alias(Variable('IgnoreAL'), Optional(Grouping(Sequence([
    Canonical(String("' '")),
    MatchAs(Branch_IGNORE.type, Variable('ignore_'))
]))))
Alias_BasePattern = Alias(Variable('BasePattern'), Sequence([
    Match(Alias_Priority.type),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Optional(Grouping(Sequence([
        Literal(String("'('")),
        MatchAs(Regex_Variable.type, Variable('cast')),
        Literal(String("')'")),
    ]))),
    Canonical(String("' '")),
    MatchAs(Regex_String.type, Variable('expr')),
]))
Branch_StringPattern = Branch(Variable('StringPattern'), Sequence([
    Literal(String("'string'")),
    Canonical(String("' '")),
    Match(Alias_BasePattern.type),
    Match(Alias_Ignore.type)
]))
Branch_RegexPattern = Branch(Variable('RegexPattern'), Sequence([
    Literal(String("'regex'")),
    Canonical(String("' '")),
    Canonical(String("' '")),
    Match(Alias_BasePattern.type),
    Optional(Grouping(Sequence([
        Canonical(String("' '")),
        MatchAs(Regex_Integer.type, Variable('flags'))
    ]))),
    Match(Alias_Ignore.type)
]))
Branch_KeywordPattern = Branch(Variable('KeywordPattern'), Sequence([
    Literal(String("'keyword'")),
    Match(Alias_BasePattern.type),
    Match(Alias_Ignore.type)
]))
Group_PatternGR = Group(Variable('PatternGR'), [
    Branch_StringPattern.type,
    Branch_RegexPattern.type,
    Branch_KeywordPattern.type
])
Branch_Lexer = Branch(Variable('Lexer'), Sequence([
    Enum0(
        Canonical(String("'\\n'")),
        MatchIn(Group_PatternGR.type, Variable('patterns'))
    )
]))
