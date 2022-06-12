import dataclasses

from base.models import Attribute
from core.langs import bnf
from core.langs.python import *
from ._abc import PartBuilder

__all__ = [
    'DataclassBuilder'
]


@dataclasses.dataclass
class DataclassBuilder(PartBuilder):
    def convert_attribute(self, attribute: Attribute) -> AnnAssign:
        """Return the dataclass annotation corresponding to the given attribute."""
        types = [
            Variable(attr_type)
            for attr_type in sorted(attribute.types)
        ]

        # TODO : be able to resume duck typing unions using the MRO info !
        #  when all the types in the union form the complete subclassing of another.
        #  i.e. Expr > (Add, Sub, Term) if the list if [Add, Sub, Term] we can resume it to Expr
        _type = self.module.make_duck_type(types)

        return self.module.make_annotation(
            name=Variable(attribute.name),
            type_=_type,
            optional=not attribute.required,
            multiple=attribute.multiple
        )

    def statements_for(self, node: bnf.Node) -> list[Statement]:
        return [
            self.convert_attribute(attribute)
            for attribute in sorted(
                node.optimized.attributes.values(),
                key=lambda a: not a.required
            )
        ]

    def include_requirements(self, requirements: list[Statement]) -> None:
        pass
