import string

from language.base.bnf import *
from language.lang_package_builder import LangPackageBuilder


def _op2(left_type: str, operator: ParallelGR, right_type: str):
    return sequence(*[
        store(left_type, 'left'),
        canonical(' '),
        operator,
        canonical(' '),
        store(right_type, 'right'),
    ])


def _op1(operator: str, right_type: str):
    return sequence(*[
        literal(operator),
        store(right_type, 'right'),
    ])


ABSTRACT_GR = (
    GroupContext(root=None, name='AbstractGR')
    .lemma('Module', sequence(*[
        enum1(
            separator=literal('\n'),
            item=store('Statement', 'statements')
        )
    ]))
    .lemma('Block', repeat1(sequence(*[
        literal('\n'),
        store('Statement', 'statements'),
    ])), indented=True)
)

STATEMENT = (
    ABSTRACT_GR.group('Statement')
    .literal('_Pass', 'pass')
    .literal('_Continue', 'continue')
    .literal('_Break', 'break')
    .literal('_EmptyLine', '')
    .lemma('If', sequence(*[
        literal('if'),
        canonical(' '),
        store('Expression', 'test'),
        literal(':'),
        store('Block', 'block'),
        optional(store('AltGR', 'alt')),
    ]))
    .lemma('For', sequence(*[
        literal('for'),
        canonical(' '),
        enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=store('Variable', 'args')
        ),
        canonical(' '),
        literal('in'),
        canonical(' '),
        store('Expression', 'iter'),
        literal(':'),
        store('Block', 'block'),
    ]))
    .lemma('Assign', sequence(*[
        store('Primary', 'target'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            store('Expression', 'type')
        ])),
        optional(sequence(*[
            canonical(' '),
            literal('='),
            canonical(' '),
            store('Expression', 'value'),
        ])),
    ]))
    .lemma('StatementExpression', sequence(*[
        store('Expression', 'expr'),
    ]))
)

ALT_GR = (
    ABSTRACT_GR.group('AltGR')
    .lemma('Elif', sequence(*[
        literal('\n'),
        literal('elif'),
        canonical(' '),
        store('Expression', 'test'),
        literal(':'),
        store('Block', 'block'),
        optional(store('AltGR', 'alt')),
    ]))
    .lemma('Else', sequence(*[
        literal('\n'),
        literal('else'),
        literal(':'),
        store('Block', 'block'),
    ]))
)

RETURNING_STATEMENT = (
    STATEMENT.group('ReturningStatement')
    .lemma('Raise', sequence(*[
        literal('raise'),
        optional(sequence(*[
            canonical(' '),
            store('Expression', 'exc'),
            optional(sequence(*[
                canonical(' '),
                canonical('from'),
                canonical(' '),
                store('Expression', 'cause'),
            ])),
        ])),
    ]))
    .lemma('Return', sequence(*[
        literal('return'),
        optional(sequence(*[
            canonical(' '),
            enum0(
                separator=sequence(*[
                    literal(','),
                    canonical(' '),
                ]),
                item=store('Expression', 'expressions'),
            ),
        ])),
    ]))
    .lemma('Yield', sequence(*[
        literal('yield'),
        optional(sequence(*[
            canonical(' '),
            enum0(
                separator=sequence(*[
                    literal(','),
                    canonical(' '),
                ]),
                item=store('Expression', 'expressions'),
            ),
        ])),
    ]))
    .lemma('YieldFrom', sequence(*[
        literal('yield'),
        canonical(' '),
        literal('from'),
        canonical(' '),
        store('Expression', 'expr'),
    ]))
)

PARAM_GR = (
    ABSTRACT_GR.group('ParamGR')
    # Python has a strict order in how params (with or without type or default) are ordered, we ignore this constraint
    # here.
    .lemma('Param', sequence(*[
        store('Variable', 'name'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            store('Expression', 'type'),
        ])),
        optional(sequence(*[
            canonical(' '),
            literal('='),
            canonical(' '),
            store('Expression', 'default'),
        ])),
    ]))
    .lemma('ArgsParam', sequence(*[
        literal('*'),
        store('Variable', 'name'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            store('Expression', 'type'),
        ])),
    ]))
    .lemma('KwargsParam', sequence(*[
        literal('**'),
        store('Variable', 'name'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            store('Expression', 'type'),
        ])),
    ]))
)

