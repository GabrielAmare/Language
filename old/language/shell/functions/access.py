import os
import typing

from website.language.constants import WEBSITE_PATH

__all__ = [
    'access_langs'
]


def _check_dir(path: str) -> None:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"dir {path!r} not found.")


def _check_file(root: str, name: str) -> None:
    if not os.path.isfile(os.path.join(root, name)):
        raise FileNotFoundError(f"file {name!r} not found in {root!r} !")


def _check_lang_package(src: str, built: bool = False) -> None:
    """Return True if the target `path` points to a valid lang package."""
    _check_dir(src)
    _check_file(src, "__init__.py")
    _check_file(src, "config.json")

    # seek for a `grammar.bnf` file | a `grammar` dir | a `reader.py` module ; as lang initializer.
    try:
        _check_file(src, "grammar.bnf")
    except FileNotFoundError:
        try:
            _check_dir(os.path.join(src, "grammar"))
        except FileNotFoundError:
            _check_file(src, "reader.py")

    if built:
        lang_src = os.path.join(src, "lang")

        _check_dir(lang_src)
        _check_file(lang_src, "__init__.py")

        _check_file(lang_src, "engine.py")
        _check_file(lang_src, "reader.py")
        _check_file(lang_src, "models.py")


def access_langs(repo: str, built: bool = False) -> typing.Iterator[tuple[str, bool, str]]:
    """Return an iterator of all the langs defined within the `repo`."""
    src = os.path.join(WEBSITE_PATH, repo)
    for name in os.listdir(src):
        try:
            _check_lang_package(src=os.path.join(src, name), built=built)
            yield name, True, ''

        except FileNotFoundError as err:
            yield name, False, err.args[0] if err.args else ''
