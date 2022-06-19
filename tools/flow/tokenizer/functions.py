from .core import *
from .proxies import Proxy

__all__ = [
    'finalize',
]


def finalize(flow: Flow) -> None:
    # VALID
    Proxy(flow, 0).success(EOT, build='~EOT')
    
    # ERROR
    err_1 = Proxy(flow, flow.new_state())
    err_1.default.repeat().failure(EOT, build='~ERR')
    
    for state, manager in flow.managers.items():
        proxy = Proxy(flow, state)
        
        if manager.default is None:
            proxy.default.goto(to=err_1)
            continue
        
        if manager.verify(EOT):
            continue
        
        default_action = flow.actions[manager.default]
        
        if default_action.params.options == CLEAR:
            continue
        
        if default_action.params.options & CLEAR:
            proxy.build(EOT, default_action.params.build, options=0)
            continue
        
        proxy.failure(EOT, build="~ERR")