DECORATOR_GR = (
    STATEMENT.group('DecoratorGR')
    .lemma('Decorator', sequence(*[
        literal('@'),
        store('Expression', 'expr'),
        literal('\n'),
        store('DecoratorGR', 'target'),
    ]))
    .lemma('Class', sequence(*[
        literal('class'),
        canonical(' '),
        store('Variable', 'name'),
        optional(sequence(*[
            literal('('),
            enum0(
                separator=sequence(*[literal(','), canonical(' ')]),
                item=store('Expression', 'mro')
            ),
            literal(')')
        ])),
        literal(':'),
        store('Block', 'block'),
    ]))
    .lemma('Function', sequence(*[
        literal('def'),
        canonical(' '),
        store('Variable', 'name'),
        literal('('),
        enum0(
            separator=sequence(*[literal(','), canonical(' ')]),
            item=store('ParamGR', 'args')
        ),
        literal(')'),
        optional(sequence(*[
            canonical(' '),
            literal('->'),
            canonical(' '),
            store('Expression', 'returns')
        ])),
        literal(':'),
        store('Block', 'block'),
    ]))
)

SLICE_GR = (
    ABSTRACT_GR.group('SliceGR')
    .lemma('Slice', sequence(*[
        optional(store('Expression', 'first')),
        literal(':'),
        optional(store('Expression', 'second')),
        optional(sequence(*[
            literal(':'),
            store('Expression', 'third')
        ])),
    ]))
)

EXPRESSION = (
    SLICE_GR.group('Expression')
)

DISJUNCTION = EXPRESSION.group('Disjunction').lemma('Or', sequence(*[
    enum1(
        separator=sequence(canonical(' '), literal('or'), canonical(' ')),
        item=store('Conjunction', 'items')
    )
]))
CONJUNCTION = DISJUNCTION.group('Conjunction').lemma('And', sequence(*[
    enum1(
        separator=sequence(canonical(' '), literal('and'), canonical(' ')),
        item=store('Inversion', 'items')
    )
]))
INVERSION = CONJUNCTION.group('Inversion').lemma('Not', _op1('not', 'Inversion'))
COMPARISON = (
    INVERSION.group('Comparison')
    .lemma('Eq', _op2('Comparison', literal('=='), 'BitwiseOrGR'))
    .lemma('Ne', _op2('Comparison', literal('!='), 'BitwiseOrGR'))
    .lemma('Le', _op2('Comparison', literal('<='), 'BitwiseOrGR'))
    .lemma('Lt', _op2('Comparison', literal('<'), 'BitwiseOrGR'))
    .lemma('Ge', _op2('Comparison', literal('>='), 'BitwiseOrGR'))
    .lemma('Gt', _op2('Comparison', literal('>'), 'BitwiseOrGR'))
    .lemma('In', _op2('Comparison', literal('in'), 'BitwiseOrGR'))
    .lemma('NotIn', _op2('Comparison', sequence(literal('not'), canonical(' '), literal('in')), 'BitwiseOrGR'))
    .lemma('Is', _op2('Comparison', literal('is'), 'BitwiseOrGR'))
    .lemma('IsNot', _op2('Comparison', sequence(literal('is'), canonical(' '), literal('not')), 'BitwiseOrGR'))
)
BW_OR_GR = COMPARISON.group('BitwiseOrGR').lemma('BitwiseOr', _op2('BitwiseOrGR', literal('|'), 'BitwiseXorGR'))
BW_XOR_GR = BW_OR_GR.group('BitwiseXorGR').lemma('BitwiseXor', _op2('BitwiseXorGR', literal('^'), 'BitwiseAndGR'))
BW_AND_GR = BW_XOR_GR.group('BitwiseAndGR').lemma('BitwiseAnd', _op2('BitwiseAndGR', literal('&'), 'ShiftGR'))
SHIFT_GR = (
    BW_AND_GR.group('ShiftGR')
    .lemma('LShift', _op2('ShiftGR', literal('<<'), 'Sum'))
    .lemma('RShift', _op2('ShiftGR', literal('>>'), 'Sum'))
)
SUM = (
    SHIFT_GR.group('Sum')
    .lemma('Add', _op2('Sum', literal('+'), 'Term'))
    .lemma('Sub', _op2('Sum', literal('-'), 'Term'))
)
TERM = (
    SUM.group('Term')
    .lemma('Mul', _op2('Term', literal('*'), 'Factor'))
    .lemma('TrueDiv', _op2('Term', literal('/'), 'Factor'))
    .lemma('FloorDiv', _op2('Term', literal('//'), 'Factor'))
    .lemma('Mod', _op2('Term', literal('%'), 'Factor'))
    .lemma('MatMul', _op2('Term', literal('@'), 'Factor'))
)
FACTOR = (
    TERM.group('Factor')
    .lemma('Pos', _op1('+', 'Factor'))
    .lemma('Neg', _op1('-', 'Factor'))
    .lemma('Inv', _op1('~', 'Factor'))
)
POWER = FACTOR.group('Power').lemma('Pow', _op2('AwaitPrimary', literal('**'), 'Factor'))
AWAITED_PRIMARY = POWER.group('AwaitPrimary').lemma('Awaited', sequence(*[
    literal('await'),
    canonical(' '),
    store('Primary', 'right'),
]))
PRIMARY = (
    AWAITED_PRIMARY.group('Primary')
    .lemma('GetAttr', sequence(*[
        store('Primary', 'left'),
        literal('.'),
        store('Variable', 'right')
    ]))
    .lemma('GetItem', sequence(*[
        store('Primary', 'left'),
        literal('['),
        enum0(
            separator=sequence(*[
                literal(','),
                canonical(' '),
            ]),
            item=store('SliceGR', 'items'),
        ),
        literal(']'),
    ]))
    .lemma('Call', sequence(*[
        store('Primary', 'left'),
        literal('('),
        enum0(
            separator=sequence(*[
                literal(','),
                canonical(' '),
            ]),
            item=store('ArgumentGR', 'args'),
        ),
        literal(')'),
    ]))
)

