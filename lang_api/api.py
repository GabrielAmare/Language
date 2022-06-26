from flask_restful import Api

from .app import app

__all__ = [
    'api'
]

api = Api(app)
