from website.language.bnf.lang.models import *
from .lexing import Alias_Priority
from .patterns import *

__all__ = [
    'Branch_MatchAs',
    'Branch_MatchIn',
    'Group_MatchKeyGR',
    'Branch_Match',
    'Group_MatchGR',
    'Branch_Canonical',
    'Branch_Literal',
    'Group_AtomGR',
    'Branch_Grouping',
    'Group_GroupingGR',
    'Branch_Negative',
    'Group_NegativeGR',
    'Branch_Repeat',
    'Branch_RepeatStar',
    'Branch_RepeatPlus',
    'Branch_Optional',
    'Branch_Enum0',
    'Branch_Enum1',
    'Group_RepeatGR',
    'Branch_Sequence',
    'Group_SequenceGR',
    'Branch_Parallel',
    'Group_ParallelGR',
    'Alias_LinePrefix',
    'Branch_Branch',
    'Branch_Alias',
    'Branch_Group',
    'Group_BranchGR',
    'Group_Buildable',
    'Branch_Parser',
]

# PARSING
Branch_MatchAs = Branch(Variable('MatchAs'), Sequence([
    Literal(String("'<'")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Canonical(String("' '")),
    Literal(String("'as'")),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('key')),
    Literal(String("'>'"))
]))
Branch_MatchIn = Branch(Variable('MatchIn'), Sequence([
    Literal(String("'<'")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Canonical(String("' '")),
    Literal(String("'in'")),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('key')),
    Literal(String("'>'"))
]))
Group_MatchKeyGR = Group(Variable('MatchKeyGR'), [
    Branch_MatchAs.type,
    Branch_MatchIn.type
])
Branch_Match = Branch(Variable('Match'), Sequence([
    Literal(String("'<'")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Literal(String("'>'"))
]))
Group_MatchGR = Group(Variable('MatchGR'), [
    Group_MatchKeyGR.type,
    Branch_Match.type
])
Branch_Canonical = Branch(Variable('Canonical'), Sequence([
    Literal(String("'$'")),
    MatchAs(Regex_String.type, Variable('expr'))
]))
Branch_Literal = Branch(Variable('Literal'), Sequence([
    MatchAs(Regex_String.type, Variable('expr'))
]))
Group_AtomGR = Group(Variable('AtomGR'), [
    Branch_Canonical.type,
    Branch_Literal.type,
    Group_MatchGR.type,
])
# \/ always check \/
Branch_Grouping = Branch(Variable('Grouping'), Sequence([
    Literal(String("'['")),
    MatchAs(Variable('ParallelGR'), Variable('rule')),
    Literal(String("']'"))
]))
Group_GroupingGR = Group(Variable('GroupingGR'), [
    Branch_Grouping.type,
    Group_AtomGR.type
])
Branch_Negative = Branch(Variable('Negative'), Sequence([
    Literal(String("'!'")),
    MatchAs(Group_GroupingGR.type, Variable('rule')),
]))
Group_NegativeGR = Group(Variable('NegativeGR'), [
    Branch_Negative.type,
    Group_GroupingGR.type
])
Branch_Repeat = Branch(Variable('Repeat'), Sequence([
    Literal(String("'{'")),
    Optional(MatchAs(Regex_Integer.type, Variable('mn'))),
    Literal(String("','")),
    Optional(MatchAs(Regex_Integer.type, Variable('mx'))),
    Literal(String("'}'")),
    MatchAs(Group_NegativeGR.type, Variable('rule')),
]))
Branch_RepeatStar = Branch(Variable('RepeatStar'), Sequence([
    Literal(String("'*'")),
    MatchAs(Group_NegativeGR.type, Variable('rule')),
]))
Branch_RepeatPlus = Branch(Variable('RepeatPlus'), Sequence([
    Literal(String("'+'")),
    MatchAs(Group_NegativeGR.type, Variable('rule')),
]))
Branch_Optional = Branch(Variable('Optional'), Sequence([
    Literal(String("'?'")),
    MatchAs(Group_NegativeGR.type, Variable('rule')),
]))
Branch_Enum0 = Branch(Variable('Enum0'), Sequence([
    MatchAs(Group_NegativeGR.type, Variable('separator')),
    Literal(String("'.'")),
    MatchAs(Group_NegativeGR.type, Variable('element'))
]))
Branch_Enum1 = Branch(Variable('Enum1'), Sequence([
    MatchAs(Group_NegativeGR.type, Variable('separator')),
    Literal(String("'.'")),
    Literal(String("'.'")),
    MatchAs(Group_NegativeGR.type, Variable('element'))
]))
Group_RepeatGR = Group(Variable('RepeatGR'), [
    Branch_Repeat.type,
    Branch_RepeatStar.type,
    Branch_RepeatPlus.type,
    Branch_Optional.type,
    Branch_Enum0.type,
    Branch_Enum1.type,
    Group_NegativeGR.type
])
Branch_Sequence = Branch(Variable('Sequence'), Sequence([
    Enum1(Canonical(String("' '")), MatchIn(Group_RepeatGR.type, Variable('rules')))
]))
Group_SequenceGR = Group(Variable('SequenceGR'), [
    Branch_Sequence.type,
    Group_RepeatGR.type
])
Branch_Parallel = Branch(Variable('Parallel'), Sequence([
    Enum1(
        Grouping(Sequence([Canonical(String("' '")), Literal(String("'|'")), Canonical(String("' '"))])),
        MatchIn(Group_SequenceGR.type, Variable('rules'))
    )
]))
Group_ParallelGR = Group(Variable('ParallelGR'), [
    Branch_Parallel.type,
    Group_SequenceGR.type
])
Alias_LinePrefix = Alias(Variable('LinePrefixAL'), Optional(Grouping(Sequence([
    Canonical(String("' '")),
    MatchAs(Regex_String.type, Variable('line_prefix'))
]))))
Branch_Branch = Branch(Variable('Branch'), Sequence([
    Literal(String("'branch'")),
    Match(Alias_Priority.type),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Match(Alias_LinePrefix.type),
    Canonical(String("' '")),
    Literal(String("':='")),
    Canonical(String("' '")),
    MatchAs(Group_ParallelGR.type, Variable('rule'))
]))
Branch_Alias = Branch(Variable('Alias'), Sequence([
    Literal(String("'alias'")),
    Canonical(String("' '")),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Match(Alias_LinePrefix.type),
    Canonical(String("' '")),
    Literal(String("':='")),
    Canonical(String("' '")),
    MatchAs(Group_ParallelGR.type, Variable('rule'))
]))
Branch_Group = Branch(Variable('Group'), Sequence([
    Literal(String("'group'")),
    Canonical(String("' '")),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('type')),
    Canonical(String("' '")),
    Literal(String("':='")),
    Canonical(String("' '")),
    Enum0(
        Grouping(Sequence([Canonical(String("' '")), Literal(String("'|'")), Canonical(String("' '"))])),
        MatchIn(Regex_Variable.type, Variable('types'))
    )
]))
Group_BranchGR = Group(Variable('BranchGR'), [
    Branch_Branch.type,
    Branch_Alias.type,
    Branch_Group.type
])
Group_Buildable = Group(Variable('Buildable'), [
    Group_BranchGR.type,
    Group_ParallelGR.type
])
Branch_Parser = Branch(Variable('Parser'), Sequence([
    Enum0(
        Canonical(String("'\\n'")),
        MatchIn(Group_BranchGR.type, Variable('branches'))
    ),
    Canonical(String("'\\n'")),
    Canonical(String("'\\n'")),
    Literal(String("'>'")),
    Canonical(String("' '")),
    MatchAs(Regex_Variable.type, Variable('start'))
]))
