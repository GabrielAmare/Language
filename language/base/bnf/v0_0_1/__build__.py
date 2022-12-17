import string

from language.base.bnf.v0_0_0 import *
from language.base.python import Environment, LintRule
from language.lang_package_builder import LangPackageBuilder

__all__ = [
    'bnf_engine_0_0_1',
]

ABSTRACT_GR = (
    GroupContext(root=None, name='AbstractGR')
    .lemma('Engine', sequence(*[
        enum1(
            literal('\n'),
            match_in('BuildGR', 'rules'),
        ),
        literal('\n'),
        literal('entry'),
        canonical(' '),
        match_as('Variable', 'entry')
    ]))
    .token('Variable', sequence(*[
        match_char(string.ascii_letters + '_'),
        repeat0(match_char(string.ascii_letters + string.digits + '_')),
    ]))
    .token('String', parallel(*[
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
    ]))
    .token('_Inverted', literal('!'))
    .token('_Indented', literal(':i'))
)

BUILD_GR = (
    ABSTRACT_GR.group('BuildGR')
    .lemma('BuildToken', sequence(*[
        literal('token'),
        canonical(' '),
        match_as('Variable', 'type'),
        canonical(' '),
        literal('='),
        canonical(' '),
        # TODO : maybe define an engine to emulate regex lang here instead of using ParallelGR.
        match_as('ParallelGR', 'rule'),
    ]))
    .lemma('BuildLemma', sequence(*[
        literal('lemma'),
        optional(sequence(*[
            match_as('_Indented', 'indented'),
        ])),
        canonical(' '),
        match_as('Variable', 'type'),
        canonical(' '),
        literal('='),
        canonical(' '),
        match_as('ParallelGR', 'rule'),
    ]))
    .lemma('BuildGroup', sequence(*[
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
    ]))
)
PARALLEL_GR = (
    ABSTRACT_GR.group('ParallelGR')
    .lemma('Parallel', sequence(*[
        enum1(
            sequence(
                canonical(' '),
                literal('|'),
                canonical(' '),
            ),
            match_in('SequenceGR', 'rules')
        )
    ]))
)

SEQUENCE_GR = (
    PARALLEL_GR.group('SequenceGR')
    .lemma('Sequence', sequence(*[
        enum1(
            sequence(
                canonical(' '),
            ),
            match_in('RepeatGR', 'rules')
        )
    ]))
)

REPEAT_GR = (
    SEQUENCE_GR.group('RepeatGR')
    .lemma('Repeat0', sequence(*[
        literal('*'),
        match_as('GroupingGR', 'rule'),
    ]))
    .lemma('Repeat1', sequence(*[
        literal('+'),
        match_as('GroupingGR', 'rule'),
    ]))
    .lemma('Optional', sequence(*[
        literal('?'),
        match_as('GroupingGR', 'rule'),
    ]))
    .lemma('Enum0', sequence(*[
        match_as('GroupingGR', 'separator'),
        literal('.'),
        match_as('GroupingGR', 'item'),
    ]))
    .lemma('Enum1', sequence(*[
        match_as('GroupingGR', 'separator'),
        literal('..'),
        match_as('GroupingGR', 'item'),
    ]))
)
GROUPING_GR = (
    REPEAT_GR.group('GroupingGR')
    .lemma('Grouping', sequence(*[
        literal('['),
        match_as('ParallelGR', 'rule'),
        literal(']'),
    ]))
)
MATCH_GR = (
    GROUPING_GR.group('MatchGR')
    .lemma('MatchChar', sequence(*[
        optional(match_as('Inverted', 'inverted')),
        match_as('String', 'charset'),
    ]))
    .lemma('MatchAs', sequence(*[
        literal('<'),
        match_as('Variable', 'type'),
        canonical(' '),
        literal('as'),
        canonical(' '),
        match_as('Variable', 'key'),
        literal('>'),
    ]))
    .lemma('MatchIn', sequence(*[
        literal('<'),
        match_as('Variable', 'type'),
        canonical(' '),
        literal('in'),
        canonical(' '),
        match_as('Variable', 'key'),
        literal('>'),
    ]))
    .lemma('Literal', sequence(*[
        match_as('String', 'expr')
    ]))
    .lemma('Canonical', sequence(*[
        literal('$'),
        match_as('String', 'expr')
    ]))
)

bnf_engine_0_0_1 = ABSTRACT_GR.engine()

if __name__ == '__main__':
    builder = LangPackageBuilder(
        name='core',
        python_env=Environment(
            version=(3, 10, 0),
            builtins=['dataclasses', 'abc', 'typing'],
            style={
                LintRule.MODULE_NO_IMPORT_FROM: False,
                LintRule.DATACLASS_FROZEN: True,
            }
        ),
        build_visitors=['ParallelGR', 'BuildGR']
    )
    
    builder.build(bnf_engine_0_0_1)
