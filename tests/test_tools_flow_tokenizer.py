import string
import unittest

from tools.flow.tokenizer import *
from tools.flow.tokenizer.port.portable import make_tokenizer_function


def flow_x():
    flow = Flow()
    origin = Proxy(flow, 0)
    
    origin.build('x', 'X')
    
    finalize(flow)
    
    return flow


def flow_xy():
    flow = Flow()
    origin = Proxy(flow, 0)
    
    origin.match('x').build('y', 'XY')
    
    finalize(flow)
    
    return flow


def flow_x_star_y_z():
    flow = Flow()
    origin = Proxy(flow, 0)
    
    origin.match('x').repeat('y').build('z', 'X*YZ')
    
    finalize(flow)
    
    return flow


def flow_x_plus_y_z():
    flow = Flow()
    origin = Proxy(flow, 0)
    
    origin.match('x').repeat_plus('y').build('z', 'X+YZ')
    
    finalize(flow)
    
    return flow


def flow_integer_and_decimal():
    flow = Flow()
    origin = Proxy(flow, 0)
    
    # integer
    origin.repeat_plus(string.digits).default.build('Integer')
    
    # decimal
    origin.repeat_plus(string.digits).match('.').repeat(string.digits).default.build('Decimal')
    origin.match('.').repeat_plus(string.digits).default.build('Decimal')
    
    finalize(flow)
    
    return flow


def flow_xy_or_xz():
    flow = Flow()
    origin = Proxy(flow, 0)
    
    origin.match('x').build('y', 'XY')
    origin.match('x').build('z', 'XZ')
    
    finalize(flow)
    
    return flow


