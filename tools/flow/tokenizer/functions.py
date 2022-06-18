from .core import *
from .proxies import Proxy

__all__ = [
    'finalize',
]


def finalize(flow: Flow) -> None:
    # VALID
    Proxy(flow, 0).success(EOT, options=ADD + INC + CLR, build='~EOT')
    
    # ERROR
    err_1 = Proxy(flow, flow.new_state())
    err_1.failure(EOT, options=ADD + INC + CLR + CLEAR, build='~ERR')
    
    for state, manager in flow.managers.items():
        proxy = Proxy(flow, state)
        
        if manager.default is None:
            proxy.default.match(to=err_1.state)
        
        if not manager.verify(EOT):
            if manager.default and manager.default.params.options & CLEAR:
                proxy.build(EOT, manager.default.params.build, options=0)
            else:
                proxy.failure(EOT, options=ADD + INC + CLR + CLEAR, build='~ERR')
