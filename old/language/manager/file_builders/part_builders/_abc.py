import abc
import dataclasses
import typing

from website.language import python as py, classmodule as cm, bnf
from website.language.manager.config import LangConfig

__all__ = [
    'Builder'
]


@dataclasses.dataclass
class Builder(abc.ABC):
    config: LangConfig
    graph: cm.Graph
    module: py.DynamicModule

    @abc.abstractmethod
    def statements_for(self, node: cm.Node) -> list[py.Statement]:
        """"""

    @abc.abstractmethod
    def include_requirements(self, requirements: list[py.Statement]) -> None:
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
