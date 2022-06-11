import unittest

from core.langs import regex


class TestCoreRegex(unittest.TestCase):
    def test_integrity(self):
        src = r"[a-zA-Z_]\w*\.\d+"

        obj = regex.engine(src)

        self.assertIsInstance(obj, regex.ParallelGR)


if __name__ == '__main__':
    unittest.main()
