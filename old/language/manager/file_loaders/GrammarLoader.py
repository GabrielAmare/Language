import dataclasses
import os.path
import typing

from website.tools.file_utils import load_file
from ._abc import Loader

__all__ = [
    'GrammarLoader'
]


def _is_file_path(o) -> bool:
    return isinstance(o, str)


def _is_file_path_list(o) -> bool:
    return isinstance(o, list) and all(isinstance(e, str) for e in o)


def _make_header(name: str, width: int = 120):
    title = name.upper().replace('_', ' ')
    return (f"{width * '#'}\n"
            f"# {title}\n"
            f"{width * '#'}")


def _remove_comments(text: str, comment_prefix: str = '#') -> str:
    return '\n'.join(line for line in text.split('\n') if not line.lstrip().startswith(comment_prefix))


def _remove_double_newline(text: str) -> str:
    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    return text


def _remove_trailing_newline(text: str) -> str:
    return text.strip('\n')


def _force_newline_after_group(text: str) -> str:
    lines = []
    for line in text.split('\n'):
        if lines and lines[-1].startswith('group ') and line != '':
            lines.append('')
        lines.append(line)

    return '\n'.join(lines)


def _align_definitions(text: str) -> str:
    items = []
    width_left = 0
    for line in text.split('\n'):
        if line.startswith('branch') or line.startswith('group') or line.startswith('alias'):
            left, right = line.split(':=', 1)
            right = ' := ' + right.lstrip()
        else:
            left = line
            right = ''
        width_left = max(width_left, len(left))
        items.append((left, right))

    lines = []
    for left, right in items:
        lines.append(left.ljust(width_left, ' ') + right)

    return '\n'.join(lines)


@dataclasses.dataclass(frozen=True)
class GrammarLoader(Loader):
    option: typing.Callable[[str], bool]

    def _section(self, __name: str) -> str:
        content = load_file(os.path.join(self.root, __name))

        if self.option("remove-comments"):
            content = _remove_comments(content)

        if self.option("remove-double-newline"):
            content = _remove_double_newline(content)

        if self.option("remove-trailing-newline"):
            content = _remove_trailing_newline(content)

        if self.option("force-newline-after-group"):
            content = _force_newline_after_group(content)

        if self.option("align-definitions"):
            content = _align_definitions(content)

        return content

    @property
    def _sections(self) -> typing.Iterator[str]:
        if len(self.names) == 0:
            yield '# EMPTY GRAMMAR'

        elif len(self.names) == 1:
            yield self._section(self.names[0])

        else:
            for name in self.names:
                key = os.path.splitext(os.path.basename(name))[0]
                yield _make_header(key)
                yield self._section(name)

    def load(self) -> str:
        return '\n\n'.join(self._sections)
