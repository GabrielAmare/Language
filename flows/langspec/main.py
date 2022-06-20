import os
import string

import tools.files
from tools.flow.tokenizer import *


def _create(version: tuple[int, int, int]) -> Flow:
    flow = Flow()
    entry = Proxy(flow, 0)
    
    entry.match('#').default.repeat().build(EOT + '\n', 'Comment', options=0)
    
    entry.repeat_plus(string.ascii_letters).default.build('Name')
    
    entry.repeat_plus(' ').default.build('WHITESPACE')
    
    entry.build('\n', 'NEWLINE')
    entry.build('=', 'EQUAL')
    entry.build('|', 'VBAR')
    
    string1 = entry.match("'").default.repeat()
    string1.match('\\').default.match(to=string1)
    string1.build("'", 'String')
    
    string2 = entry.match('"').default.repeat()
    string2.match('\\').default.match(to=string2)
    string2.build('"', 'String')
    
    entry.build('*', 'STAR')
    entry.build('+', 'PLUS')
    entry.build('(', 'LP')
    entry.build(')', 'RP')
    
    finalize(flow)
    
    return flow


if __name__ == '__main__':
    root = "../../interactive_ide/src/assets/langs/"
    assert os.path.exists(root)
    name = "langspec"
    
    for version in [(1, 0, 0)]:
        major, minor, patch = version
        flow = _create(version)
        
        # from tools.flow.render_graph import TokenizerGraph
        #
        # TokenizerGraph(flow=flow_database, name="database").render()
        
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
