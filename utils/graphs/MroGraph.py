import dataclasses

from .DirectedGraph import DirectedGraph

__all__ = [
    'MroGraph'
]


@dataclasses.dataclass
class MroGraph(DirectedGraph):
    def register(self, namespace: dict) -> None:
        """Register all the classes defined in the `namespace`."""
        for key, val in namespace.items():
            if isinstance(val, type):
                for sub_cls in val.__subclasses__():
                    self.add_link(val, sub_cls)
    
    @classmethod
    def make(cls, *modules) -> 'MroGraph':
        """Make a `MroGraph` instance using the classes defined in the given `modules`."""
        mro = cls()
        for module in modules:
            mro.register(module.__dict__)
        return mro
