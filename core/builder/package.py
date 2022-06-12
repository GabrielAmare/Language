import dataclasses
import functools
import os.path

from core.langs import bnf, python
from tools import console, files
from .builders import *
from .config import LangConfig
from .loaders import *

__all__ = [
    'LangPackage'
]


def _log(text: str):
    return console.context(text, "took", timer=True)


@dataclasses.dataclass
class LangPackage:
    root: str
    config: LangConfig

    @classmethod
    def load(cls, root: str):
        assert os.path.isdir(root), f"{root!r} does not exists !"
        return cls(
            root=root,
            config=LangConfig.load(os.path.join(root, 'config.json'))
        )

    ####################################################################################################################
    # FILE LOADERS
    ####################################################################################################################

    @functools.cached_property
    def grammar_loader(self) -> GrammarLoader:
        return GrammarLoader(root=self.root, src=self.config.src.grammar, option=self.config.option)

    @functools.cached_property
    def reader_loader(self) -> ReaderLoader:
        return ReaderLoader(root=self.root, src=self.config.src.reader)

    @functools.cached_property
    def imports_loader(self) -> ImportsLoader:
        return ImportsLoader(root=self.root, src=self.config.src.imports, python_version=self.config.python_version)

    ####################################################################################################################
    # FILE BUILDERS
    ####################################################################################################################

    @functools.cached_property
    def init_builder(self) -> InitBuilder:
        return InitBuilder(config=self.config)

    @functools.cached_property
    def reader_builder(self) -> ReaderBuilder:
        return ReaderBuilder(config=self.config, reader=self.reader)

    @functools.cached_property
    def models_builder(self) -> ModelsBuilder:
        return ModelsBuilder(config=self.config, reader=self.reader)

    @functools.cached_property
    def engine_builder(self) -> EngineBuilder:
        return EngineBuilder(config=self.config, reader=self.reader)

    @functools.cached_property
    def config_builder(self) -> ConfigBuilder:
        return ConfigBuilder(config=self.config)

    ####################################################################################################################
    # METHODS
    ####################################################################################################################

    def can_be_built(self) -> bool:
        """Return True when the lang package can be built."""
        return self.config.src.can_be_built(self.root)

    def is_built(self) -> bool:
        """Return True when the lang package already exists."""
        return self.config.dst.exists()

    def can_be_built_from_grammar(self) -> bool:
        return self.config.src.can_be_built_from_grammar(self.root)

    def can_be_built_from_reader(self) -> bool:
        return self.config.src.can_be_built_from_reader(self.root)

    @functools.cached_property
    def reader(self) -> bnf.Reader:
        if self.can_be_built_from_grammar():
            return bnf.engine(self.grammar)

        elif self.can_be_built_from_reader():
            return self.reader_loader.load()

        else:
            raise NotImplementedError

    @functools.cached_property
    def grammar(self) -> str:
        if self.can_be_built_from_grammar():
            return self.grammar_loader.load()

        elif self.can_be_built_from_reader():
            return str(self.reader)

        else:
            raise NotImplementedError

    def _generate_models_module_content(self) -> str:
        dynamic: python.DynamicModule = self.models_builder.build()

        if self.config.src.imports:
            with _log(f"including `imports` into `models.py`"):
                external_builder = python.ImportExternalMethods(classes=dynamic)
                for external in self.imports_loader.load():
                    external_builder.build(methods=external)

        module = dynamic.to_module()
        return str(module)

    def build(self, changelog: str = '') -> None:
        package = files.Directory(root=self.root, name=self.config.dst.root)

        package.python_module(name='__init__', content=self.init_builder.build())

        if self.config.dst.reader:
            package.python_module(name=self.config.reader_fn, content=self.reader_builder.build())

        if self.config.dst.models:
            package.python_module(name=self.config.models_fn, content=self._generate_models_module_content())

        if self.config.dst.engine:
            package.python_module(name=self.config.engine_fn, content=self.engine_builder.build())

        if self.config.dst.grammar:
            package.text_file(name=self.config.grammar_fn + '.bnf', content=self.grammar)

        if self.config.dst.config:
            package.json_file(name=self.config.config_fn, data=self.config_builder.build(changelog=changelog))

        package.save()
