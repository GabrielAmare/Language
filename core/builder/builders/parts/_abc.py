import abc
import dataclasses

from core.builder.config import LangConfig
from core.langs import bnf
from core.langs.python import *

__all__ = [
    'PartBuilder'
]


@dataclasses.dataclass
class PartBuilder(abc.ABC):
    config: LangConfig
    graph: bnf.Graph
    module: DynamicModule

    @abc.abstractmethod
    def statements_for(self, node: bnf.Node) -> list[Statement]:
        """"""

    @abc.abstractmethod
    def include_requirements(self, requirements: list[Statement]) -> None:
        """"""

    @property
    def reader(self) -> bnf.Reader:
        return self.graph.reader

    def has_pattern(self, __type: bnf.Variable) -> bool:
        return self.reader.lexer.has(__type)

    def get_pattern(self, __type: bnf.Variable) -> bnf.PatternGR:
        return self.reader.lexer.get(__type)

    def has_branch(self, __type: bnf.Variable) -> bool:
        return self.reader.parser.has(__type)

    def get_branch(self, __type: bnf.Variable) -> bnf.BranchGR:
        return self.reader.parser.get(__type)

    def has(self, __type: bnf.Variable) -> bool:
        return self.reader.has(__type)

    def get(self, __type: bnf.Variable) -> bnf.TopLevel:
        return self.reader.get(__type)
