import string

from language.base.bnf import *
from language.base.python import Environment, LintRule
from language.lang_package_builder import *

__all__ = [
    'definition',
]

ABSTRACT_GR = (
    GroupContext(root=None, name='AbstractGR')
    .lemma('Engine', sequence(*[
        enum1(
            literal('\n'),
            store('BuildGR', 'rules'),
        ),
        literal('\n'),
        literal('entry'),
        canonical(' '),
        store('Variable', 'entry')
    ]))
    .token('Variable', sequence(*[
        match(string.ascii_letters + '_'),
        repeat0(match(string.ascii_letters + string.digits + '_')),
    ]))
    .token('String', parallel(*[
        sequence(
            match('"'),
            repeat0(
                parallel(
                    sequence(match('\\'), match('"')),
                    sequence(match('"', inverted=True)),
                )
            ),
            match('"'),
        ),
        sequence(
            match("'"),
            repeat0(
                parallel(
                    sequence(match('\\'), match("'")),
                    sequence(match("'", inverted=True)),
                )
            ),
            match("'"),
        ),
    ]))
)

BUILD_GR = (
    ABSTRACT_GR.group('BuildGR')
    .lemma('BuildToken', sequence(*[
        literal('token'),
        canonical(' '),
        store('Variable', 'type'),
        canonical(' '),
        literal('='),
        canonical(' '),
        # TODO : maybe define an engine to emulate regex lang here instead of using ParallelGR.
        store('ParallelGR', 'rule'),
    ]))
    .lemma('BuildLemma', sequence(*[
        literal('lemma'),
        literal_if(':i', 'indented'),
        canonical(' '),
        store('Variable', 'type'),
        canonical(' '),
        literal('='),
        canonical(' '),
        store('ParallelGR', 'rule'),
    ]))
    .lemma('BuildGroup', sequence(*[
        literal('group'),
        canonical(' '),
        store('Variable', 'type'),
        canonical(' '),
        literal('='),
        canonical(' '),
        enum1(
            sequence(
                canonical(' '),
                literal('|'),
                canonical(' ')
            ),
            store('Variable', 'refs')
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
            store('SequenceGR', 'rules')
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
            store('RepeatGR', 'rules')
        )
    ]))
)

REPEAT_GR = (
    SEQUENCE_GR.group('RepeatGR')
    .lemma('Repeat0', sequence(*[
        literal('*'),
        store('GroupingGR', 'rule'),
    ]))
    .lemma('Repeat1', sequence(*[
        literal('+'),
        store('GroupingGR', 'rule'),
    ]))
    .lemma('Optional', sequence(*[
        literal('?'),
        store('GroupingGR', 'rule'),
    ]))
    .lemma('Enum0', sequence(*[
        store('GroupingGR', 'separator'),
        literal('.'),
        store('GroupingGR', 'item'),
    ]))
    .lemma('Enum1', sequence(*[
        store('GroupingGR', 'separator'),
        literal('..'),
        store('GroupingGR', 'item'),
    ]))
)
GROUPING_GR = (
    REPEAT_GR.group('GroupingGR')
    .lemma('Grouping', sequence(*[
        literal('['),
        store('ParallelGR', 'rule'),
        literal(']'),
    ]))
)

ATOM_GR = (
    GROUPING_GR.group('AtomGR')
    .lemma('Match', sequence(*[
        literal_if('!', 'inverted'),
        store('String', 'charset'),
    ]))
    .lemma('Literal', sequence(*[
        store('String', 'expr')
    ]))
    .lemma('LiteralIf', sequence(*[
        store('String', 'expr'),
        canonical(' '),
        literal('->'),
        canonical(' '),
        store('Variable', 'key'),
    ]))
    .lemma('Canonical', sequence(*[
        literal('$'),
        store('String', 'expr')
    ]))
    .lemma('Store', sequence(*[
        store('Variable', 'type'),
        canonical(' '),
        literal('->'),
        canonical(' '),
        store('Variable', 'key'),
    ]))
)

definition = ABSTRACT_GR.engine()

builder = LangPackageBuilder(
    name='v0_2_0',
    python_env=Environment(
        version=(3, 10, 0),
        builtins=['dataclasses', 'abc', 'typing'],
        style={
            LintRule.MODULE_NO_IMPORT_FROM: False,
            LintRule.DATACLASS_FROZEN: True,
        }
    ),
    casters={
        'Variable': CAST_TO_VAR,
        'String': CAST_TO_STRING,
    },
    build_visitors=['ParallelGR', 'BuildGR', 'AbstractGR']
)

builder.build(definition)
