import dataclasses

from core.langs.python import *
from ._abc import TextBuilder

__all__ = [
    'InitBuilder'
]


@dataclasses.dataclass
class InitBuilder(TextBuilder):
    def build(self) -> str:
        dynamic = DynamicModule(
            docstring=f"Init module for `{self.config.lang}` lang.",
            import_future_annotations=False,
            build_all_list=False,
            version=self.config.python_version
        )

        if self.config.dst.engine:
            dynamic.imports_all(path='.' + self.config.engine_fn)

        if self.config.dst.models:
            dynamic.imports_all(path='.' + self.config.models_fn)

        if self.config.dst.reader:
            dynamic.imports_all(path='.' + self.config.reader_fn)

        module = dynamic.to_module()

        return str(module)
