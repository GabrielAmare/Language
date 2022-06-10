import dataclasses

from ._abc import JsonBuilder

__all__ = [
    'ConfigBuilder'
]


@dataclasses.dataclass
class ConfigBuilder(JsonBuilder):
    """Builder for the `lang/config.json` file."""

    def build(self, changelog: str = '') -> dict:
        return {
            'lang': self.config.lang,
            'version': '1.0.0',  # TODO : use dynamic version.
            'engine': {
                'lang': 'bnf',
                'version': '1.0.0'  # TODO : use dynamic version.
            },
            'changelog': changelog
        }
