import unittest
from core.langs import bnf


class TestCoreBNF(unittest.TestCase):
    def test_integrity(self):
        src = ("string Hello 'hello'\n"
               "\n"
               "branch Greetings := <Hello>\n"
               "\n"
               "> Greetings")

        obj = bnf.engine(src)

        self.assertIsInstance(obj, bnf.Reader)


if __name__ == '__main__':
    unittest.main()
