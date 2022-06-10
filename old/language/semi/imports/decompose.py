import operator
import typing

from website.language.semi.lang import *
from website.language.utils import resume_to_dict
from website.language.base.decorators import *
from website.language.utils import develop_tree

_STI = typing.Dict[typing.FrozenSet[int], list[str]]
_STG = typing.Dict[typing.FrozenSet[int], Group]


@__class_method__
def decouple_iter(cls: BranchSet.__class__, result: typing.Iterator[tuple[Group, BranchSet]]
                  ) -> typing.Iterator[tuple[Group, BranchSet]]:
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


@__class_method__
def get_targets(cls: BranchSet.__class__, result: list[tuple[Group, BranchSet]]) -> list[BranchSet]:
    targets = [target for group, target in result]
    return sorted(targets, key=operator.attrgetter('order_key'))


@__method__
def can_be_origin(self: BranchSet) -> bool:
    return self.branches and not self.is_terminal


# TODO : remove when Error class is removed
@__method__
def as_origin(self: BranchSet) -> BranchSet:
    return self.pre_processed


@__method__
def make_origin_select(self: BranchSet) -> tuple[list[BranchSet], list[list[tuple[Group, BranchSet]]]]:
    def generate(origin: BranchSet) -> list[tuple[Group, BranchSet]]:
        result = origin.process()
        result = BranchSet.decouple_iter(result)
        result = [(group, target.simplified) for group, target in result]
        return list(result)

    origins, choices = develop_tree(
        root=self,
        generate=generate,
        get_targets=get_targets,
        can_be_origin=can_be_origin,
        as_origin=as_origin
    )

    return origins, choices
