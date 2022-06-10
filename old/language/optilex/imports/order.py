import typing

from website.language.base.decorators import *
from ..lang.models import *


@__method__
def order(self: Charset) -> tuple[int, str]:
    """Return the key to order `Charset` objects."""
    content = ''.join(sorted(self.items.value))
    size = len(content)
    return size, content


@__method__
def order(self: Action) -> tuple[int, int, int, int]:
    """Return the key to order `Action` objects."""
    x = 0 if self.build else 1
    y = 0 if self.include_ else 1
    z, t = (0, self.goto.value) if self.goto else (1, 0)
    return x, y, z, t


@__method__
def order(self: ActionList) -> tuple[int, tuple[tuple[int, int, int, int], ...]]:
    """Return the key to order `ActionList` objects."""
    return len(self.items), tuple(map(Action.order, self.items))


@__method__
def order(self: Outcome) -> tuple[int, int, tuple[tuple[int, int, int, int], ...], str]:
    """Return the key to order `Outcome` objects."""
    n_chars, content = self.charset.order()
    n_actions, args = self.actions.order()
    return n_chars, n_actions, args, content
