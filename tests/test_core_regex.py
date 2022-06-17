import unittest

from core.langs import regex


class TestCoreRegex(unittest.TestCase):
    def test_integrity(self):
        src = r"[a-zA-Z_]\w*\.\d+"
        
        obj = regex.engine(src)
        
        self.assertIsInstance(obj, regex.ParallelGR)
    
    def test_001(self):
        self.assertIsInstance(regex.engine(r"\w"), regex.AnyWord)
    
    def test_002(self):
        self.assertIsInstance(regex.engine(r"\s"), regex.AnyWhitespace)
    
    def test_003(self):
        self.assertIsInstance(regex.engine(r"\d"), regex.AnyDigit)
    
    def test_004(self):
        self.assertIsInstance(regex.engine(r"\W"), regex.AnyNonWord)
    
    def test_005(self):
        self.assertIsInstance(regex.engine(r"\S"), regex.AnyNonWhitespace)
    
    def test_006(self):
        self.assertIsInstance(regex.engine(r"\D"), regex.AnyNonDigit)


if __name__ == '__main__':
    unittest.main()
