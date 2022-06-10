import operator
import typing

from website.language.utils import resume_to_dict
from website.language.semi.imports.constants import *
from website.language.semi.lang.models import *

__all__ = [
    'decouple_iter',
    'decouple_dict',
    'simplify_iter',
    'make_origin_select',
]

_PROCESS_RESULT = typing.Iterator[tuple[Group, BranchSet]]
_GROUP_SELECT = typing.Dict[Group, BranchSet]

_STI = typing.Dict[typing.FrozenSet[int], list[str]]
_STG = typing.Dict[typing.FrozenSet[int], Group]


def decouple_iter(result: _PROCESS_RESULT) -> typing.Iterator[tuple[Group, BranchSet]]:
    """This makes sure that no groups intersect and that there's only one group which is inverted (the default one)."""
    # the last (group, branch_set) pair is always the default group^(which is inverted)
    groups, targets = map(list, zip(*result))

    alphabet = frozenset(item for group in groups for items in group.to_frozenset() for item in items)

    def _get_signature_to_items() -> typing.Iterator[tuple[typing.FrozenSet[int], str]]:
        return [
            (frozenset(index for index, group in enumerate(groups) if item in group), item)
            for item in alphabet
        ]

    sign_to_items: _STI = resume_to_dict(_get_signature_to_items())

    sign_to_group: _STG = {
        signature: Group.from_frozenset(items=frozenset(items), inverted=False)
        for signature, items in sign_to_items.items()
    }

    default_signature = frozenset(index for index, group in enumerate(groups) if group.is_inverted)
    default_group = Group.union(
        Group.from_frozenset(alphabet, inverted=True),
        sign_to_group.pop(default_signature, NEVER)
    )

    def _make_branch_set(signature: typing.FrozenSet[int]) -> BranchSet:
        return BranchSet.from_branches(map(targets.__getitem__, signature))

    for signature, group in sign_to_group.items():
        assert not group.is_inverted
        yield group, _make_branch_set(signature)

    assert default_group.is_inverted
    yield default_group, _make_branch_set(default_signature)


def decouple_dict(result: _PROCESS_RESULT) -> tuple[_GROUP_SELECT, Group, BranchSet]:
    """This makes sure that no groups intersect and that there's only one group which is inverted (the default one)."""

    pairs: list[tuple[Group, BranchSet]] = list(decouple_iter(result))

    group_select = dict(pairs[:-1])
    default_group, default_branch_set = pairs[-1]

    return group_select, default_group, default_branch_set


def simplify_iter(
        result: typing.Iterator[tuple[Group, BranchSet]]
) -> typing.Iterator[tuple[Group, BranchSet]]:
    for group, target in result:
        yield group, target.simplified


_BLOCK = tuple[_GROUP_SELECT, BranchSet]
_ORIGIN_SELECT = typing.Dict[BranchSet, _BLOCK]

E = typing.TypeVar('E')
F = typing.TypeVar('F')


def develop_tree(
        root: E,
        generate: typing.Callable[[E], F],
        get_targets: typing.Callable[[F], list[E]],
        can_be_origin: typing.Callable[[E], bool],
        as_origin: typing.Callable[[E], E]
) -> tuple[list[E], list[F]]:
    origins: list[E] = [root]
    choices: list[F] = []

    def add_origin(item: E) -> None:
        if item not in origins:
            origins.append(item)

    index = 0
    while index < len(origins):
        assert len(choices) == index
        choice = generate(origins[index])
        choices.append(choice)

        for target in get_targets(choice):
            if can_be_origin(target):
                origin = as_origin(target)
                add_origin(origin)

        index += 1

    return origins, choices


_ORIGIN = _TARGET = BranchSet
_ORIGINS = list[_ORIGIN]
_TARGETS = list[_TARGET]
_CHOICE = list[tuple[Group, _TARGET]]
_CHOICES = list[_CHOICE]


def make_origin_select(root: BranchSet) -> tuple[list[BranchSet], list[list[tuple[Group, BranchSet]]]]:
    def generate(origin: _ORIGIN) -> _CHOICE:
        result = origin.process()
        result = decouple_iter(result)
        result = simplify_iter(result)
        return list(result)

    def get_targets(result: _CHOICE) -> _TARGETS:
        return sorted([target for group, target in result], key=operator.attrgetter('order_key'))

    def can_be_origin(target: _TARGET) -> bool:
        return target.branches and not target.is_terminal

    # TODO : remove when Error class is removed
    def as_origin(target: _TARGET) -> _ORIGIN:
        return target.pre_processed

    origins, choices = develop_tree(
        root=root,
        generate=generate,
        get_targets=get_targets,
        can_be_origin=can_be_origin,
        as_origin=as_origin
    )

    return origins, choices


def _make_origin_select(root: BranchSet) -> tuple[list[BranchSet], _ORIGIN_SELECT]:
    origins: list[BranchSet] = [root]
    cases: typing.Dict[BranchSet, _BLOCK] = {}

    index = 0

    while index < len(origins):
        origin = origins[index]

        # DETERMINE THE RESULTS
        result = origin.process()
        result = decouple_iter(result)
        result = simplify_iter(result)
        result = list(result)

        # REGISTER RESULT IN MAPPING
        *pairs, default = result
        group_select = dict(pairs)
        default_group, default_target = default
        cases[origin] = (group_select, default_target)

        # REGISTER NEW ORIGINS
        for group, target in result:
            if not target.is_terminal:
                origin = target.pre_processed
                if origin not in origins:
                    origins.append(origin)

        index += 1

    return origins, cases
