import os
import string

import tools.files
from tools.flow.tokenizer import *

__all__ = [
    'flow_database'
]


def _create(version: tuple[int, int, int]) -> Flow:
    flow = Flow()
    entry = Proxy(flow, 0)
    
    entry.build('\n', 'NEWLINE')
    entry.match('/').match('/').default.repeat().build('\n' + EOT, 'Comment', options=0)
    
    if (1, 1, 0) <= version:
        mlc1 = entry.match('/').match('*').default.repeat()
        mlc2 = mlc1.match('*')
        mlc2.build('/', 'Comment')
        mlc2.default.match(to=mlc1)
    
    table_body = (
        entry
        .sequence(*"table", build="KW_TABLE", to=NEW)
        .repeat_plus(' ').default.build('WHITESPACE', to=NEW)
        .repeat_plus(string.ascii_letters).default.build('TableName', to=NEW)
        .repeat_plus(' ').default.build('WHITESPACE', to=NEW)
        .build('{', 'LS', to=NEW)
    )
    
    field = (
        table_body
        .build('\n', 'NEWLINE')
        .repeat_plus(' ').default.build('WHITESPACE', to=NEW)
    )
    (
        field
        .build('\n', 'NEWLINE')
        .repeat_plus(' ').default.build('WHITESPACE', to=field)
    )
    (
        table_body
        .build('\n', 'NEWLINE', to=NEW)
        .build('}', 'RS')
    )
    
    field1 = Proxy(flow, flow.new_state())
    
    field.build('!', 'UnitField', to=field1)
    field.build('*', 'ListField', to=field1)
    field.build('?', 'UnitOptionalField', to=field1)
    
    if version >= (1, 2, 0):
        field2 = (
            field1
            .repeat_plus(string.ascii_letters).default.build('FieldName', to=NEW)
            .build('[', 'LB', to=NEW)
            .repeat_plus(string.ascii_letters).default.build('FieldType', to=NEW)
            .build(']', 'RB', to=NEW)
        )
        
        field3 = (
            field2
            .build('=', 'EQUAL', to=NEW)
        )
        field3.match('"').default.repeat().build('"', 'String', to=table_body)
        field3.sequence(*"auto", build="AutoIncrement")
        
        field2.default.goto(to=table_body)
    else:
        (
            field1
            .repeat_plus(string.ascii_letters).default.build('FieldName', to=NEW)
            .build('[', 'LB', to=NEW)
            .repeat_plus(string.ascii_letters).default.build('FieldType', to=NEW)
            .build(']', 'RB', to=table_body)
        )
    
    finalize(flow)
    
    return flow


def _style():
    return {
        'Name': {
            'color': 'orange'
        }
    }


if __name__ == '__main__':
    root = "../../interactive_ide/src/assets/langs/"
    assert os.path.exists(root)
    name = "database"
    for version in [(1, 0, 0), (1, 1, 0), (1, 2, 0)]:
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
