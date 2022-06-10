import functools
import typing

from .processing import Element, Lemma, Token

__all__ = [
    'builder'
]


def builder(models: object):
    def get_factory(__type: str) -> type:
        try:
            return getattr(models, __type)

        except AttributeError:
            raise AttributeError(f"can't build AST[{__type}]:\n"
                                 f"\treason: {__type} class not found in the models !")

    @functools.singledispatch
    def build(o: typing.Union[Element, list[Element]]):
        raise NotImplementedError(type(o))

    @build.register
    def _(o: list) -> list[object]:
        return list(map(build, o))

    @build.register
    def _(o: Token) -> object:
        factory = get_factory(o.type)
        try:
            return factory(o.content)

        except TypeError:
            return factory()

    @build.register
    def _(o: Lemma) -> object:
        factory = get_factory(o.type)

        data = {key: build(value) for key, value in o.data.items()}
        try:
            return factory(**data)
        except TypeError as error:
            raise TypeError(f"can't build AST[{o.type!r}]:\n"
                            f"\tdata: {data}\n"
                            f"\terror: {error}")

    return build
