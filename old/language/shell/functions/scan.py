from website import console
from .access import access_langs

__all__ = [
    'scan'
]


def scan(repo: str, debug: bool):
    """Scan the selected lang `repo` to find the valid lang packages."""
    for lang, valid, msg in access_langs(repo):
        if valid:
            console.success(lang)

        elif debug:
            console.warning(lang + ' -> ' + msg)
