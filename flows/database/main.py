import string

import tools.files
from tools.flow.tokenizer import *

__all__ = [
    'flow_database'
]


def _create() -> Flow:
    flow = Flow()
    entry = Proxy(flow, 0)
    
    entry.repeat_plus(' ').default.build('')
    
    entry.repeat_plus(string.ascii_letters).default.build('Variable')
    
    entry.build('\n', 'NEWLINE')
    
    entry.match('/').match('/').default.repeat().build('\n' + EOT, 'Comment', options=0)
    
    entry.build('-', 'DASH')
    entry.build('*', 'STAR')
    
    entry.build('[', 'LB')
    entry.build(']', 'RB')
    
    entry.build('{', 'LS')
    entry.build('}', 'RS')
    
    finalize(flow)
    
    return flow


flow_database = _create()

if __name__ == '__main__':
    from tools.flow.render_graph import TokenizerGraph
    
    TokenizerGraph(flow=flow_database, name="database").render()
    
    tools.files.save_json_file(
        path="../../interactive_ide/src/assets/langs/database.json",
        data=flow_database.data
    )
