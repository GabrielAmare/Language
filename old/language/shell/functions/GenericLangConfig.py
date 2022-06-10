import dataclasses

__all__ = [
    'GenericLangConfig'
]


@dataclasses.dataclass
class GenericLangConfig:
    """Default configuration for a lang package structure."""
    lang_dirname: str = 'lang'
    imports_dirname: str = 'imports'
    config_filename: str = 'config'
    engine_filename: str = 'engine'
    models_filename: str = 'models'
    reader_filename: str = 'reader'
    grammar_filename: str = 'grammar'
