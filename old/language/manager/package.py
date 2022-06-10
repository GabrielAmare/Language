import dataclasses
import functools
import os.path

from website import console
from website.language import bnf, python as py
from website.language.constants import LEX
from website.tools.file_build import Directory
from .config import LangConfig
from .file_builders import *
from .file_loaders import GrammarLoader, ImportsLoader, ReaderLoader

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

    def can_be_built(self) -> bool:
        """Return True when the lang package can be built."""
        return self.config.src.can_be_built(self.root)

    def is_built(self) -> bool:
        """Return True when the lang package already exists."""
        return self.config.dst.exists()

    @functools.cached_property
    def grammar_loader(self) -> GrammarLoader:
        return GrammarLoader(
            root=self.root,
            src=self.config.src.grammar,
            option=self.config.option
        )

    @functools.cached_property
    def reader_loader(self) -> ReaderLoader:
        return ReaderLoader(root=self.root, src=self.config.src.reader)

    @functools.cached_property
    def imports_loader(self) -> ImportsLoader:
        return ImportsLoader(root=self.root, src=self.config.src.imports, python_version=self.config.python_version)

    def _load_grammar_and_reader(self) -> tuple[str, bnf.Reader]:
        if self.config.src.can_be_built_from_grammar(self.root):
            with _log(f"loading `{LEX.GRAMMAR}`"):
                grammar = self.grammar_loader.load()

            with _log(f"building `{LEX.READER}` from `{LEX.GRAMMAR}` using `bnf.{LEX.ENGINE}`."):
                reader = bnf.engine(grammar)

        elif self.config.src.can_be_built_from_reader(self.root):
            with _log(f"loading `{LEX.READER}`"):
                reader = self.reader_loader.load()

            with _log(f"building `{LEX.GRAMMAR}` from `{LEX.READER}` using `str`."):
                grammar = str(reader)

        else:
            raise Exception(f"Can't build config : requires `{LEX.GRAMMAR}.src` | `{LEX.READER}.src`.")

        return grammar, reader

    def _generate_models_module_content(self, reader: bnf.Reader) -> str:
        initial_builder = ModelsBuilder(config=self.config, reader=reader)

        dynamic: py.DynamicModule = initial_builder.build()

        if self.config.src.imports:
            with _log(f"including `imports` into `models.py`"):
                external_builder = py.ImportExternalMethods(classes=dynamic)
                for external in self.imports_loader.load():
                    external_builder.build(methods=external)

        module = dynamic.to_module()
        return str(module)

    def build(self, changelog: str = '') -> None:
        with _log(f"building `{self.config.lang}`."):
            with _log("loading grammar & reader."):
                grammar, reader = self._load_grammar_and_reader()

            # TODO : build the contents only when required.
            #        try using some function that handle 2 steps (generating the content -> writing the file)
            with _log("generating file contents."):
                reader_module_content = ReaderBuilder(config=self.config, reader=reader).build()
                models_module_content = self._generate_models_module_content(reader=reader)
                engine_module_content = EngineBuilder(config=self.config, reader=reader).build()
                init_module_content = InitBuilder(config=self.config).build()
                # tokenizer_module_content = TokenizerBuilder(config=self.config, reader=reader).build()
                grammar_module_content = grammar
                config_data = ConfigBuilder(config=self.config).build(changelog=changelog)

            with _log("building lang directory."):
                lang_dir = Directory(root=self.root, name=self.config.dst.root)
                lang_dir.text_file(name='__init__.py', content=init_module_content)

                if self.config.dst.engine:
                    lang_dir.text_file(name=f'{self.config.engine_fn}.py', content=engine_module_content)

                if self.config.dst.models:
                    lang_dir.text_file(name=f'{self.config.models_fn}.py', content=models_module_content)

                if self.config.dst.reader:
                    lang_dir.text_file(name=f'{self.config.reader_fn}.py', content=reader_module_content)

                # if self.config.dst.tokenizer:
                #     lang_dir.text_file(name=f'{self.config.tokenizer_fn}.py', content=tokenizer_module_content)

                if self.config.dst.grammar:
                    lang_dir.text_file(name=f'{self.config.grammar_fn}.bnf', content=grammar_module_content)

                if self.config.dst.config:
                    lang_dir.json_file(name=f'{self.config.config_fn}.json', data=config_data)

                lang_dir.build()
