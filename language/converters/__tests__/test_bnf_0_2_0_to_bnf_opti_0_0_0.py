import logging
import os.path
import pickle
import unittest

from language.base.bnf.v0_2_0 import *
from language.converters.bnf_0_2_0_to_bnf_opti_0_0_0 import convert

TEST_DATA = {
    'match_non_inverted': Match(charset="'0123456789'", inverted=False),
    'match_inverted': Match(charset="'0123456789'", inverted=True),
    'store': Store(type='Integer', key='integer_item'),
    'literal': Literal(expr="'match this'"),
    'literal_if': LiteralIf(expr="'this is true'", key='boolean_attr'),
    'canonical': Canonical(expr="'this should be empty on write'"),
    'grouping': Grouping(rule=Match(charset="'.'")),
    'repeat_0': Repeat0(rule=Match(charset="'.'")),
    'repeat_1': Repeat1(rule=Match(charset="'.'")),
    'enum_0': Enum0(item=Match(charset="'x'"), separator=Match(charset="'.'")),
    'enum_1': Enum1(item=Match(charset="'x'"), separator=Match(charset="'.'")),
    'optional': Optional(rule=Match(charset="'.'")),
    'sequence': Sequence(rules=(Match(charset="'a'"), Match(charset="'b'"))),
    'parallel': Parallel(rules=(Match(charset="'a'"), Match(charset="'b'"))),
    'build_token': BuildToken(type="Integer", rule=Repeat1(rule=Match(charset="'0123456789'"))),
    'build_lemma': BuildLemma(type="Add", rule=Sequence(rules=(
        Store(type="Expr", key="left"),
        Canonical(expr="' '"),
        Literal(expr="'+'"),
        Canonical(expr="' '"),
        Store(type="Term", key="right"),
    ))),
    'build_group': BuildGroup(type="Expr", refs=("Add", "Sub", "Term")),
    'lexicon': Engine(entry='ignored', rules=(
        BuildToken(type="Integer", rule=Repeat1(rule=Match(charset="'0123456789'"))),
        BuildLemma(type="Add", rule=Sequence(rules=(
            Store(type="Expr", key="left"),
            Canonical(expr="' '"),
            Literal(expr="'+'"),
            Canonical(expr="' '"),
            Store(type="Integer", key="right"),
        ))),
        BuildLemma(type="Sub", rule=Sequence(rules=(
            Store(type="Expr", key="left"),
            Canonical(expr="' '"),
            Literal(expr="'-'"),
            Canonical(expr="' '"),
            Store(type="Integer", key="right"),
        ))),
        BuildGroup(type="Expr", refs=("Add", "Sub", "Integer"))
    ))
}


class TestConversion(unittest.TestCase):
    def test_conversion(self):
        for test_id, origin in sorted(list(TEST_DATA.items()), key=lambda row: row[0]):
            with self.subTest(msg=test_id):
                target = convert(origin)
                result = (origin, target)
                
                filepath = os.path.join(
                    os.path.dirname(__file__),
                    'snapshots',
                    'test_bnf_0_2_0_to_bnf_opti_0_0_0',
                    f"{test_id}.pickle"
                )
                
                if os.path.isfile(filepath):
                    with open(filepath, mode="rb") as file:
                        expected = pickle.load(file)
                    
                    self.assertEqual(
                        first=expected,
                        second=result,
                        msg=(
                            f"Failed to regenerate snapshot for test {test_id!r}.\n"
                            f"{50 * '#'}\n"
                            f"{result[1]!s}\n"
                            f"{50 * '#'}\n"
                            f"{expected[1]!s}\n"
                            f"{50 * '#'}\n"
                        )
                    )
                else:
                    # expected = result
                    with open(filepath, mode="wb") as file:
                        pickle.dump(result, file)
                        logging.info(f"The snapshot for {test_id!r} have been generated.")


if __name__ == '__main__':
    unittest.main()
