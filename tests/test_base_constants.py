import string
import unittest

from base.constants import SYMBOL_NAMES


class TestConstants(unittest.TestCase):
    def test_symbol_names(self):
        actual_symbols = list(SYMBOL_NAMES.keys())
        symbol_names = list(SYMBOL_NAMES.values())
        actual_symbols_set = set(actual_symbols)
        symbol_names_set = set(symbol_names)
        expected_symbols_set = set(string.punctuation + string.whitespace)

        self.assertEqual(
            first=len(symbol_names),
            second=len(symbol_names_set),
            msg=("symbol names duplicated : " +
                 ", ".join(map(repr, [name for name in sorted(symbol_names_set) if symbol_names.count(name) > 1])))
        )

        self.assertEqual(
            first=actual_symbols_set,
            second=expected_symbols_set,
            msg=("missing symbols : " +
                 ", ".join(map(repr, sorted(expected_symbols_set.difference(actual_symbols_set)))))
        )
