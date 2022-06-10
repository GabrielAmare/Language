import dataclasses
import functools
import typing

from website.language import bnf
from website.language.manager.constants import PARAMS, OPTIONS
from website.language.python import *
from ._abc import TextBuilder
from .part_builders.ParseBuilder import LEX as PARSE_LEX
__all__ = [
    'EngineBuilder'
]


class LEX:
    READER = Variable('reader')
    MODELS = Variable('models')
    SINGLE_LINE_ERRORS = Variable('single_line_errors')
    MAX_REPEAT_ITERATIONS = Variable('max_repeat_iterations')
    MAKE_ENGINE = Variable('make_engine')

    TOKENIZE = Variable('_tokenize')
    PROCESS = Variable('_process')
    BUILD = Variable('_build')

    ENGINE = Variable('engine')
    TEXT = Variable('text')

    TOK = Variable('tok')
    AST = Variable('ast')
    OBJ = Variable('obj')


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
    def var_builder(self) -> Primary:
        return self.dynamic.imports(path='website.language.base.building', name='builder')

    @functools.cached_property
    def var_processor(self) -> Primary:
        return self.dynamic.imports(path='website.language.core.processor', name='Processor')

    @functools.cached_property
    def var_tokenizer(self) -> Primary:
        return self.dynamic.imports(path='website.language.core.tokenizer', name='tokenizer')

    @functools.cached_property
    def var_models(self) -> Primary:
        return self.dynamic.imports(path='', name=self.config.models_fn)

    @functools.cached_property
    def var_reader(self) -> Primary:
        return self.dynamic.imports(path=f'.{self.config.reader_fn}', name=self.config.reader_name)

    def _i_statements(self) -> typing.Iterator[Statement]:
        yield AnnAssign(
            target=LEX.TOKENIZE,
            value=self.var_tokenizer.call(
                NamedArgument(Variable('lexer'), self.var_reader.getattr('lexer')),
                NamedArgument(Variable('make_list'), TRUE),
                NamedArgument(
                    LEX.SINGLE_LINE_ERRORS,
                    Constant.from_value(self.config.param(*PARAMS.SINGLE_LINE_ERRORS))
                ),
            )
        )
        yield AnnAssign(
            target=LEX.PROCESS,
            value=self.var_processor.call(
                NamedArgument(Variable('reader'), self.var_reader),
                NamedArgument(
                    LEX.MAX_REPEAT_ITERATIONS,
                    Constant.from_value(self.config.param(*PARAMS.MAX_REPEAT_ITERATIONS))
                ),
            )
        )
        if self.config.option(OPTIONS.MODELS_PARSE):
            yield AnnAssign(
                target=LEX.BUILD,
                value=GetAttr(
                    left=self.var_models.getattr(Variable(content=str(self.reader.parser.start))),
                    right=PARSE_LEX.PARSE
                )
            )
        else:
            yield AnnAssign(
                target=LEX.BUILD,
                value=self.var_builder.call(
                    self.var_models
                )
            )
        yield Def(
            name=LEX.ENGINE,
            args=[
                Argument(name=LEX.TEXT, type=TYPES.STR)
            ],
            rtype=self.var_models.getattr(Variable(content=str(self.reader.parser.start))),
            block=Block([
                AnnAssign(target=LEX.TOK, value=LEX.TOKENIZE.call(LEX.TEXT)),
                AnnAssign(target=LEX.AST, value=LEX.PROCESS.call(LEX.TOK)),
                AnnAssign(target=LEX.OBJ, value=LEX.BUILD.call(LEX.AST)),
                Return(LEX.OBJ)
            ])
        )

    def build(self) -> str:
        self.dynamic.statements.extend(self._i_statements())

        # make_engine = dynamic.imports(path='website.language.core.make_engine', name='make_engine')
        # _reader = dynamic.imports(path='.' + self.config.reader_fn, name=self.config.reader_name)

        # """
        # from .builder import builder
        # from .processor import Processor
        # from .tokenizer import tokenizer
        # from . import models
        #
        # __all__ = [
        #     'engine'
        # ]
        #
        # _tokenize = tokenizer(
        #     lexer=reader.lexer,
        #     make_list=True,
        #     single_line_errors=<single_line_errors>
        # )
        # _process = Processor(
        #     reader=reader,
        #     max_repeat_iterations=<max_repeat_iterations>
        # )
        # _build = builder(models)
        #
        # def engine(text: str):
        #     tok = _tokenize(text)
        #     ast = _process(tok)
        #     obj = _build(ast)
        #     return obj
        #
        # return read
        #
        # def make_engine(
        #         reader,
        #         models,
        #         single_line_errors: bool = False,
        #         max_repeat_iterations: int = 100,
        #         debug: bool = False
        # ):
        # """
        #
        # dynamic.statements.extend([
        #     EmptyLine(),
        #     AnnAssign(
        #         target=Variable(self.config.engine_name),
        #         value=IndentedCall(
        #             left=make_engine,
        #             body=IndentedCallBody(args=[
        #                 NamedArgument(
        #                     LEX.READER,
        #                     _reader.getattr('simplify').call()
        #                 ),
        #                 NamedArgument(
        #                     LEX.MODELS,
        #                     _models
        #                 ),
        #                 NamedArgument(
        #                     LEX.SINGLE_LINE_ERRORS,
        #                     Constant.from_value(self.config.param('single_line_errors', False))
        #                 ),
        #                 NamedArgument(
        #                     LEX.MAX_REPEAT_ITERATIONS,
        #                     Constant.from_value(self.config.param('max_repeat_iterations', 1000))
        #                 ),
        #             ])
        #         )
        #     )
        # ])

        module = self.dynamic.to_module()
        return str(module)
