import dataclasses
import functools

from website.language import bnf, semi, optilex, code_generator as cg, optilex_to_code, python as py
from ._abc import TextBuilder

__all__ = [
    'TokenizerBuilder'
]


@dataclasses.dataclass
class TokenizerBuilder(TextBuilder):
    """
        This builder creates a file for the tokenizer.
        It will contain the code required to tokenize any text written in the source language.
        (encapsulated within the reader attribute)
    """
    reader: bnf.Reader

    @functools.cached_property
    def lexer(self) -> bnf.Lexer:
        """Get the lexer from `self.reader`."""
        return self.reader.lexer

    @functools.cached_property
    def branch_set(self) -> semi.BranchSet:
        """Convert `self.lexer` to a `semi.BranchSet`."""
        # TODO : transform `semi/from_bnf` to `bnf/to_semi`.
        return semi.BranchSet.from_bnf(self.lexer)

    @functools.cached_property
    def origin_select(self) -> optilex.OriginSelect:
        """Convert `self.branch_set` to a `optilex.OriginSelect`."""
        return self.branch_set.to_optilex()

    @functools.cached_property
    def generic_module(self) -> cg.Module:
        """Convert `self.origin_select` to a `code_generator.Module`."""
        # TODO : use `generic` language instead !
        return optilex_to_code.origin_select_to_module(self.origin_select)

    @functools.cached_property
    def python_module(self) -> py.Module:
        """Convert `self.generic_module` to a `python.Module`."""
        return self.generic_module.to_python()

    def build(self) -> str:
        """Return the convent of the python module."""
        return str(self.python_module)
