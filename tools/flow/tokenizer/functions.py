from .core import *
from .proxies import Proxy

__all__ = [
    'finalize',
]


def finalize(flow: Flow) -> None:
    # VALID
    Proxy(flow, 0).success(EOT)
    
    # ERROR
    err_1 = Proxy(flow, flow.new_state())
    err_1.failure(EOT, build='~ERROR')
    
    for manager in flow.managers.values():
        if manager.default is None:
            manager.default = Action(ActionParams(add=True, inc=True, clr=True, build='', clear=False), to=err_1.state)
        
        if not manager.verify(EOT):
            condition = Condition(EOT)
            if manager.default and manager.default.params.clear:
                params = ActionParams(add=False, inc=False, clr=True, build=manager.default.params.build, clear=False)
                action = Action(params, to=VALID)
            else:
                params = ActionParams(add=False, inc=False, clr=True, build='~ERROR', clear=False)
                action = Action(params, to=ERROR)
            
            handler = Handler(condition, action)
            manager.handlers.append(handler)
