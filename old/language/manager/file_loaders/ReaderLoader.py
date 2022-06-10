import dataclasses
import importlib
import os.path

from website.functions import get_module_path
from website.language import bnf
from website.language.constants import LEX
from ._abc import Loader

__all__ = [
    'ReaderLoader'
]


@dataclasses.dataclass(frozen=True, order=True)
class ReaderLoader(Loader):
    def load(self) -> bnf.Reader:
        assert isinstance(self.src, str)
        src = os.path.join(self.root, self.src).replace('\\', '/')
        module = importlib.import_module(name=get_module_path(src))

        if not hasattr(module, "reader"):
            raise Exception(f"Can't load {LEX.READER} from the {LEX.READER} module.")

        reader = getattr(module, "reader")

        if not isinstance(reader, bnf.Reader):
            raise Exception(f"Loaded {LEX.READER} from {src!r} is not a `website.language.bnf.Reader` object.")

        return reader
