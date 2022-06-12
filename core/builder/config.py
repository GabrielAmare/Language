import dataclasses
import os.path
import platform

from tools import files

__all__ = [
    'LangConfigSrc',
    'LangConfigDst',
    'LangConfig'
]


@dataclasses.dataclass(frozen=True)
class LangConfigSrc:
    grammar: str | list[str] | None = None
    imports: str | list[str] | None = None
    reader: str | None = None

    def can_be_built_from_grammar(self, root: str) -> bool:
        if isinstance(self.grammar, str):
            return os.path.isfile(os.path.join(root, self.grammar))

        elif isinstance(self.grammar, list):
            return any(os.path.isfile(os.path.join(root, target)) for target in self.grammar)

        else:
            return False

    def can_be_built_from_reader(self, root: str) -> bool:
        return self.reader and os.path.isfile(os.path.join(root, self.reader))

    def can_be_built(self, root: str) -> bool:
        return self.can_be_built_from_grammar(root) or self.can_be_built_from_reader(root)


@dataclasses.dataclass(frozen=True)
class LangConfigDst:
    root: str

    # modules
    reader: bool = True  # build `reader` module
    models: bool = True  # build `models` module
    engine: bool = True  # build `engine` module
    tokenizer: bool = True  # build `tokenizer` module

    # other files
    grammar: bool = True  # build `grammar` file
    config: bool = True  # build `config` file

    def exists(self) -> bool:
        """Return True if the target directory exists."""
        return os.path.isdir(self.root)


@dataclasses.dataclass(frozen=True)
class LangConfig:
    lang: str
    src: LangConfigSrc
    dst: LangConfigDst
    options: dict
    params: dict

    @classmethod
    def load(cls, __fp: str) -> 'LangConfig':
        data = files.load_json_file(__fp)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> 'LangConfig':
        return cls(
            lang=data['lang'],
            src=LangConfigSrc(**data.get('src', {})),
            dst=LangConfigDst(**data.get('dst', {})),
            options=data.get('options', {}),
            params=data.get('params', {})
        )

    def option(self, __key: str, default: bool = False) -> bool:
        return self.options.get(__key, default)

    def param(self, __key: str, __default: object = None) -> bool:
        return self.params.get(__key, __default)

    @property
    def reader_name(self) -> str:
        """Return the name of the reader object."""
        return self.params.get('reader-name', 'reader')

    @property
    def engine_name(self) -> str:
        """Return the name of the engine object."""
        return self.params.get('engine-name', 'engine')

    @property
    def reader_fn(self) -> str:
        """Return the filename of the reader module."""
        return self.params.get('reader-fn', 'reader')

    @property
    def engine_fn(self) -> str:
        """Return the filename of the engine module."""
        return self.params.get('engine-fn', 'engine')

    @property
    def models_fn(self) -> str:
        """Return the filename of the models module."""
        return self.params.get('models-fn', 'models')

    @property
    def tokenizer_fn(self) -> str:
        """Return the filename of the tokenizer module."""
        return self.params.get('tokenizer-fn', 'tokenizer')

    @property
    def grammar_fn(self) -> str:
        """Return the filename of the grammar file."""
        return self.params.get('grammar-fn', 'grammar')

    @property
    def config_fn(self) -> str:
        """Return the filename of the config file."""
        return self.params.get('config-fn', 'config')

    @property
    def python_version(self) -> tuple[int, int, int]:
        """Return the python version to use for the lang package."""
        version = self.params.get('python-version', platform.python_version())
        major, minor, patch = version.split('.', 2)
        return int(major), int(minor), int(patch)
