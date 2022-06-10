from website.language.base.decorators import *
from website.language.python.lang.models import *


@__method__
def __pow__(self: Primary, other: Factor) -> Pow:
    """Return self ** other"""
    return Pow(left=self, right=other)


@__method__
def __lshift__(self: ShiftExpr, other: Sum) -> LShift:
    """Return self << other"""
    return LShift(left=self, right=other)


@__method__
def __rshift__(self: ShiftExpr, other: Sum) -> RShift:
    """Return self >> other"""
    return RShift(left=self, right=other)


@__method__
def __add__(self: Sum, other: Term) -> Add:
    """Return self + other"""
    return Add(left=self, right=other)


@__method__
def __sub__(self: Sum, other: Term) -> Sub:
    """Return self - other"""
    return Sub(left=self, right=other)


@__method__
def __mul__(self: Term, other: Factor) -> Mul:
    """Return self * other"""
    return Mul(left=self, right=other)


@__method__
def __truediv__(self: Term, other: Factor) -> TrueDiv:
    """Return self / other"""
    return TrueDiv(left=self, right=other)


@__method__
def __mod__(self: Term, other: Factor) -> Mod:
    """Return self % other"""
    return Mod(left=self, right=other)


@__method__
def __matmul__(self: Term, other: Factor) -> MatMul:
    """Return self @ other"""
    return MatMul(left=self, right=other)


@__method__
def __floordiv__(self: Term, other: Factor) -> FloorDiv:
    """Return self // other"""
    return FloorDiv(left=self, right=other)


@__method__
def __pos__(self: Factor) -> UAdd:
    """Return +self"""
    return UAdd(factor=self)


@__method__
def __neg__(self: Factor) -> USub:
    """Return -self"""
    return USub(factor=self)
