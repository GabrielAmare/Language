import typing

from website.language import optilex as ol
from website.language.base.decorators import *
from website.language.semi.lang.models import *
from website.language.semi.processing import make_origin_select


@__method__
def to_optilex(self: Group) -> ol.Charset:
    items = ol.String(content=repr(''.join(sorted(self.items.to_str()))))
    if isinstance(self.inverted, Inverted):
        inverted = ol.Inverted()
    else:
        inverted = None
    return ol.Charset(items=items, inverted=inverted)


@__method__
def to_optilex(self: ParallelGR) -> typing.Optional[ol.Include]:
    if isinstance(self, Valid):
        return ol.Include()
    elif isinstance(self, Excluded):
        return None
    else:
        raise TypeError(type(self))


@__method__
def to_optilex(self: Branch) -> ol.Action:
    include = self.rule.to_optilex()
    build = ol.Variable(self.type.content)
    goto = ol.Integer.from_int(0)
    if isinstance(self.ignore_, Ignore):
        clear = ol.Clear()
    else:
        clear = None
    return ol.Action(include_=include, build=build, goto=goto, clear=clear)


@__method__
def to_optilex_index(self: BranchSet, origins: list[BranchSet]) -> int:
    """Return the assigned index of `self`."""
    try:
        return origins.index(self.pre_processed)

    except ValueError:
        return -1


@__method__
def to_optilex_al(self: BranchSet, origins: list[BranchSet], origin: BranchSet) -> ol.ActionList:
    errors, excluded, included, continued = self.split_branches()

    if continued:
        goto = ol.Integer.from_int(self.to_optilex_index(origins))
        action = ol.Action(include_=ol.Include(), build=None, goto=goto, clear=None)
        actions = [action]

    elif included:
        included = Branch.keep_max_priority(included)
        actions = [branch.to_optilex() for branch in included]

    elif excluded:
        excluded = Branch.keep_max_priority(excluded)
        actions = [branch.to_optilex() for branch in excluded]

    else:
        if origin == origins[0]:  # no error on state=0
            error = None
        else:
            error_types = [branch.type.content for branch in self.branches]
            error_types = set(error_types)
            error_types = sorted(error_types)
            error = ol.Variable.from_str('!' + '|'.join(error_types))

        action = ol.Action(include_=ol.Include(), build=error, goto=ol.Integer.from_int(-1), clear=None)
        actions = [action]

    return ol.ActionList(actions)


@__method__
def to_optilex_gs(self: BranchSet, choice: list[tuple[Group, BranchSet]], origins: list[BranchSet]) -> ol.GroupSelect:
    default_group, default_target = choice.pop(-1)
    outcomes: list[ol.Outcome] = []
    for group, target in choice:
        charset: ol.Charset = group.to_optilex()
        actions: ol.ActionList = target.to_optilex_al(origins=origins, origin=self)
        outcome: ol.Outcome = ol.Outcome(charset=charset, actions=actions)
        outcomes.append(outcome)

    outcomes: list[ol.Outcome] = list(sorted(outcomes, key=ol.Outcome.order))
    default: ol.ActionList = default_target.to_optilex_al(origins=origins, origin=self)

    block: ol.Block = ol.Block(outcomes=outcomes, default=default)
    origin_index: ol.Integer = ol.Integer.from_int(self.to_optilex_index(origins))

    return ol.GroupSelect(origin=origin_index, block=block)


@__method__
def to_optilex(self: BranchSet) -> ol.OriginSelect:
    origins, choices = make_origin_select(self)
    cases = [origin.to_optilex_gs(choice=choice, origins=origins) for origin, choice in zip(origins, choices)]
    return ol.OriginSelect(cases=cases)
