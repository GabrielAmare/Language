import enum

__all__ = [
    'Lang'
]


class Lang(str, enum.Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
