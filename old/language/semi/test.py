import unittest

from website.language.semi import *

always_match = Match(ALWAYS)

repeat_star = Repeat(rule=always_match, mn=None, mx=None)
repeat_plus = Repeat(rule=always_match, mn=Integer.from_int(1), mx=None)
optional = Repeat(rule=always_match, mn=None, mx=Integer.from_int(1))


class TestProcessing(unittest.TestCase):
    def test_repeat_minus_one_0(self):
        self.assertEqual(first=repeat_star.repeat_minus_one(), second=repeat_star)

    def test_repeat_minus_one_1(self):
        self.assertEqual(first=repeat_plus.repeat_minus_one(), second=repeat_star)

    def test_repeat_minus_one_2(self):
        self.assertEqual(first=optional.repeat_minus_one(), second=VALID)

    def test_repeat_minus_one_3(self):
        repeat_before = Repeat(rule=always_match, mn=Integer.from_int(4), mx=None)
        repeat_after = Repeat(rule=always_match, mn=Integer.from_int(3), mx=None)
        self.assertEqual(first=repeat_before.repeat_minus_one(), second=repeat_after)

    def test_repeat_minus_one_4(self):
        repeat_before = Repeat(rule=always_match, mn=Integer.from_int(4), mx=Integer.from_int(9))
        repeat_after = Repeat(rule=always_match, mn=Integer.from_int(3), mx=Integer.from_int(8))
        self.assertEqual(first=repeat_before.repeat_minus_one(), second=repeat_after)

    def test_repeat_minus_one_5(self):
        repeat_before = Repeat(rule=always_match, mn=None, mx=Integer.from_int(9))
        repeat_after = Repeat(rule=always_match, mn=None, mx=Integer.from_int(8))
        self.assertEqual(first=repeat_before.repeat_minus_one(), second=repeat_after)


if __name__ == '__main__':
    unittest.main()
