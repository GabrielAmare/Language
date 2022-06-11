__all__ = [
    '__method__',
    '__class_method__',
    '__static_method__',
    '__property__',
    '__cached_property__'
]


def identity(x):
    return x


__method__ = identity
__class_method__ = identity
__static_method__ = identity
__property__ = identity
__cached_property__ = identity
