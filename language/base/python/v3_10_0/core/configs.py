from __future__ import annotations

import dataclasses

from .linting import LintRule

__all__ = [
    'Environment',
]


@dataclasses.dataclass
class Environment:
    """Representation of the python environment."""
    version: tuple[int, int, int]
    builtins: list[str]
    # TODO: implement a nomenclature for the style rules.
    style: dict[str, bool] = dataclasses.field(default_factory=dict)
    
    def lint(self, key: LintRule) -> bool:
        try:
            return self.style[key]
        
        except KeyError:
            return False
    
    @classmethod
    def default(cls, version: tuple[int, int, int]) -> Environment:
        if version >= (3, 10, 0):
            return cls(
                version=version,
                builtins=[
                    'abc',
                    'typing',
                    'dataclasses',
                    'itertools',
                    'functools',
                    'collections',
                ]
            )
        
        raise ValueError(f"No default environment defined for version {version!r}")
