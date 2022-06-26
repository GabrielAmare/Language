import os
import string

import tools.files
from tools.flow.tokenizer import *


def mount_keyword(at: Proxy, expr, name, to=NEW) -> Proxy:
    for char in expr:
        at = at.match(char, to=NEW)
    
    at.match(string.ascii_letters, options=0, to=-1)
    return at.default.build(name, to=to)


def mount_variable(at: Proxy, to=NEW) -> Proxy:
    return (
        at
        .match(string.ascii_letters + '_')
        .repeat(string.ascii_letters + string.digits + '_')
        .default.build('Variable', to=to)
    )


def _create(v: tuple[int, int, int]) -> Flow:
    flow = Flow()
    entry = Proxy(flow, 0)

    after_string = (
        mount_keyword(entry, 'string', 'KW_STRING')
        
        .repeat_plus(' ').default.build('WHITESPACE', to=NEW)
        
        .match(string.ascii_letters + '_')
        .repeat(string.ascii_letters + '_' + string.digits)
        .default.build('Variable', to=NEW)

        .repeat_plus(' ').default.build('WHITESPACE', to=NEW)
        
        .build('=', 'EQUAL', to=NEW)
        
        .repeat_plus(' ').default.build('WHITESPACE', to=NEW)
        
        .match("'").default.repeat().build("'", "String")

    )
    # mount_variable(after_string, to=ENTRY)
    
    # mount_keyword(entry, 'regex', 'KW_REGEX')
    
    entry.build('\n', 'NEWLINE')
    
    finalize(flow)
    
    return flow


if __name__ == '__main__':
    root = "../../interactive_ide/src/assets/langs/"
    assert os.path.exists(root)
    name = "bnf"
    
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
