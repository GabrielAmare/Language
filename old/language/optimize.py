import os.path

from website.language import bnf, semi, optilex, optilex_to_code
from website.language.enums import Lang
from website.tools.file_utils import save_file

__all__ = [
    'make_tokenizer',
]


def make_tokenizer(__file: str, reader: bnf.Reader, tokenizer_fn: str, lang: Lang) -> None:
    root = semi.BranchSet.from_bnf(reader.lexer)
    origin_select = root.to_optilex()
    code = optilex_to_code.origin_select_to_module(origin_select)

    if lang is Lang.PYTHON:
        save_file(
            dst=os.path.join(os.path.dirname(__file), tokenizer_fn + '.py'),
            content=str(code.to_python())
        )
    elif lang is Lang.JAVASCRIPT:
        save_file(
            dst=os.path.join(os.path.dirname(__file), tokenizer_fn + '.js'),
            content=str(code.to_javascript())
        )
    else:
        raise NotImplementedError(f"Can't make tokenizer for Lang {lang.name!r}.")
