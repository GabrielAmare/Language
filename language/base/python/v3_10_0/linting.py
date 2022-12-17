import enum

__all__ = [
    'LintRule',
]


class LintRule(str, enum.Enum):
    MODULE_NO_IMPORT_FROM = "module-no-import-from"
    MODULE_NO_IMPORT_ALL = "module-no-import-all"
    MODULE_NO_MIXED_IMPORTS = "module-no-mixed-imports"
    
    DATACLASS_FROZEN = "dataclass-frozen"
    DATACLASS_MULTIPLE_NO_REPEATS = "dataclass-multiple-no-repeats"
    DATACLASS_MULTIPLE_CAN_BE_NONE = "dataclass-multiple-can-be-none"
