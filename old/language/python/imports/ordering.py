import typing

from website.language.base.decorators import *
from website.language.python.lang.models import *


@__method__
def order(self: Import):
    # TODO : make this cleaner !!!
    return ' '.join(map(str, self.targets))


@__method__
def order(self: DottedAsName) -> tuple[str, str]:
    return '.'.join(name.content for name in self.names), self.as_name.content if self.as_name else ''


@__method__
def order(self: ImportPath) -> tuple[int, str]:
    if isinstance(self, AbsoluteImportPath):
        return 0, str(self)
    elif isinstance(self, RelativeImportPath):
        return 1, str(self)
    else:
        raise NotImplementedError


@__method__
def order(self: ImportFrom):
    return self.path.order()
