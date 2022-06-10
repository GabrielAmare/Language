import platform

__all__ = [
    'OPTIONS',
    'PARAMS'
]


class OPTIONS:
    MODELS_ANNOTATIONS = 'models-annotations'  # include the annotations into the models (required when dataclass).
    MODELS_STR = 'models-str'  # include __str__ & __istr__ methods into the models.
    MODELS_PARSE = 'models-parse'  # include the parse method that transform Element object into the model classes.
    MODELS_DATACLASS = 'models-dataclass'  # build the models as dataclasses.
    MODELS_DATACLASS_FROZEN = 'models-dataclass-frozen'  # models are frozen dataclasses.
    MODELS_DATACLASS_ORDER = 'models-dataclass-order'  # models are ordered dataclasses.


class PARAMS:
    # list of the params (<name>, <default_value>)
    READER_NAME = ('reader_name', 'reader')
    ENGINE_NAME = ('engine_name', 'engine')
    READER_FN = ('reader_fn', 'reader')
    ENGINE_FN = ('engine_fn', 'engine')
    MODELS_FN = ('models_fn', 'models')
    TOKENIZER_FN = ('tokenizer_fn', 'tokenizer')
    GRAMMAR_FN = ('grammar_fn', 'grammar')
    CONFIG_FN = ('config_fn', 'config')

    SINGLE_LINE_ERRORS = ('single-line-errors', False)
    MAX_REPEAT_ITERATIONS = ('max-repeat-iterations', 100)
    
    # default the param to the currently used python version.
    PYTHON_VERSION = ('python-version', platform.python_version())
