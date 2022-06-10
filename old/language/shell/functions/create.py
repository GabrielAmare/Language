import dataclasses
import os.path
import os.path

from website.language.constants import WEBSITE_PATH
from website.tools.file_utils import PythonTemplateFile, copy_file
from .GenericLangConfig import GenericLangConfig

__all__ = [
    'create_lang'
]


def _build_template(src: str, dst: str, filename: str, cfg: dict) -> None:
    PythonTemplateFile \
        .load(src=os.path.join(src, filename)) \
        .build(cfg=cfg) \
        .save(dst=os.path.join(dst, filename))


def _copy_file(src: str, dst: str, filename: str) -> None:
    copy_file(
        src=os.path.join(src, filename),
        dst=os.path.join(dst, filename),
    )


def create_lang(repo: str, lang_name: str, create_imports: bool) -> None:
    struct = GenericLangConfig()

    cfg = {
        'repo': repo,
        'lang': lang_name,
        **dataclasses.asdict(struct),
    }

    # building : <lang_name>/
    src: str = os.path.join(os.path.dirname(__file__), 'lang_package_template')
    dst: str = os.path.join(WEBSITE_PATH, repo, lang_name).replace('\\', '/')
    if os.path.exists(dst):
        raise Exception(f"Can't overwrite existing {dst!r}.")
    os.mkdir(dst)
    _build_template(src=src, dst=dst, filename='__init__', cfg=cfg)
    _copy_file(src=src, dst=dst, filename=struct.config_filename + '.json')
    _copy_file(src=src, dst=dst, filename=struct.grammar_filename + '.bnf')

    if create_imports:
        # building : <lang_name>/imports/
        imports_dst = os.path.join(dst, struct.imports_dirname)
        os.mkdir(imports_dst)