class TestToolsFlowTokenizer(unittest.TestCase):
    def test_001(self):
        """Test the `build` method"""
        internal = flow_x()
        external = make_tokenizer_function(internal.data)
        
        for function in (internal, external):
            # Success
            self.assertEqual(
                first=list(function('x')),
                second=[
                    Token('X', 'x', 0, 1)
                ],
                msg=""
            )
            
            # Success -> Success
            self.assertEqual(
                first=list(function('xx')),
                second=[
                    Token('X', 'x', 0, 1),
                    Token('X', 'x', 1, 2)
                ],
                msg=""
            )
            
            # Failure
            self.assertEqual(
                first=list(function('y')),
                second=[
                    Token('~ERROR', 'y', 0, 1)
                ],
                msg=""
            )
            
            # Success -> Failure
            self.assertEqual(
                first=list(function('xy')),
                second=[
                    Token('X', 'x', 0, 1),
                    Token('~ERROR', 'y', 1, 2)
                ],
                msg=""
            )
    
    def test_002(self):
        """Test the `match` method"""
        internal = flow_xy()
        external = make_tokenizer_function(internal.data)
        
        for function in (internal, external):
            # Success
            self.assertEqual(
                first=list(function('xy')),
                second=[
                    Token(type='XY', content='xy', at=0, to=2)
                ],
                msg=""
            )
            
            # Success -> Success
            self.assertEqual(
                first=list(function('xyxy')),
                second=[
                    Token(type='XY', content='xy', at=0, to=2),
                    Token(type='XY', content='xy', at=2, to=4)
                ],
                msg=""
            )
            
            # Failure (1st item)
            self.assertEqual(
                first=list(function('z')),
                second=[
                    Token(type='~ERROR', content='z', at=0, to=1)
                ],
                msg=""
            )
            
            # Failure (2nd item)
            self.assertEqual(
                first=list(function('xz')),
                second=[
                    Token(type='~ERROR', content='xz', at=0, to=2)
                ],
                msg=""
            )
    
    def test_003(self):
        """Test the `repeat` method"""
        internal = flow_x_star_y_z()
        external = make_tokenizer_function(internal.data)
        
        for function in (internal, external):
            # Success (x0)
            self.assertEqual(
                first=list(function('xz')),
                second=[
                    Token(type='X*YZ', content='xz', at=0, to=2)
                ],
                msg=""
            )
            
            # Success (x1)
            self.assertEqual(
                first=list(function('xyz')),
                second=[
                    Token(type='X*YZ', content='xyz', at=0, to=3)
                ],
                msg=""
            )
            
            # Success (x2)
            self.assertEqual(
                first=list(function('xyyz')),
                second=[
                    Token(type='X*YZ', content='xyyz', at=0, to=4)
                ],
                msg=""
            )
            
            # Failure (x0)
            self.assertEqual(
                first=list(function('xt')),
                second=[
                    Token(type='~ERROR', content='xt', at=0, to=2)
                ],
                msg=""
            )
            
            # Failure (x1)
            self.assertEqual(
                first=list(function('xyt')),
                second=[
                    Token(type='~ERROR', content='xyt', at=0, to=3)
                ],
                msg=""
            )
            
            # Failure (x2)
            self.assertEqual(
                first=list(function('xyyt')),
                second=[
                    Token(type='~ERROR', content='xyyt', at=0, to=4)
                ],
                msg=""
            )
    
    def test_004(self):
        """Test the `repeat` method"""
        internal = flow_x_plus_y_z()
        external = make_tokenizer_function(internal.data)
        
        for function in (internal, external):
            # Success (x1)
            self.assertEqual(
                first=list(function('xyz')),
                second=[
                    Token(type='X+YZ', content='xyz', at=0, to=3)
                ],
                msg=""
            )
            
            # Success (x2)
            self.assertEqual(
                first=list(function('xyyz')),
                second=[
                    Token(type='X+YZ', content='xyyz', at=0, to=4)
                ],
                msg=""
            )
            
            # Failure : missing required item (x0)
            self.assertEqual(
                first=list(function('xz')),
                second=[
                    Token(type='~ERROR', content='xz', at=0, to=2)
                ],
                msg=""
            )
            
            # Failure (x0)
            self.assertEqual(
                first=list(function('xt')),
                second=[
                    Token(type='~ERROR', content='xt', at=0, to=2)
                ],
                msg=""
            )
            
            # Failure (x1)
            self.assertEqual(
                first=list(function('xyt')),
                second=[
                    Token(type='~ERROR', content='xyt', at=0, to=3)
                ],
                msg=""
            )
            
            # Failure (x2)
            self.assertEqual(
                first=list(function('xyyt')),
                second=[
                    Token(type='~ERROR', content='xyyt', at=0, to=4)
                ],
                msg=""
            )
    
    def test_101(self):
        """Test combination."""
        internal = flow_xy_or_xz()
        external = make_tokenizer_function(internal.data)
        
        for function in (internal, external):
            # Failure (missing second element)
            self.assertEqual(first=list(function("x")), second=[
                Token(type='~ERROR', content='x', at=0, to=1)
            ], msg="")
            
            # Success (first pattern)
            self.assertEqual(first=list(function("xy")), second=[
                Token(type='XY', content='xy', at=0, to=2)
            ], msg="")
            
            # Success (second pattern)
            self.assertEqual(first=list(function("xz")), second=[
                Token(type='XZ', content='xz', at=0, to=2)
            ], msg="")
            
            # Failure (wrong second element)
            self.assertEqual(first=list(function("xt")), second=[
                Token(type='~ERROR', content='xt', at=0, to=2)
            ], msg="")
    
    def test_201(self):
        """Test the combinining of integer & decimal."""
        internal = flow_integer_and_decimal()
        external = make_tokenizer_function(internal.data)
        
        for function in (internal, external):
            self.assertEqual(first=list(function("0")), second=[
                Token(type='Integer', content='0', at=0, to=1)
            ], msg="")
            self.assertEqual(first=list(function("1")), second=[
                Token(type='Integer', content='1', at=0, to=1)
            ], msg="")
            self.assertEqual(first=list(function("12")), second=[
                Token(type='Integer', content='12', at=0, to=2)
            ], msg="")
            self.assertEqual(first=list(function("0.1")), second=[
                Token(type='Decimal', content='0.1', at=0, to=3)
            ], msg="")
            self.assertEqual(first=list(function("0.")), second=[
                Token(type='Decimal', content='0.', at=0, to=2)
            ], msg="")
            self.assertEqual(first=list(function(".1")), second=[
                Token(type='Decimal', content='.1', at=0, to=2)
            ], msg="")


if __name__ == '__main__':
    unittest.main()
