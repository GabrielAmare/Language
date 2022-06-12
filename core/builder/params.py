import platform

__all__ = [
    'Base',
    'Engine',
]


class Base:
    # list of the params (<name>, <default_value>)
    READER_NAME = 'reader_name', 'reader'
    ENGINE_NAME = 'engine_name', 'engine'
    READER_FN = 'reader_fn', 'reader'
    ENGINE_FN = 'engine_fn', 'engine'
    MODELS_FN = 'models_fn', 'models'
    TOKENIZER_FN = 'tokenizer_fn', 'tokenizer'
    GRAMMAR_FN = 'grammar_fn', 'grammar'
    CONFIG_FN = 'config_fn', 'config'


class Engine:
    SINGLE_LINE_ERRORS = 'single-line-errors', False
    MAX_REPEAT_ITERATIONS = 'max-repeat-iterations', 100


# default the param to the currently used python version.
PYTHON_VERSION = 'python-version', platform.python_version()
