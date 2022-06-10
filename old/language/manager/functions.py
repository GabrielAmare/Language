import importlib
import os.path
import typing

from website import console
from website.language.constants import WEBSITE_PATH
from website.tools.file_build import Directory
from .package import LangPackage

__all__ = [
    'update',
    'test',
    'load',
    'get_all',
    'scan',
    'create'
]


def _logger_update(lang_id: str) -> console.context:
    return console.context(
        message=f"updating {lang_id!r}",
        success=f"updated  {lang_id!r}",
        failure=f"failed to update {lang_id!r}",
        timer=True
    )


def update(repo: str, lang: str, changelog: str = '') -> None:
    lang_id = f"{repo}/{lang}"

    with _logger_update(lang_id):
        root = os.path.join(WEBSITE_PATH, lang_id).replace('\\', '/')
        pckg = LangPackage.load(root)
        pckg.build(changelog=changelog)


def test(repo: str, lang: str) -> None:
    importlib.import_module(name=f"website.{repo}.{lang}.lang")


def load(repo: str, lang: str) -> LangPackage:
    lang_id = f"{repo}/{lang}"
    fp = os.path.join(WEBSITE_PATH, lang_id)

    try:
        pckg = LangPackage.load(fp)

    except FileNotFoundError:
        raise Warning(f"{lang_id} -> 'config.json' file not found.")

    except KeyError:
        raise Warning(f"{lang_id} -> 'config.json' invalid.")

    except Exception as e:
        raise Warning(f"{lang_id} -> unexpected error {e!r}")

    if not pckg.can_be_built():
        raise Warning(f"{lang_id} -> can't be built (requires `grammar.bnf` | `reader.py`).")

    return pckg


def get_all(repo: str, debug: bool = False) -> typing.Iterator[str]:
    for lang in os.listdir(os.path.join(WEBSITE_PATH, repo)):
        try:
            load(repo, lang)
            yield lang

        except Warning as err:
            if debug:
                console.warning(f"{lang} -> {err.args[0]}")


def scan(repo: str, debug: bool = False) -> None:
    """Scan the selected lang `repo` to find the valid lang packages."""
    for pckg in get_all(repo, debug):
        console.success(pckg)


_DEFAULT_CONFIG = {
    "lang": "",
    "src": {
        "grammar": "grammar.bnf",
        "imports": []
    },
    "dst": {
        "root": "lang",
        "reader": "reader.py",
        "models": "models.py",
        "engine": "engine.py",
        "grammar": "grammar.bnf"
    }
}


def create(repo: str, lang: str, create_imports: bool = False) -> None:
    repo_fp = os.path.join(WEBSITE_PATH, repo)
    assert os.path.isdir(repo_fp)

    lang_fp = os.path.join(repo_fp, lang)
    if os.path.exists(lang_fp):
        raise FileExistsError(lang_fp)

    dst = Directory(root=repo_fp, name=lang)

    config = _DEFAULT_CONFIG.copy()
    config['lang'] = lang

    dst.text_file('grammar.bnf', '')
    dst.text_file('__init__.py', 'from .lang import *\n')
    dst.json_file('config.json', config)
    if create_imports:
        dst.directory('imports')

    dst.build()