ABSTRACT_GR.lemma('IndentedListBody', sequence(*[
    repeat1(sequence(*[
        literal('\n'),
        store('Expression', 'items'),
        literal(','),
    ])),
]), indented=True)

ATOM = (
    PRIMARY.group('Atom')
    .literal('_True', 'True')
    .literal('_False', 'False')
    .literal('_None', 'None')
    .literal('_Ellipsis', '...')
    .token('Variable', sequence(*[
        match(string.ascii_letters + '_'),
        repeat0(match(string.ascii_letters + string.digits + '_')),
    ]))
    .token('String', parallel(*[
        sequence(*[
            match('"'),
            match('"', True),
            match('"'),
        ]),
        sequence(*[
            match("'"),
            match("'", True),
            match("'"),
        ]),
    ]))
    .token('Integer', repeat1(match('0123456789')))
    .token('Decimal', parallel(*[
        sequence(*[
            repeat1(match(string.digits)),
            match('.'),
            repeat0(match(string.digits)),
        ]),
        sequence(*[
            match('.'),
            repeat1(match(string.digits)),
        ]),
    ]))
    .lemma('List', sequence(*[
        literal('['),
        optional(enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=store('Expression', 'items')
        )),
        literal(']'),
    ]))
    .lemma('Tuple', sequence(*[
        literal('('),
        enum1(
            separator=sequence(literal(','), canonical(' ')),
            item=store('Expression', 'items'),
        ),
        # TODO : include the case where the tuple has only a single item `(item,)`.
        literal(')'),
    ]))
    .lemma('IndentedList', sequence(*[
        literal('['),
        store('IndentedListBody', 'body'),
        literal('\n'),
        literal(']')
    ]))
)
ARGUMENT_GR = (
    ABSTRACT_GR.group('ArgumentGR')
    .lemma('Kwarg', sequence(*[
        store('Variable', 'name'),
        literal('='),
        store('Expression', 'value')
    ]))
    .lemma('StarredExpression', sequence(*[
        literal('*'),
        store('Expression', 'value')
    ]))
    .lemma('DoubleStarred', sequence(*[
        literal('**'),
        store('Expression', 'value')
    ]))
)
ARGUMENT_GR.ref('Expression')  # This make `Expression` inherits from `ArgumentGR` (introducing multiple inheritance).

ABSTRACT_GR.lemma('ImportPath', sequence(*[
    enum0(
        separator=literal('.'),
        item=store('Variable', 'parts'),
    ),
]))
IMPORT_STATEMENT = (
    STATEMENT.group('ImportStatement')
    .lemma('Import', sequence(*[
        literal('import'),
        canonical(' '),
        enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=store('ImportPath', 'targets'),
        ),
    ]))
    .lemma('ImportFrom', sequence(*[
        literal('from'),
        canonical(' '),
        store('ImportPath', 'origin'),
        canonical(' '),
        literal('import'),
        canonical(' '),
        enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=store('ImportPath', 'targets'),
        ),
    ]))
)

definition = ABSTRACT_GR.engine()

builder = LangPackageBuilder('v3_10_0')

builder.build(
    definition
)
