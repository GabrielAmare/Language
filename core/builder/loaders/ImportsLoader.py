import dataclasses
import os.path

from core.langs import python as py
from tools import console
from ._abc import Loader

__all__ = [
    'ImportsLoader'
]


@dataclasses.dataclass(frozen=True)
class ImportsLoader(Loader):
    python_version: tuple[int, int, int]

    def load(self) -> list[py.DynamicModule]:
        assets = []
        for name in self.names:
            fp = os.path.join(self.root, name)

            if not os.path.exists(fp):
                console.warning(f"{fp!r} does not exists !")
                continue

            with console.context(message=f"loading {fp!r}.", success="ok"):
                module = py.Module.from_file(fp)

            dynamic = py.DynamicModule.from_module(module, version=self.python_version)

            assets.append(dynamic)

        return assets
