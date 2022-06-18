import dataclasses
import os
import string
import typing
import unittest

import js2py

import tools.console
from tools import files
from tools.flow.tokenizer import *
from tools.flow.tokenizer.port.portable import make_tokenizer_function

_JS_FUNC_ECMA5 = js2py.eval_js(files.load_text_file('../tools/flow/tokenizer/port/portable_ecma5.js'))


def _token_dict_to_list(token_dict: dict) -> str:
    return f"{token_dict['at']} {token_dict['to']} {token_dict['type']} {token_dict['content']}"


_TOKENIZER = typing.Callable[[str], list[str]]


def _make_builtin_tokenizer(flow: Flow) -> _TOKENIZER:
    def tokenize(src: str) -> list[str]:
        return list(map(_token_dict_to_list, map(dataclasses.asdict, flow(src))))
    
    return tokenize


def _make_portable_python_tokenizer(flow: Flow) -> _TOKENIZER:
    tokenizer = make_tokenizer_function(flow.data)
    
    def tokenize(src: str) -> list[str]:
        return list(map(_token_dict_to_list, map(dataclasses.asdict, tokenizer(src))))
    
    return tokenize


def _make_portable_javascript_ecma5_tokenizer(flow: Flow) -> _TOKENIZER:
    tokenizer = _JS_FUNC_ECMA5(flow.data)
    
    def tokenize(src: str) -> list[str]:
        return list(map(_token_dict_to_list, tokenizer(src)))
    
    return tokenize


_TOKENIZER_MAKERS = {
    "builtin": _make_builtin_tokenizer,
    "portable_python": _make_portable_python_tokenizer,
    "portable_javascript_ecma5": _make_portable_javascript_ecma5_tokenizer
}

REGENERATE = os.environ.get('REGEN_TESTS')  # Set this to True will regenerate all the tests


class TestToolsFlowTokenizer(unittest.TestCase):
    
    def __testing(self, flow: Flow, fp: str, generate: bool = REGENERATE):
        cases = files.load_json_file(fp)
        
        if generate:
            output = []
            
            function = _TOKENIZER_MAKERS["builtin"]
            tokenize = function(flow)
            for case in cases:
                if case['tokens'] is None or REGENERATE:
                    case['tokens'] = tokenize(case['src'])
                
                output.append(case)
            
            files.save_json_file(fp, output, indent=2)
            tools.console.success(f"regenerated {fp!r}.")
        
        else:
            for label, function in _TOKENIZER_MAKERS.items():
                tokenize = function(flow)
                for case in cases:
                    with self.subTest(f"{label}", label=case['label'], src=case['src']):
                        self.assertEqual(first=tokenize(case['src']), second=case['tokens'], msg="")
    
    def test_method_build(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        origin.build('x', 'X')
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_method_build.json")
    
    def test_method_match(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').build('y', 'XY')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_method_match.json")
    
    def test_method_repeat(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').repeat('y').build('z', 'X*YZ')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_method_repeat.json")
    
    def test_method_repeat_plus(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').repeat_plus('y').build('z', 'X+YZ')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_method_repeat_plus.json")
    
    def test_method_optional(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.optional('x').build('y', '?XY')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_method_optional.json")
    
    def test_combination(self):
        """Test combination."""
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').build('y', 'XY')
        origin.match('x').build('z', 'XZ')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_combination.json")
    
    def test_integer_and_decimal(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        # integer
        origin.repeat_plus(string.digits).default.build('Integer')
        
        # decimal
        origin.repeat_plus(string.digits).match('.').repeat(string.digits).default.build('Decimal')
        origin.match('.').repeat_plus(string.digits).default.build('Decimal')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_integer_and_decimal.json")
    
    def test_skip_token(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.build('x', '')
        origin.build('y', 'Y')
        
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_skip_token.json")
    
    def test_string(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        body = origin.match("'")
        body.default.repeat().build("'", "String")
        body.match('\\').default.match(to=body)
        finalize(flow)
        
        self.__testing(flow, "flow_tokenizer/test_string.json")
    
    def test_complex(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        # symbols
        origin.build('+', 'PLUS')
        origin.build('*', 'STAR')
        origin.build('-', 'MINUS')
        origin.build('/', 'SLASH')
        
        # whitespace
        origin.repeat_plus(' ').default.build('')
        
        # integer
        origin.repeat_plus(string.digits).default.build('Integer')
        
        # decimal
        origin.repeat_plus(string.digits).match('.').repeat(string.digits).default.build('Decimal')
        origin.match('.').repeat_plus(string.digits).default.build('Decimal')
        
        # simple quote string
        body = origin.match("'")
        body.default.repeat().build("'", "String")
        body.match('\\').default.match(to=body)
        
        # double quote string
        body = origin.match('"')
        body.default.repeat().build('"', "String")
        body.match('\\').default.match(to=body)
        
        letters_no_keywords = set(string.ascii_letters)
        
        def add_keyword(expr: str, name: str):
            letters_no_keywords.remove(expr[0])
            states = []
            state = origin
            for char in expr:
                state = state.match(char)
                states.append(state)
            state.default.build(name)
            
            def mount(ref: Proxy):
                for s, c in zip(states[:-1], expr[1:]):
                    s.match(string.ascii_letters.replace(c, ''), to=ref)
                
                states[-1].match(string.ascii_letters, to=ref)
            
            return mount
        
        # true & false
        mount_true = add_keyword("true", "True")
        mount_false = add_keyword("false", "False")
        
        # variable
        var = (origin
               .match(''.join(sorted(letters_no_keywords)))
               .repeat(string.ascii_letters))
        var.default.build("Variable")
        
        mount_true(var)
        mount_false(var)
        
        finalize(flow)
                
        self.__testing(flow, "flow_tokenizer/test_complex.json")


if __name__ == '__main__':
    unittest.main()
