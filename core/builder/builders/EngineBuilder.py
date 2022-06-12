import dataclasses
import functools
import typing

from core.builder import params
from core.langs import bnf
from core.langs.python import *
from ._abc import TextBuilder

__all__ = [
    'EngineBuilder'
]


@dataclasses.dataclass
class EngineBuilder(TextBuilder):
    reader: bnf.Reader

    def __post_init__(self):
        self.reader = self.reader.simplify(literals=True, aliases=True)

    @functools.cached_property
    def dynamic(self) -> DynamicModule:
        return DynamicModule(
            version=self.config.python_version
        )

    @functools.cached_property
    def var_engine(self) -> Primary:
        return self.dynamic.imports(path='core.langs.bnf.maker', name='Engine')

    @functools.cached_property
    def var_models(self) -> Primary:
        return self.dynamic.imports(path='', name=self.config.models_fn)

    @functools.cached_property
    def var_reader(self) -> Primary:
        return self.dynamic.imports(path=f'.{self.config.reader_fn}', name=self.config.reader_name)

    def _i_statements(self) -> typing.Iterator[Statement]:
        yield AnnAssign(
            target=Variable('engine'),
            value=IndentedCall(
                left=self.var_engine,
                body=IndentedCallBody([
                    NamedArgument(
                        name=Variable('reader'),
                        expr=self.var_reader
                    ),
                    NamedArgument(
                        name=Variable('models'),
                        expr=self.var_models
                    ),
                    NamedArgument(
                        name=Variable('single_line_errors'),
                        expr=Constant.from_value(self.config.param(*params.Engine.SINGLE_LINE_ERRORS))
                    ),
                    NamedArgument(
                        name=Variable('max_repeat_iterations'),
                        expr=Constant.from_value(self.config.param(*params.Engine.MAX_REPEAT_ITERATIONS))
                    )
                ])
            )
        )

    def build(self) -> str:
        self.dynamic.statements.extend(self._i_statements())

        module = self.dynamic.to_module()
        return str(module)
