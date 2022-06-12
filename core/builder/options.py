__all__ = [
    'Grammar',
    'Models',
]


class Grammar:
    _PREFIX = 'grammar-'
    REMOVE_COMMENTS = _PREFIX + 'remove-comments'
    REMOVE_DOUBLE_NEWLINE = _PREFIX + 'remove-double-newline'
    REMOVE_TRAILING_NEWLINE = _PREFIX + 'remove-trailing-newline'
    FORCE_NEWLINE_AFTER_GROUP = _PREFIX + 'force-newline-after-group'
    ALIGN_DEFINITIONS = _PREFIX + 'align-definitions'


class Models:
    _PREFIX = 'models-'
    ANNOTATIONS = 'annotations'  # include the annotations into the models (required when dataclass).
    STR = 'str'  # include __str__ & __istr__ methods into the models.
    PARSE = 'parse'  # include the parse method that transform Element object into the model classes.
    DATACLASS = 'dataclass'  # build the models as dataclasses.
    DATACLASS_FROZEN = 'dataclass-frozen'  # models are frozen dataclasses.
    DATACLASS_ORDER = 'dataclass-order'  # models are ordered dataclasses.
