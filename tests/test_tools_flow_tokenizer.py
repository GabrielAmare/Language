import unittest

from tools.flow.tokenizer import *


class TestToolsFlowTokenizer(unittest.TestCase):
    def test_001(self):
        """Test the `build` method"""
        flow = Flow()
        origin = ManagerProxy(flow, 0)

        origin.build('x', 'X')

        finalize(flow)

        # Success
        self.assertEqual(
            first=list(flow('x')),
            second=[
                Token('X', 'x', 0, 1)
            ],
            msg=""
        )

        # Success -> Success
        self.assertEqual(
            first=list(flow('xx')),
            second=[
                Token('X', 'x', 0, 1),
                Token('X', 'x', 1, 2)
            ],
            msg=""
        )

        # Failure
        self.assertEqual(
            first=list(flow('y')),
            second=[
                Token('~ERROR', 'y', 0, 1)
            ],
            msg=""
        )

        # Success -> Failure
        self.assertEqual(
            first=list(flow('xy')),
            second=[
                Token('X', 'x', 0, 1),
                Token('~ERROR', 'y', 1, 2)
            ],
            msg=""
        )

    def test_002(self):
        """Test the `match` method"""
        flow = Flow()
        origin = ManagerProxy(flow, 0)

        origin.match('x').build('y', 'XY')

        finalize(flow)

        # Success
        self.assertEqual(
            first=list(flow('xy')),
            second=[
                Token(type='XY', content='xy', at=0, to=2)
            ],
            msg=""
        )

        # Success -> Success
        self.assertEqual(
            first=list(flow('xyxy')),
            second=[
                Token(type='XY', content='xy', at=0, to=2),
                Token(type='XY', content='xy', at=2, to=4)
            ],
            msg=""
        )

        # Failure (1st item)
        self.assertEqual(
            first=list(flow('z')),
            second=[
                Token(type='~ERROR', content='z', at=0, to=1)
            ],
            msg=""
        )

        # Failure (2nd item)
        self.assertEqual(
            first=list(flow('xz')),
            second=[
                Token(type='~ERROR', content='xz', at=0, to=2)
            ],
            msg=""
        )

    def test_003(self):
        """Test the `repeat` method"""
        flow = Flow()
        origin = ManagerProxy(flow, 0)

        origin.match('x').repeat('y').build('z', 'X*YZ')

        finalize(flow)

        # Success (x0)
        self.assertEqual(
            first=list(flow('xz')),
            second=[
                Token(type='X*YZ', content='xz', at=0, to=2)
            ],
            msg=""
        )

        # Success (x1)
        self.assertEqual(
            first=list(flow('xyz')),
            second=[
                Token(type='X*YZ', content='xyz', at=0, to=3)
            ],
            msg=""
        )

        # Success (x2)
        self.assertEqual(
            first=list(flow('xyyz')),
            second=[
                Token(type='X*YZ', content='xyyz', at=0, to=4)
            ],
            msg=""
        )

        # Failure (x0)
        self.assertEqual(
            first=list(flow('xt')),
            second=[
                Token(type='~ERROR', content='xt', at=0, to=2)
            ],
            msg=""
        )

        # Failure (x1)
        self.assertEqual(
            first=list(flow('xyt')),
            second=[
                Token(type='~ERROR', content='xyt', at=0, to=3)
            ],
            msg=""
        )

        # Failure (x2)
        self.assertEqual(
            first=list(flow('xyyt')),
            second=[
                Token(type='~ERROR', content='xyyt', at=0, to=4)
            ],
            msg=""
        )

    def test_004(self):
        """Test the `repeat` method"""
        flow = Flow()
        origin = ManagerProxy(flow, 0)

        origin.match('x').repeat_plus('y').build('z', 'X+YZ')

        finalize(flow)

        # Success (x1)
        self.assertEqual(
            first=list(flow('xyz')),
            second=[
                Token(type='X+YZ', content='xyz', at=0, to=3)
            ],
            msg=""
        )

        # Success (x2)
        self.assertEqual(
            first=list(flow('xyyz')),
            second=[
                Token(type='X+YZ', content='xyyz', at=0, to=4)
            ],
            msg=""
        )

        # Failure : missing required item (x0)
        self.assertEqual(
            first=list(flow('xz')),
            second=[
                Token(type='~ERROR', content='xz', at=0, to=2)
            ],
            msg=""
        )

        # Failure (x0)
        self.assertEqual(
            first=list(flow('xt')),
            second=[
                Token(type='~ERROR', content='xt', at=0, to=2)
            ],
            msg=""
        )

        # Failure (x1)
        self.assertEqual(
            first=list(flow('xyt')),
            second=[
                Token(type='~ERROR', content='xyt', at=0, to=3)
            ],
            msg=""
        )

        # Failure (x2)
        self.assertEqual(
            first=list(flow('xyyt')),
            second=[
                Token(type='~ERROR', content='xyyt', at=0, to=4)
            ],
            msg=""
        )


if __name__ == '__main__':
    unittest.main()
