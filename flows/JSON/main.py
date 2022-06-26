import os
import string

import tools.files
from tools.flow.tokenizer import *


def _create(version: tuple[int, int, int]) -> Flow:
    flow = Flow()
    entry = Proxy(flow, 0)
    
    entry.build('{', 'LS')
    entry.build('}', 'RS')
    entry.build('[', 'LB')
    entry.build(']', 'RB')
    entry.build(':', 'COLON')
    entry.build(',', 'COMMA')
    entry.build('\n', 'NEWLINE')
    
    entry.repeat_plus(' ').default.build('WHITESPACE')
    entry.match('"').default.repeat().build('"', "String")
    entry.repeat_plus(string.digits).default.build('Integer')
    
    on_true = entry.match('t').match('r').match('u').match('e')
    on_true.default.build('TRUE')
    on_true.match(string.ascii_letters, options=0, to=ENTRY)

    on_false = entry.match('f').match('a').match('l').match('s').match('e')
    on_false.default.build('FALSE')
    on_false.match(string.ascii_letters, options=0, to=ENTRY)
    
    finalize(flow)
    
    return flow


if __name__ == '__main__':
    root = "../../interactive_ide/src/assets/langs/"
    assert os.path.exists(root)
    name = "json"
    
    for version in [(1, 0, 0)]:
        major, minor, patch = version
        flow = _create(version)
        
        dst = root + f"{name}_{major}_{minor}_{patch}/"
        
        if not os.path.exists(dst):
            os.mkdir(dst)
        
        tools.files.save_json_file(
            path=dst + "data.json",
            data=flow.data
        )
        
        tools.files.save_json_file(
            path=dst + "styles.json",
            data=tools.files.load_json_file("styles.json")
        )

        from tools.flow.render_graph import TokenizerGraph

        graph = TokenizerGraph(flow=flow, name="graph")
        
        graph.save(fp=dst + "graph.svg")
