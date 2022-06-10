import dataclasses

from website.language import python as py, classmodule as cm
from website.language.base.models import Attribute
from ._abc import Builder

__all__ = [
    'AnnotationsBuilder'
]


@dataclasses.dataclass
class AnnotationsBuilder(Builder):
    def convert_attribute(self, attribute: Attribute) -> py.AnnAssign:
        """Return the dataclass annotation corresponding to the given attribute."""
        types = [
            py.Variable(attr_type)
            for attr_type in sorted(attribute.types)
        ]

        # TODO : be able to resume duck typing unions using the MRO info !
        #  when all the types in the union form the complete subclassing of another.
        #  i.e. Expr > (Add, Sub, Term) if the list if [Add, Sub, Term] we can resume it to Expr
        _type = self.module.make_duck_type(types)

        return self.module.make_annotation(
            name=py.Variable(attribute.name),
            type_=_type,
            optional=not attribute.required,
            multiple=attribute.multiple
        )

    def statements_for(self, node: cm.Node) -> list[py.Statement]:
        return [
            self.convert_attribute(attribute)
            for attribute in sorted(
                node.optimized.attributes.values(),
                key=lambda a: not a.required
            )
        ]

    def include_requirements(self, requirements: list[py.Statement]) -> None:
        pass
