import collections
import time
import typing

__all__ = [
    'resume_to_dict',
    'nested_map',
    'time_logger',
    'memoize',
    'prevent_infinite_recursion_loop',
    'develop_tree',
]

E = typing.TypeVar('E')
F = typing.TypeVar('F')


def resume_to_dict(data_list: typing.Iterator[tuple[E, F]]) -> collections.defaultdict[E, list[F]]:
    data_dict: collections.defaultdict[E, list[F]] = collections.defaultdict(list)

    for e, f in data_list:
        data_dict[e].append(f)

    return data_dict


def nested_map(function: typing.Callable[[E], typing.Iterator[F]], iterable: typing.Iterator[E]) -> typing.Iterator[F]:
    return (inner for outer in iterable for inner in function(outer))


class TimeLogger:
    def __init__(self):
        self._register = {}

    def register_function(self, label: str):
        self._register[label] = []

        def wrapper(function):
            def wrapped(*args, **kwargs):
                ti = time.perf_counter()
                result = function(*args, **kwargs)
                tf = time.perf_counter()
                self._register[label].append(tf - ti)
                return result

            return wrapped

        return wrapper

    def display(self):
        """Display the perfs."""
        for label, times in self._register.items():
            print(f"\n{label!r} :"
                  f"\n\tnumber of calls : {len(times) if times else '0'}"
                  f"\n\ttotal time      : {sum(times) if times else '0'}s"
                  f"\n\tmax time        : {max(times) if times else '0'}s"
                  f"\n\tmin time        : {min(times) if times else '0'}s"
                  f"\n\tmean time       : {sum(times) / len(times) if times else '0'}s")


time_logger = TimeLogger()


def memoize(function):
    _register = {}

    def wrapped(*args):
        try:
            result = _register[args]

        except KeyError:
            result = _register[args] = function(*args)

        return result

    return wrapped


def prevent_infinite_recursion_loop(function):
    _register = []

    def wrapped(*args):
        if args in _register:
            raise Exception(f"Infinite Recursion Error !")

        _register.append(args)
        result = function(*args)
        _register.remove(args)
        return result

    return wrapped


def develop_tree(
        root: E,
        generate: typing.Callable[[E], F],
        get_targets: typing.Callable[[F], list[E]],
        can_be_origin: typing.Callable[[E], bool],
        as_origin: typing.Callable[[E], E]
) -> tuple[list[E], list[F]]:
    origins: list[E] = [root]
    choices: list[F] = []

    def add_origin(item: E) -> None:
        if item not in origins:
            origins.append(item)

    index = 0
    while index < len(origins):
        assert len(choices) == index
        choice = generate(origins[index])
        choices.append(choice)

        for target in get_targets(choice):
            if can_be_origin(target):
                origin = as_origin(target)
                add_origin(origin)

        index += 1

    return origins, choices
