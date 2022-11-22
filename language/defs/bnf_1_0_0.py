import string

from language.base.bnf import *
from language.gen.bnf_to_python import ModelsBuilder, ModelsBuilderConfig, TypeCast

__all__ = [
    'bnf_engine_0_0_1',
]

bnf_engine_0_0_1 = engine(
    tokens={
        'Variable': sequence(*[
            match_char(string.ascii_letters + '_'),
            repeat0(match_char(string.ascii_letters + string.digits + '_')),
        ]),
        'String': parallel(*[
            sequence(
                match_char('"'),
                repeat0(
                    parallel(
                        sequence(match_char('\\'), match_char('"')),
                        sequence(match_char('"', inverted=True)),
                    )
                ),
                match_char('"'),
            ),
            sequence(
                match_char("'"),
                repeat0(
                    parallel(
                        sequence(match_char('\\'), match_char("'")),
                        sequence(match_char("'", inverted=True)),
                    )
                ),
                match_char("'"),
            ),
        ]),
        'Inverted': literal('!'),
    },
    lemmas={
        'MatchChar': sequence(*[
            optional(match_as('Inverted', 'inverted')),
            match_as('String', 'charset'),
        ]),
        'MatchAs': sequence(*[
            literal('<'),
            match_as('Variable', 'type'),
            canonical(' '),
            literal('as'),
            canonical(' '),
            match_as('Variable', 'key'),
            literal('>'),
        ]),
        'MatchIn': sequence(*[
            literal('<'),
            match_as('Variable', 'type'),
            canonical(' '),
            literal('in'),
            canonical(' '),
            match_as('Variable', 'key'),
            literal('>'),
        ]),
        'Literal': sequence(*[
            match_as('String', 'expr')
        ]),
        'Canonical': sequence(*[
            literal('$'),
            match_as('String', 'expr')
        ]),
        'Grouping': sequence(*[
            literal('['),
            match_as('ParallelGR', 'rule'),
            literal(']'),
        ]),
        'Repeat0': sequence(*[
            literal('*'),
            match_as('GroupingGR', 'rule'),
        ]),
        'Repeat1': sequence(*[
            literal('+'),
            match_as('GroupingGR', 'rule'),
        ]),
        'Optional': sequence(*[
            literal('?'),
            match_as('GroupingGR', 'rule'),
        ]),
        'Enum0': sequence(*[
            match_as('GroupingGR', 'separator'),
            literal('.'),
            match_as('GroupingGR', 'item'),
        ]),
        'Enum1': sequence(*[
            match_as('GroupingGR', 'separator'),
            literal('..'),
            match_as('GroupingGR', 'item'),
        ]),
        'Sequence': sequence(*[
            enum1(
                sequence(
                    canonical(' '),
                ),
                match_in('RepeatGR', 'rules')
            )
        ]),
        'Parallel': sequence(*[
            enum1(
                sequence(
                    canonical(' '),
                    literal('|'),
                    canonical(' '),
                ),
                match_in('SequenceGR', 'rules')
            )
        ]),
        'BuildToken': sequence(*[
            literal('token'),
            canonical(' '),
            match_as('Variable', 'type'),
            canonical(' '),
            literal('='),
            canonical(' '),
            # TODO : maybe define an engine to emulate regex lang here instead of using ParallelGR.
            match_as('ParallelGR', 'rule'),
        ]),
        'BuildLemma': sequence(*[
            literal('lemma'),
            canonical(' '),
            match_as('Variable', 'type'),
            canonical(' '),
            literal('='),
            canonical(' '),
            match_as('ParallelGR', 'rule'),
        ]),
        'BuildGroup': sequence(*[
            literal('group'),
            canonical(' '),
            match_as('Variable', 'type'),
            canonical(' '),
            literal('='),
            canonical(' '),
            enum1(
                sequence(
                    canonical(' '),
                    literal('|'),
                    canonical(' ')
                ),
                match_in('Variable', 'refs')
            )
        ]),
        'Engine': sequence(*[
            enum1(
                literal('\n'),
                match_in('BuildGR', 'rules'),
            ),
            literal('\n'),
            literal('entry'),
            canonical(' '),
            match_as('Variable', 'entry')
        ])
    },
    groups={
        'BuildGR': ['BuildToken', 'BuildLemma', 'BuildGroup'],
        'MatchGR': ['MatchChar', 'MatchAs', 'MatchIn', 'Literal', 'Canonical'],
        'GroupingGR': ['Grouping', 'MatchGR'],
        'RepeatGR': ['Enum0', 'Enum1', 'Optional', 'Repeat0', 'Repeat1', 'GroupingGR'],
        'SequenceGR': ['Sequence', 'RepeatGR'],
        'ParallelGR': ['Parallel', 'SequenceGR'],
        'AbstractGR': ['Engine', 'ParallelGR'],
    },
    entry='Engine',
)

if __name__ == '__main__':
    src = str(bnf_engine_0_0_1)
    
    with open("../base/bnf/grammar.bnf", mode="w", encoding="utf-8") as file:
        file.write(src)
    
    builder = ModelsBuilder(
        engine=bnf_engine_0_0_1,
        casts={
            'Variable': TypeCast.VAR,
            'Inverted': TypeCast.BOOL,
            'String': TypeCast.STR,
        },
        config=ModelsBuilderConfig(
            frozen_dataclasses=True,
            multiple_are_tuples=True,
        )
    )
    
    module = builder.module
    
    with open("../base/bnf/models.py", mode="w", encoding="utf-8") as file:
        file.write(str(module))
