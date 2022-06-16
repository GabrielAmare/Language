from __future__ import annotations

import abc
import dataclasses
import json
import os
import typing

__all__ = [
    # functions
    'load_json_file',
    'save_json_file',
    'load_text_file',
    'save_text_file',

    # classes
    'Resource',
    'Directory',
    'TextFile',
    'JsonFile',
]


def _force_suffix(expr: str, suffix: str) -> str:
    if expr.endswith(suffix):
        return expr

    return expr + suffix


def load_text_file(path: str) -> str:
    with open(path, mode='r', encoding='utf-8') as file:
        return file.read()


def save_text_file(path: str, content: str) -> None:
    with open(path, mode='w', encoding='utf-8') as file:
        file.write(content)


def load_json_file(path: str) -> dict | list:
    with open(_force_suffix(path, '.json'), mode='r', encoding='utf-8') as file:
        return json.load(file)


def save_json_file(path: str, data: dict | list | tuple, indent: int = None, compact: bool = False):
    if compact:
        separators = (',', ':')
    else:
        separators = None
    with open(_force_suffix(path, '.json'), mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=indent, separators=separators)


@dataclasses.dataclass
class Resource(abc.ABC):
    root: str | Directory
    name: str

    @property
    def path(self) -> str:
        if isinstance(self.root, str):
            return os.path.join(self.root, self.name)

        elif isinstance(self.root, Directory):
            return os.path.join(self.root.path, self.name)

        else:
            raise NotImplementedError

    @abc.abstractmethod
    def save(self) -> None:
        """Save the resource in memory."""


@dataclasses.dataclass
class Directory(Resource):
    _resources: typing.List[Resource] = dataclasses.field(default_factory=list)

    def save(self) -> None:
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        for resource in self._resources:
            resource.save()

    def directory(self, name: str) -> Directory:
        resource = Directory(root=self, name=name)
        self._resources.append(resource)
        return resource

    def text_file(self, name: str, content: str) -> TextFile:
        resource = TextFile(root=self, name=name, content=content)
        self._resources.append(resource)
        return resource

    def python_module(self, name: str, content: str) -> TextFile:
        resource = TextFile(root=self, name=_force_suffix(name, '.py'), content=content)
        self._resources.append(resource)
        return resource

    def json_file(self, name: str, data: list | dict) -> JsonFile:
        resource = JsonFile(root=self, name=_force_suffix(name, '.json'), data=data)
        self._resources.append(resource)
        return resource


@dataclasses.dataclass
class TextFile(Resource):
    content: str

    def save(self) -> None:
        save_text_file(self.path, self.content)


@dataclasses.dataclass
class JsonFile(Resource):
    data: list | dict

    def save(self) -> None:
        save_json_file(self.path, self.data, indent=2)
