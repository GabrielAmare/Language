import dataclasses
import functools
import json
import os.path
import typing

from .constants import PARAMS

__all__ = [
    'FilePath',
    'FilePathList',
    'FileSrc',
    'LangConfigSrc',
    'LangConfigDst',
    'LangConfig'
]

FilePath = str
FilePathList = list[FilePath]
FileSrc = typing.Optional[typing.Union[FilePath, FilePathList]]


@dataclasses.dataclass(frozen=True)
class LangConfigSrc:
    grammar: typing.Optional[typing.Union[FilePath, FilePathList]]
    imports: typing.Optional[typing.Union[FilePath, FilePathList]]
    reader: typing.Optional[FilePath]

    @classmethod
    def from_dict(cls, data: dict) -> 'LangConfigSrc':
        return cls(
            grammar=data.get('grammar', None),
            imports=data.get('imports', None),
            reader=data.get('reader', None),
        )

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
    reader: bool
    models: bool
    engine: bool
    grammar: bool
    config: bool
    tokenizer: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'LangConfigDst':
        return cls(
            root=data['root'],
            reader=data.get('reader', True),
            models=data.get('models', True),
            engine=data.get('engine', True),
            grammar=data.get('grammar', True),
            config=data.get('config', True),
            tokenizer=data.get('tokenizer', True),
        )

    def exists(self) -> bool:
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
        with open(__fp, mode='r', encoding='utf-8') as file:
            data = json.load(file)

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> 'LangConfig':
        return cls(
            lang=data['lang'],
            src=LangConfigSrc.from_dict(data.get('src', {})),
            dst=LangConfigDst.from_dict(data.get('dst', {})),
            options=data.get('options', {}),
            params=data.get('params', {})
        )

    def option(self, __key: str, default: bool = False) -> bool:
        return self.options.get(__key, default)

    def param(self, __key: str, __default: object = None) -> bool:
        return self.params.get(__key, __default)

    @functools.cached_property
    def reader_name(self) -> str:
        return self.params.get(*PARAMS.READER_NAME)

    @functools.cached_property
    def engine_name(self) -> str:
        return self.params.get(*PARAMS.ENGINE_NAME)

    @functools.cached_property
    def reader_fn(self) -> str:
        return self.params.get(*PARAMS.READER_FN)

    @functools.cached_property
    def engine_fn(self) -> str:
        return self.params.get(*PARAMS.ENGINE_FN)

    @functools.cached_property
    def models_fn(self) -> str:
        return self.params.get(*PARAMS.MODELS_FN)

    @functools.cached_property
    def grammar_fn(self) -> str:
        return self.params.get(*PARAMS.GRAMMAR_FN)

    @functools.cached_property
    def config_fn(self) -> str:
        return self.params.get(*PARAMS.CONFIG_FN)

    @functools.cached_property
    def tokenizer_fn(self) -> str:
        return self.params.get(*PARAMS.TOKENIZER_FN)

    @functools.cached_property
    def python_version(self) -> tuple[int, int, int]:
        """Return the python version to use for the lang package."""
        version = self.params.get(*PARAMS.PYTHON_VERSION)
        major, minor, patch = version.split('.', 2)
        return int(major), int(minor), int(patch)
