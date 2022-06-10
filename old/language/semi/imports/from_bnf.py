from website.language import bnf, regex
from website.language.base.decorators import *
from website.language.semi.lang.models import *


@__class_method__
def from_bnf(cls: ParallelGR.__class__, obj: bnf.PatternGR) -> ParallelGR:
    if isinstance(obj, (bnf.StringPattern, bnf.KeywordPattern)):
        rules = [Match(Group(String(repr(char)))) for char in obj.expr.value]
        return Sequence.from_rules(rules=rules)

    elif isinstance(obj, bnf.RegexPattern):
        regex_pattern = regex.engine(obj.expr.value)
        return cls.from_regex(regex_pattern)

    else:
        raise NotImplementedError(type(obj))


@__class_method__
def from_bnf(cls: Branch.__class__, obj: bnf.PatternGR) -> Branch:
    type_ = Variable(str(obj.type))
    rule = ParallelGR.from_bnf(obj)
    if obj.priority:
        priority = Integer(obj.priority.content)
    else:
        priority = None
    return cls(type=type_, rule=rule, priority=priority)


@__class_method__
def from_bnf(cls: BranchSet.__class__, obj: bnf.Lexer) -> BranchSet:
    branches = list(map(Branch.from_bnf, obj.patterns))
    return cls(branches=branches)
