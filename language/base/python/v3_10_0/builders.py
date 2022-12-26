import dataclasses
import typing

from .models import *

__all__ = [
    'SwitchBuilder',
]


# TODO : remove occurrences of this class.
@dataclasses.dataclass
class SwitchBuilder:
    cases: list[tuple[Expression, Block]] = dataclasses.field(default_factory=list)
    default: Block = None
    
    def add_case(self, test: Expression, statements: typing.Iterator[Statement]):
        statements = list(statements)
        self.cases.append((test, Block(statements or [PASS])))
    
    def set_default(self, statements: typing.Iterator[Statement]):
        statements = list(statements)
        self.default = Block(statements or [PASS])
    
    def build(self) -> typing.Iterator[Statement]:
        if self.cases:
            if self.default is None:
                res = None
            else:
                res = Else(block=self.default)
            
            first, *others = self.cases
            
            for test, block in reversed(others):
                res = Elif(test=test, block=block, alt=res)
            
            yield If(test=first[0], block=first[1], alt=res)
        elif self.default:
            yield from self.default.statements
        else:
            yield from ()
