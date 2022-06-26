import dataclasses
import json

from flask import request
from flask_restful import Api, Resource

from . import models

__all__ = [
    'add_resources'
]


class Lang(Resource):
    def get(self, name: str, version: str):
        lang = models.Lang.load(name, version)
        data = dataclasses.asdict(lang)
        return data


def add_resources(api: Api) -> None:
    api.add_resource(Lang, '/langs/<name>/<version>')
