import dataclasses

__all__ = [
    'Element',
    'Context',
    'Token',
]


@dataclasses.dataclass
class Element:
    type: str

    @staticmethod
    def is_typed_as(__type: str):
        def wrapped(element: Element) -> bool:
            return element.type == __type

        return wrapped


@dataclasses.dataclass
class Context:
    data: dict[str, Element | list[Element]] = dataclasses.field(default_factory=dict)

    def set_as(self, __key: str, __element: Element) -> None:
        assert __key not in self.data
        self.data[__key] = __element

    def add_in(self, __key: str, __element: Element) -> None:
        if __key in self.data:
            assert isinstance(self.data[__key], list)
            self.data[__key].append(__element)
        else:
            self.data[__key] = [__element]

    @staticmethod
    def set_as_for(__key: str):
        def wrapped(ctx: Context, element: Element) -> None:
            ctx.set_as(__key, element)

        return wrapped

    @staticmethod
    def add_in_for(__key: str):
        def wrapped(ctx: Context, element: Element) -> None:
            ctx.add_in(__key, element)

        return wrapped


@dataclasses.dataclass
class Token(Element):
    content: str
