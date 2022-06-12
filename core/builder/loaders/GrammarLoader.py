import dataclasses
import os.path
import typing

from core.builder.options import Grammar
from tools import files
from ._abc import Loader

__all__ = [
    'GrammarLoader'
]


class ModifySection:
    @staticmethod
    def remove_comments(text: str, comment_prefix: str = '#') -> str:
        return '\n'.join(line for line in text.split('\n') if not line.lstrip().startswith(comment_prefix))

    @staticmethod
    def remove_double_newline(text: str) -> str:
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')

        return text

    @staticmethod
    def remove_trailing_newline(text: str) -> str:
        return text.strip('\n')

    @staticmethod
    def force_newline_after_group(text: str) -> str:
        lines = []
        for line in text.split('\n'):
            if lines and lines[-1].startswith('group ') and line != '':
                lines.append('')
            lines.append(line)

        return '\n'.join(lines)

    @staticmethod
    def align_definitions(text: str) -> str:
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

    binds = [
        (Grammar.REMOVE_COMMENTS, remove_comments),
        (Grammar.REMOVE_DOUBLE_NEWLINE, remove_double_newline),
        (Grammar.REMOVE_TRAILING_NEWLINE, remove_trailing_newline),
        (Grammar.FORCE_NEWLINE_AFTER_GROUP, force_newline_after_group),
        (Grammar.ALIGN_DEFINITIONS, align_definitions),
    ]


def _make_header(name: str, width: int = 120):
    title = name.upper().replace('_', ' ')
    return (f"{width * '#'}\n"
            f"# {title}\n"
            f"{width * '#'}")


@dataclasses.dataclass(frozen=True)
class GrammarLoader(Loader):
    option: typing.Callable[[str], bool]

    def _section(self, __name: str) -> str:
        content = files.load_text_file(os.path.join(self.root, __name))

        for key, function in ModifySection.binds:
            if self.option(key):
                content = function(content)

        return content

    @property
    def _sections(self) -> typing.Iterator[str]:
        if len(self.names) == 0:
            yield '# EMPTY GRAMMAR'

        elif len(self.names) == 1:
            yield self._section(self.names[0])

        else:
            for name in self.names:
                section_name = os.path.splitext(os.path.basename(name))[0]
                yield _make_header(section_name)
                yield self._section(name)

    def load(self) -> str:
        return '\n\n'.join(self._sections)
