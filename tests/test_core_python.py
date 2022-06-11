import unittest
from core.langs import python
import ast


class TestCorePython(unittest.TestCase):
    def test_integrity(self):
        src = ("x = 1\n"
               "y = 2\n"
               "z = x + y\n"
               "print(x, y, z)\n")

        ele = ast.parse(src)

        obj = python.Module.from_ast(ele)

        self.assertIsInstance(obj, python.Module)


if __name__ == '__main__':
    unittest.main()
