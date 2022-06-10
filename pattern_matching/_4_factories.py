from ._1_elements import *
from ._3_patterns import *

__all__ = [
    'sequence',
    'repeat',
    'optional',
    'atom',
    'match',
    'match_as',
    'match_in'
]

sequence = PatternSequence
repeat = PatternRepeat
optional = PatternOptional
atom = AtomPattern


def match(__type: str) -> AtomPattern:
    return AtomPattern(
        function=Element.is_typed_as(__type),
    )


def match_as(__type: str, __key: str) -> AtomPattern:
    return AtomPattern(
        function=Element.is_typed_as(__type),
        action=Context.set_as_for(__key)
    )


def match_in(__type: str, __key: str) -> AtomPattern:
    return AtomPattern(
        function=Element.is_typed_as(__type),
        action=Context.add_in_for(__key)
    )
