import unittest

from core.langs import python


class TestCorePython(unittest.TestCase):
    def test_integrity(self):
        src = ("x = 1\n"
               "y = 2\n"
               "z = x + y\n"
               "print(x, y, z)\n")

        obj = python.Module.from_text(src)

        self.assertIsInstance(obj, python.Module)


if __name__ == '__main__':
    unittest.main()
