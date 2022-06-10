import functools
import operator

from website.language.base.decorators import *
from website.language.base.models import Descriptor, Attribute
from website.language.bnf.lang.models import *


@__property__
def descriptor(self: ParallelGR) -> Descriptor:
    """Return the descriptor associated with `self` (assumes that no match refers to `Alias` objects)."""
    if isinstance(self, (Match, Literal, Canonical, Negative)):
        return Descriptor()

    elif isinstance(self, MatchIn):
        return Descriptor({
            str(self.key): Attribute(name=str(self.key), types={str(self.type)}, multiple=True, required=True)
        })

    elif isinstance(self, MatchAs):
        return Descriptor({
            str(self.key): Attribute(name=str(self.key), types={str(self.type)}, multiple=False, required=True)
        })

    elif isinstance(self, Optional):
        return self.rule.descriptor.optional()

    elif isinstance(self, Grouping):
        return self.rule.descriptor

    elif isinstance(self, RepeatPlus):
        model = self.rule.descriptor
        assert model.only_multiple_attributes(), "RepeatPlus only allow attributes with `multiple`"
        return model

    elif isinstance(self, RepeatStar):
        model = self.rule.descriptor
        assert model.only_multiple_attributes(), "RepeatStar only allow attributes with `multiple`"
        return model.optional()

    elif isinstance(self, Repeat):
        model = self.rule.descriptor
        assert model.only_multiple_attributes(), "Repeat only allow attributes with `multiple`"
        if Integer.to_int(self.mn) > 0:
            return model.optional()
        else:
            return model

    elif isinstance(self, Enum0):
        model = self.separator.descriptor.optional() & self.element.descriptor
        assert model.only_multiple_attributes(), "Enum only allow attributes with `multiple`"
        return model

    elif isinstance(self, Enum1):
        model = self.separator.descriptor & self.element.descriptor
        assert model.only_multiple_attributes(), "EnumPlus only allow attributes with `multiple`"
        return model

    elif isinstance(self, Sequence):
        return functools.reduce(operator.and_, [rule.descriptor for rule in self.rules], Descriptor())

    elif isinstance(self, Parallel):
        return functools.reduce(operator.or_, [rule.descriptor for rule in self.rules], Descriptor())

    else:
        raise NotImplementedError


@__property__
def descriptor(self: TopLevel) -> Descriptor:
    if isinstance(self, Group):
        return Descriptor()

    elif isinstance(self, PatternGR):
        return Descriptor({'content': Attribute(name='content', types={'str'}, required=True, multiple=False)})

    elif isinstance(self, (Branch, Alias)):
        return self.rule.descriptor

    else:
        raise NotImplementedError
