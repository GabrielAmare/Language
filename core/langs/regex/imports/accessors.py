import string
import typing

from base.decorators import *
from base.groups import Charset
from core.langs.regex.lang.base.models import *


@__property__
def as_char(self: AtomGR) -> str:
    """Return the character corresponding to `self`."""
    if isinstance(self, CharacterGR):
        assert len(self.content) == 1, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[0]

    elif isinstance(self, (EscapedCharacter, AnyDigit, AnyNonDigit, AnyWhitespace, AnyWord)):
        assert len(self.content) == 2, 'cannot read `{}` as a character.'.format(repr(str(self)))
        return self.content[1]

    elif isinstance(self, Range):
        raise NotImplementedError('no single character associated with a `Range` object.')

    else:
        raise NotImplementedError


@__property__
def literal_chars(self: RangeGR) -> typing.FrozenSet[str]:
    """Return the literal characters that `self` refers to."""
    if isinstance(self, Range):
        start = ord(self.start.as_char)
        end = ord(self.end.as_char) + 1
        assert start <= end, 'invalid character range !'
        return frozenset(map(chr, range(start, end)))
    elif isinstance(self, (AnyDigit, AnyNonDigit)):
        return frozenset(string.digits)
    elif isinstance(self, (AnyWhitespace, AnyNonWhitespace)):
        return frozenset(string.whitespace)
    elif isinstance(self, (AnyWord, AnyNonWord)):
        return frozenset(string.ascii_letters + string.digits + '_')
    elif isinstance(self, (Dash, Dot, Digit, Character, EscapedCharacter)):
        return frozenset(self.as_char)
    else:
        raise NotImplementedError


@__property__
def as_inner_charset(self: RangeGR) -> Charset:
    """
        Return the Charset object corresponding to `self`.
        - Assuming `self` is an element inside a GroupInner | GroupInnerNot.
    """
    if isinstance(self, (Range, Dot, Dash, Digit, Character, EscapedCharacter, AnyDigit, AnyWhitespace, AnyWord)):
        return Charset(items=self.literal_chars, inverted=False)

    elif isinstance(self, (AnyNonDigit, AnyNonWhitespace, AnyNonWord)):
        return Charset(items=self.literal_chars, inverted=True)

    else:
        raise NotImplementedError


@__property__
def as_outer_charset(self: GroupInnerGR) -> Charset:
    """
        Return the Charset object corresponding to `self`.
        - Assuming `self` is not an element inside a GroupInner | GroupInnerNot.
    """
    if isinstance(self, GroupInner):
        charsets = [item.as_inner_charset for item in self.items]
        return Charset.union(*charsets)
    elif isinstance(self, GroupInnerNot):
        charsets = [item.as_inner_charset for item in self.items]
        return Charset.union(*charsets).complement
    elif isinstance(self, Range):
        raise NotImplementedError("Range objects does not have outer charset.")
    elif isinstance(self, Dot):
        return Charset(items=frozenset(''), inverted=True)
    elif isinstance(self, (Dash, Digit, Character, EscapedCharacter,
                           AnyDigit, AnyWhitespace, AnyWord,
                           AnyNonDigit, AnyNonWhitespace, AnyNonWord)):
        return self.as_inner_charset
    else:
        raise NotImplementedError
