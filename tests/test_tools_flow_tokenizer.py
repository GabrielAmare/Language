import dataclasses
import string
import typing
import unittest

import js2py

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


class TestToolsFlowTokenizer(unittest.TestCase):
    
    def __testing(self, flow: Flow, cases: list[dict]):
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
        
        self.__testing(flow, [
            {
                "label": "Success",
                "src": 'x',
                "tokens": ['0 1 X x']
            },
            {
                "label": "Success -> Success",
                "src": "xx",
                "tokens": ['0 1 X x', '1 2 X x']
            },
            {
                "label": "Failure",
                "src": "y",
                "tokens": ['0 1 ~ERROR y']
            },
            {
                "label": "Success -> Failure",
                "src": "xy",
                "tokens": ['0 1 X x', '1 2 ~ERROR y']
            },
        ])
    
    def test_method_match(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').build('y', 'XY')
        
        finalize(flow)
        
        self.__testing(flow, [
            {
                "label": "Success",
                "src": "xy",
                "tokens": ['0 2 XY xy']
            },
            {
                "label": "Success -> Success",
                "src": "xyxy",
                "tokens": ['0 2 XY xy', '2 4 XY xy']
            },
            {
                "label": "Failure (1st item)",
                "src": "z",
                "tokens": ['0 1 ~ERROR z']
            },
            {
                "label": "Failure (2nd item)",
                "src": "xz",
                "tokens": ['0 2 ~ERROR xz']
            },
        ])
    
    def test_method_repeat(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').repeat('y').build('z', 'X*YZ')
        
        finalize(flow)
        
        self.__testing(flow, [
            {
                "label": "Success (x0)",
                "src": "xz",
                "tokens": ['0 2 X*YZ xz']
            },
            {
                "label": "Success (x1)",
                "src": "xyz",
                "tokens": ['0 3 X*YZ xyz']
            },
            {
                "label": "Success (x2)",
                "src": "xyyz",
                "tokens": ['0 4 X*YZ xyyz']
            },
            {
                "label": "Failure (x0)",
                "src": "xt",
                "tokens": ['0 2 ~ERROR xt']
            },
            {
                "label": "Failure (x1)",
                "src": "xyt",
                "tokens": ['0 3 ~ERROR xyt']
            },
            {
                "label": "Failure (x2)",
                "src": "xyyt",
                "tokens": ['0 4 ~ERROR xyyt']
            },
        ])
    
    def test_method_repeat_plus(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').repeat_plus('y').build('z', 'X+YZ')
        
        finalize(flow)
        
        self.__testing(flow, [
            {
                "label": "Success (x1)",
                "src": "xyz",
                "tokens": ['0 3 X+YZ xyz']
            },
            {
                "label": "Success (x2)",
                "src": "xyyz",
                "tokens": ['0 4 X+YZ xyyz']
            },
            {
                "label": "Failure : missing required item (x0)",
                "src": "xz",
                "tokens": ['0 2 ~ERROR xz']
            },
            {
                "label": "Failure (x0)",
                "src": "xt",
                "tokens": ['0 2 ~ERROR xt']
            },
            {
                "label": "Failure (x1)",
                "src": "xyt",
                "tokens": ['0 3 ~ERROR xyt']
            },
            {
                "label": "Failure (x2)",
                "src": "xyyt",
                "tokens": ['0 4 ~ERROR xyyt']
            },
        ])
    
    def test_combination(self):
        """Test combination."""
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.match('x').build('y', 'XY')
        origin.match('x').build('z', 'XZ')
        
        finalize(flow)
        
        self.__testing(flow, [
            {
                "label": "Failure (missing second element)",
                "src": "x",
                "tokens": ['0 1 ~ERROR x']
            },
            {
                "label": "Success (first pattern)",
                "src": "xy",
                "tokens": ['0 2 XY xy']
            },
            {
                "label": "Success (second pattern)",
                "src": "xz",
                "tokens": ['0 2 XZ xz']
            },
            {
                "label": "Failure (wrong second element)",
                "src": "xt",
                "tokens": ['0 2 ~ERROR xt']
            },
        ])
    
    def test_integer_and_decimal(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        # integer
        origin.repeat_plus(string.digits).default.build('Integer')
        
        # decimal
        origin.repeat_plus(string.digits).match('.').repeat(string.digits).default.build('Decimal')
        origin.match('.').repeat_plus(string.digits).default.build('Decimal')
        
        finalize(flow)
        
        self.__testing(flow, [
            {
                "label": "",
                "src": "0",
                "tokens": ['0 1 Integer 0']
            },
            {
                "label": "",
                "src": "1",
                "tokens": ['0 1 Integer 1']
            },
            {
                "label": "",
                "src": "12",
                "tokens": ['0 2 Integer 12']
            },
            {
                "label": "",
                "src": "0.1",
                "tokens": ['0 3 Decimal 0.1']
            },
            {
                "label": "",
                "src": "0.",
                "tokens": ['0 2 Decimal 0.']
            },
            {
                "label": "",
                "src": ".1",
                "tokens": ['0 2 Decimal .1']
            },
        ])
    
    def test_skip_token(self):
        flow = Flow()
        origin = Proxy(flow, 0)
        
        origin.build('x', '')
        origin.build('y', 'Y')
        
        finalize(flow)
        
        self.__testing(flow, [
            {
                "label": "Single item",
                "src": "x",
                "tokens": []
            },
            {
                "label": "Wrapped item",
                "src": "yxy",
                "tokens": ['0 1 Y y', '2 3 Y y']
            },
        ])


if __name__ == '__main__':
    unittest.main()
