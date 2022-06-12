import enum
import re
import typing

__all__ = [
    'Styles',
    'matches',
    'convert'
]


class Styles(int, enum.Enum):
    PASCAL_CASE = 0
    SCREAM_CASE = 1
    SNAKE_CASE = 2
    MIXIN_CASE = 3


_STYLE_TO_PATTERN = {
    Styles.PASCAL_CASE: re.compile(r"^(?:[A-Z][a-z0-9]*)+$"),
    Styles.SCREAM_CASE: re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z][A-Z0-9]*)*$"),
    Styles.SNAKE_CASE: re.compile(r"^[a-z][a-z0-9]*(?:_[a-z][a-z0-9]*)*$"),
}


def _pascal_case_to_snake_case(__expr: str) -> str:
    result = ''
    last = False
    for index, char in enumerate(__expr):
        if char.isupper():
            if index and not last:
                result += '_'
            last = True
        else:
            last = False

        result += char.lower()
    return result


def _scream_case_to_snake_case(__expr: str) -> str:
    return __expr.lower()


def _pascal_case_to_scream_case(__expr: str) -> str:
    result = ''
    last = False
    for index, char in enumerate(__expr):
        if char.isupper():
            if index and not last:
                result += '_'
            last = True
        else:
            last = False

        result += char.upper()
    return result


_CONVERTERS = {
    (Styles.PASCAL_CASE, Styles.SNAKE_CASE): _pascal_case_to_snake_case,
    (Styles.SCREAM_CASE, Styles.SNAKE_CASE): _scream_case_to_snake_case,
    (Styles.PASCAL_CASE, Styles.SCREAM_CASE): _pascal_case_to_scream_case,
}


def _get_converter(src: Styles, dst: Styles) -> typing.Callable[[str], str]:
    try:
        return _CONVERTERS[(src, dst)]

    except KeyError:
        raise ValueError(f"No converter from {src.name!r} to {dst.name!r}.")


def _get_regex(style: Styles) -> re.Pattern:
    if not isinstance(style, Styles):
        raise TypeError(f"Invalid case style provided {style!r} (should be {Styles.__qualname__!r} member).")

    try:
        return _STYLE_TO_PATTERN[style]

    except KeyError:
        raise ValueError(f"Undefined regex pattern for {style.name!r}")


def matches(expression: str, style: Styles) -> bool:
    """Return True when the given `expression` matches the case `style`."""
    pattern = _get_regex(style)
    match = pattern.match(expression)
    return bool(match)


def convert(expression: str, src: Styles, dst: Styles) -> str:
    """Convert an `expression` from a given case style to another."""
    if not matches(expression, src):
        raise ValueError(f"The expression {expression!r} does not match {src!r} case style.")

    if src is dst:
        return expression

    converter = _get_converter(src, dst)

    return converter(expression)
