import dataclasses
import importlib
import os.path
import pathlib

from core.langs import bnf
from ._abc import Loader

__all__ = [
    'ReaderLoader'
]


# TODO : check this function works as intended
def _get_module_path(__fp: str) -> str:
    """Convert a module filepath to a valid import path."""
    assert os.path.exists(__fp), "should exists."
    assert __fp.endswith('.py'), "should be a module."
    parts = os.path.splitext(os.path.relpath(__fp, pathlib.Path().resolve()).replace('\\', '/'))[0].split('/')
    assert all(part.isidentifier() for part in parts), f"should have a valid module path not {__fp!r}."
    return ".".join(parts)


@dataclasses.dataclass(frozen=True, order=True)
class ReaderLoader(Loader):
    def load(self) -> bnf.Reader:
        assert isinstance(self.src, str)
        src = os.path.join(self.root, self.src).replace('\\', '/')
        module = importlib.import_module(name=_get_module_path(src))

        if not hasattr(module, "reader"):
            raise Exception(f"Can't load reader from the reader module.")

        reader = getattr(module, "reader")

        if not isinstance(reader, bnf.Reader):
            raise Exception(f"Loaded reader from {src!r} is not a `website.language.bnf.Reader` object.")

        return reader
