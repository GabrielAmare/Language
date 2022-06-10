import typing

from website.language import regex
from website.language.base.decorators import *
from website.language.semi.lang.models import *


@__class_method__
def from_regex(cls: Integer.__class__, obj: typing.Optional[regex.Integer]) -> typing.Optional[Integer]:
    if isinstance(obj, regex.Integer):
        return cls(content=''.join(digit.content for digit in obj.digits))

    else:
        return None


@__class_method__
def from_regex(cls: Group.__class__, obj: regex.GroupInnerGR) -> Group:
    charset = obj.as_outer_charset
    items = String(content=repr(''.join(sorted(charset.items))))
    inverted = Inverted() if charset.inverted else None
    return cls(items=items, inverted=inverted)


@__class_method__
def from_regex(cls: ParallelGR.__class__, obj: regex.ParallelGR) -> ParallelGR:
    if isinstance(obj, regex.GroupInnerGR):
        return Match(Group.from_regex(obj))

    elif isinstance(obj, regex.Parallel):
        return Parallel.from_rules(rules=map(cls.from_regex, obj.items))

    elif isinstance(obj, (regex.Sequence, regex.GroupOuter, regex.GroupIgnore)):
        return Sequence.from_rules(rules=map(cls.from_regex, obj.items))

    elif isinstance(obj, regex.Repeat):
        return cls.from_regex(obj.item).as_repeat(mn=Integer.from_regex(obj.mn), mx=Integer.from_regex(obj.mx))

    elif isinstance(obj, regex.Optional):
        return cls.from_regex(obj.item).as_repeat(mn=Integer.from_int(0), mx=Integer.from_int(1))

    elif isinstance(obj, (regex.RepeatStar, regex.LazyRepeatStar)):
        return cls.from_regex(obj.item).as_repeat(mn=Integer.from_int(0), mx=Integer.from_int(0))

    elif isinstance(obj, (regex.RepeatPlus, regex.LazyRepeatPlus)):
        return cls.from_regex(obj.item).as_repeat(mn=Integer.from_int(1), mx=Integer.from_int(0))

    elif isinstance(obj, regex.NegativeLookBehind):
        return cls.from_regex(obj.rule)  # TODO : handle negative look behind

    else:
        raise NotImplementedError(type(obj))
