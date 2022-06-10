from __future__ import annotations

import dataclasses
import functools

__all__ = [
    'Attribute',
    'Descriptor',
    'get_shared_descriptor',
]


@dataclasses.dataclass
class Attribute:
    name: str
    types: set[str]
    multiple: bool = False
    required: bool = True

    def optional(self) -> Attribute:
        return dataclasses.replace(self, required=False)

    def __and__(self, other: Attribute) -> Attribute:
        """Concatenate self and other"""
        assert self.multiple == other.multiple, "mismatching multiplicity."
        assert self.multiple is True, "cannot concatenate non-multiple attributes."
        return dataclasses.replace(self, types=self.types.union(other.types), required=self.required or other.required)

    def __or__(self, other: Attribute) -> Attribute:
        """Join self and other. they must be equal."""
        assert self.multiple == other.multiple, "mismatching multiplicity."
        return dataclasses.replace(self, types=self.types.union(other.types), required=self.required and other.required)


@dataclasses.dataclass
class Descriptor:
    attributes: dict[str, Attribute] = dataclasses.field(default_factory=dict)

    def only_multiple_attributes(self):
        return all(attribute.multiple for attribute in self.attributes.values())

    def optional(self) -> Descriptor:
        """Make all the attributes optional"""
        return Descriptor({name: attribute.optional() for name, attribute in self.attributes.items()})

    def has_attribute(self, __name: str) -> bool:
        return __name in self.attributes

    def get_attribute(self, __name: str) -> Attribute:
        return self.attributes[__name]

    def __and__(self, other: Descriptor) -> Descriptor:
        """Concatenate self and other"""
        names = []
        for name in self.attributes.keys():
            if name not in names:
                names.append(name)
        for name in other.attributes.keys():
            if name not in names:
                names.append(name)

        attributes = {}

        for name in names:
            if name in self.attributes and name in other.attributes:
                attributes[name] = self.attributes[name] & other.attributes[name]
            elif name in self.attributes:
                attributes[name] = self.attributes[name]
            elif name in other.attributes:
                attributes[name] = other.attributes[name]
            else:
                pass

        return Descriptor(attributes)

    def get_common_names(self, other: Descriptor) -> list[str]:
        names = []
        for name in self.attributes.keys():
            if name not in names:
                names.append(name)
        for name in other.attributes.keys():
            if name not in names:
                names.append(name)
        return names

    def __or__(self, other: Descriptor) -> Descriptor:
        """Join self and other."""
        names = self.get_common_names(other)

        attributes = {}

        for name in names:
            if self.has_attribute(name) and other.has_attribute(name):
                attributes[name] = self.get_attribute(name) | other.get_attribute(name)
            elif self.has_attribute(name):
                attributes[name] = self.get_attribute(name).optional()
            elif other.has_attribute(name):
                attributes[name] = other.get_attribute(name).optional()
            else:
                pass

        return Descriptor(attributes)

    def __truediv__(self, other: Descriptor) -> Descriptor:
        """Remove all the attributes that are equal from self."""
        names = self.get_common_names(other)

        attributes = {}

        for name in names:
            if self.has_attribute(name) and other.has_attribute(name):
                a1 = self.get_attribute(name)
                a2 = other.get_attribute(name)
                if a1 == a2:
                    pass
                else:
                    attributes[name] = a1
            elif self.has_attribute(name):
                attributes[name] = self.get_attribute(name)
            elif other.has_attribute(name):
                pass
            else:
                pass

        return Descriptor(attributes)

    def intersection(self, other: Descriptor) -> Descriptor:
        """Return the common descriptor to self and other. keep only the exact same shared attributes."""
        names = self.get_common_names(other)

        attributes = {}

        for name in names:
            has1, has2 = self.has_attribute(name), other.has_attribute(name)
            if has1 and has2:
                get1, get2 = self.get_attribute(name), other.get_attribute(name)
                if get1 == get2:
                    attributes[name] = get1
                else:
                    pass
            elif has1:
                pass
            elif has2:
                pass
            else:
                pass

        return Descriptor(attributes)


def get_shared_descriptor(descriptors: list[Descriptor]) -> Descriptor:
    """Return the list of identical attributes shared between the models."""
    if descriptors:
        return functools.reduce(Descriptor.intersection, descriptors)

    else:
        return Descriptor({})
