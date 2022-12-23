from __future__ import annotations

import dataclasses

__all__ = [
    'Cardinality',
]


@dataclasses.dataclass
class Cardinality:
    optional: int = 0
    multiple: int = 0
    
    @dataclasses.dataclass
    class Modifier:
        context: Cardinality
        optional: bool = False
        multiple: bool = False
        
        def __enter__(self):
            if self.optional:
                self.context.optional += 1
            if self.multiple:
                self.context.multiple += 1
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.optional:
                self.context.optional -= 1
            if self.multiple:
                self.context.multiple -= 1
    
    def __call__(self, optional: bool = False, multiple: bool = False) -> Cardinality.Modifier:
        return Cardinality.Modifier(context=self, optional=optional, multiple=multiple)


if __name__ == '__main__':
    ctx = Cardinality()
    print(ctx.optional, ctx.multiple)
    with ctx(optional=True):
        print(ctx.optional, ctx.multiple)
        with ctx(optional=True):
            print(ctx.optional, ctx.multiple)
        print(ctx.optional, ctx.multiple)
    print(ctx.optional, ctx.multiple)
