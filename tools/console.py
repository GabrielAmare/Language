"""
    Module to easily display info into the console.
"""
import dataclasses
import functools
import time

RGB = tuple[int, int, int]
COLORS = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]


def _make_color(ref: str | RGB | None, key: int):
    """

    :param ref: the color reference
    :param key: 3 -> foreground | 4 -> background | 9 -> bright foreground | 10 -> bright background
    :return:
    """
    if key not in (3, 4, 9, 10):
        raise ValueError(f"Invalid color key {key!r}. Should be 3 (fg), 4 (bg), 9 (bright fg) or 10 (bright bg).")

    if ref is None:
        return ''

    elif isinstance(ref, str):
        if ref not in COLORS:
            raise ValueError(f"Undefined color ref {ref!r}.")

        return f"\033[{key}{COLORS.index(ref)}m"

    elif isinstance(ref, tuple):
        if len(ref) != 3:
            raise ValueError(f"Invalid size for an rgb color ref {len(ref)!r}.")

        if not all(isinstance(c, int) and 0 <= c < 256 for c in ref):
            raise ValueError(f"Invalid values for red | blue | green components of the rgb color ref {ref!r}.")

        return f"\033[{key}8;2;{ref[0]};{ref[1]};{ref[2]}m"

    else:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class Style:
    bg: str | RGB | None = None
    fg: str | RGB | None = None
    bright_bg: bool = False
    bright_fg: bool = False
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False

    @functools.cached_property
    def foreground(self) -> str:
        return _make_color(ref=self.fg, key=9 if self.bright_fg else 3)

    @functools.cached_property
    def background(self) -> str:
        return _make_color(ref=self.bg, key=10 if self.bright_bg else 4)

    @functools.cached_property
    def prefix(self):
        r = self.background + self.foreground
        if self.bold:
            r += '\033[1m'
        if self.italic:
            r += '\033[3m'
        if self.underline:
            r += '\033[4m'
        if self.strikethrough:
            r += '\033[9m'
        return r

    def __call__(self, text: str) -> str:
        return self.prefix + text + '\033[0m'


@dataclasses.dataclass
class Config:
    line_order: int = 3
    indent_size: int = 2
    indent_level_ceil: int = 4


@dataclasses.dataclass
class State:
    current_line: int = 0
    indent_level: int = 0
    debug: bool = False
    warning: bool = True


config = Config()
state = State()

FAILURE = object()
SUCCESS = object()
WARNING = object()
MESSAGE = object()
INFO = object()
DEBUG = object()
SCOPE = object()
CLOSE_SCOPE = object()


def _get_prefix(mode) -> str:
    if mode is None:
        return ' '
    if mode is FAILURE:
        return Style(bg=(0, 0, 0), fg="red")('✗')
    elif mode is SUCCESS:
        return Style(bg=(0, 0, 0), fg="green")('✓')
    elif mode is WARNING:
        return Style(bg=(0, 0, 0), fg="yellow")('!')
    elif mode is MESSAGE:
        return Style(bg=(0, 0, 0), fg="white")('-')
    elif mode is INFO:
        return '+'
    elif mode is DEBUG:
        return '~'
    elif mode is SCOPE:
        return Style(bg=(0, 0, 0), fg=(60, 60, 180))('>')
    elif mode is CLOSE_SCOPE:
        return '}'
    else:
        return '*'


def _get_style(mode) -> Style:
    if mode is FAILURE:
        return Style(fg="red")
    elif mode is SUCCESS:
        return Style(fg="green")
    elif mode is WARNING:
        return Style(fg="yellow")
    elif mode is MESSAGE:
        return Style(fg="white")
    elif mode is INFO:
        return Style(fg=(0, 0, 255))
    elif mode is DEBUG:
        return Style(fg="magenta")
    elif mode is SCOPE or mode is CLOSE_SCOPE:
        return Style(fg=(60, 60, 180))
    else:
        return Style()


def _print(*args, mode):
    if state.indent_level <= config.indent_level_ceil:
        line_no = str(state.current_line).zfill(config.line_order)
        message = ' '.join(map(str, args))
        prefix_start = ' '.join([
            line_no,
            '|',
            state.indent_level * config.indent_size * ' ',
            _get_prefix(mode),
        ])
        prefix_after = ' '.join([
            config.line_order * ' ',
            '|',
            state.indent_level * config.indent_size * ' ',
            _get_prefix(None),
        ])

        for index, line in enumerate(message.split('\n')):
            prefix = prefix_start if index == 0 else prefix_after
            print(prefix, _get_style(mode)(line))

        state.current_line += 1


def failure(*args):
    _print(*args, mode=FAILURE)


def success(*args):
    _print(*args, mode=SUCCESS)


def message(*args):
    _print(*args, mode=MESSAGE)


def warning(*args):
    if state.warning:
        _print(*args, mode=WARNING)


def info(*args):
    _print(*args, mode=INFO)


def debug(*args):
    if state.debug:
        _print(*args, mode=DEBUG)


def scope(*args):
    _print(*args, mode=SCOPE)


def _get_time_display(milliseconds: int):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    elif minutes:
        return f"{minutes}m {seconds}s"
    elif seconds:
        return f"{seconds}s {milliseconds}ms"
    else:
        return f"{milliseconds}ms"


@dataclasses.dataclass
class context:
    message: str
    success: str = ''
    failure: str = ''
    timer: bool = False

    def __enter__(self):
        self.time_at = time.time()
        scope(self.message + " {")
        state.indent_level += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.time_to = time.time()
        state.indent_level -= 1

        args = []

        if self.timer:
            milliseconds = int(1000 * (self.time_to - self.time_at))
            args.append(f"~{_get_time_display(milliseconds)}")

        if exc_type:
            if self.failure:
                failure(self.failure, *args)

        else:
            if self.success:
                success(self.success, *args)
