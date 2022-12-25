import dataclasses

__all__ = [
    'Caster',
    'CAST_TO_VAR',
    'CAST_TO_STRING',
    'CAST_TO_BOOL',
]


@dataclasses.dataclass
class Caster:
    name: str
    default: bool | str | int | float | None = None


CAST_TO_VAR = Caster(
    name='str',
)
CAST_TO_STRING = Caster(
    name='str',
)
CAST_TO_BOOL = Caster(
    name='bool',
    default=False,
)
