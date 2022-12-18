import string

from language.base.bnf.v0_0_1 import *
from language.lang_package_builder import LangPackageBuilder


def _op2(left_type: str, operator: ParallelGR, right_type: str):
    return sequence(*[
        match_as(left_type, 'left'),
        canonical(' '),
        operator,
        canonical(' '),
        match_as(right_type, 'right'),
    ])


def _op1(operator: str, right_type: str):
    return sequence(*[
        literal(operator),
        match_as(right_type, 'right'),
    ])


ABSTRACT_GR = (
    GroupContext(root=None, name='AbstractGR')
    .lemma('Module', sequence(*[
        enum1(
            separator=literal('\n'),
            item=match_in('Statement', 'statements')
        )
    ]))
    .lemma('Block', repeat1(sequence(*[
        literal('\n'),
        match_in('Statement', 'statements'),
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
        match_as('Expression', 'test'),
        literal(':'),
        match_as('Block', 'block'),
        optional(match_as('AltGR', 'alt')),
    ]))
    .lemma('For', sequence(*[
        literal('for'),
        canonical(' '),
        enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=match_in('Variable', 'args')
        ),
        canonical(' '),
        literal('in'),
        canonical(' '),
        match_as('Expression', 'iter'),
        literal(':'),
        match_as('Block', 'block'),
    ]))
    .lemma('Assign', sequence(*[
        match_as('Primary', 'target'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            match_as('Expression', 'type')
        ])),
        optional(sequence(*[
            canonical(' '),
            literal('='),
            canonical(' '),
            match_as('Expression', 'value'),
        ])),
    ]))
    .lemma('StatementExpression', sequence(*[
        match_as('Expression', 'expr'),
    ]))
)

ALT_GR = (
    ABSTRACT_GR.group('AltGR')
    .lemma('Elif', sequence(*[
        literal('\n'),
        literal('elif'),
        canonical(' '),
        match_as('Expression', 'test'),
        literal(':'),
        match_as('Block', 'block'),
        optional(match_as('AltGR', 'alt')),
    ]))
    .lemma('Else', sequence(*[
        literal('\n'),
        literal('else'),
        literal(':'),
        match_as('Block', 'block'),
    ]))
)

RETURNING_STATEMENT = (
    STATEMENT.group('ReturningStatement')
    .lemma('Raise', sequence(*[
        literal('raise'),
        optional(sequence(*[
            canonical(' '),
            match_as('Expression', 'exc'),
            optional(sequence(*[
                canonical(' '),
                canonical('from'),
                canonical(' '),
                match_as('Expression', 'cause'),
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
                item=match_in('Expression', 'expressions'),
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
                item=match_in('Expression', 'expressions'),
            ),
        ])),
    ]))
    .lemma('YieldFrom', sequence(*[
        literal('yield'),
        canonical(' '),
        literal('from'),
        canonical(' '),
        match_as('Expression', 'expr'),
    ]))
)

PARAM_GR = (
    ABSTRACT_GR.group('ParamGR')
    # Python has a strict order in how params (with or without type or default) are ordered, we ignore this constraint
    # here.
    .lemma('Param', sequence(*[
        match_as('Variable', 'name'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            match_as('Expression', 'type'),
        ])),
        optional(sequence(*[
            canonical(' '),
            literal('='),
            canonical(' '),
            match_as('Expression', 'default'),
        ])),
    ]))
    .lemma('ArgsParam', sequence(*[
        literal('*'),
        match_as('Variable', 'name'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            match_as('Expression', 'type'),
        ])),
    ]))
    .lemma('KwargsParam', sequence(*[
        literal('**'),
        match_as('Variable', 'name'),
        optional(sequence(*[
            literal(':'),
            canonical(' '),
            match_as('Expression', 'type'),
        ])),
    ]))
)

DECORATOR_GR = (
    STATEMENT.group('DecoratorGR')
    .lemma('Decorator', sequence(*[
        literal('@'),
        match_as('Expression', 'expr'),
        literal('\n'),
        match_as('DecoratorGR', 'target'),
    ]))
    .lemma('Class', sequence(*[
        literal('class'),
        canonical(' '),
        match_as('Variable', 'name'),
        optional(sequence(*[
            literal('('),
            enum0(
                separator=sequence(*[literal(','), canonical(' ')]),
                item=match_in('Expression', 'mro')
            ),
            literal(')')
        ])),
        literal(':'),
        match_as('Block', 'block'),
    ]))
    .lemma('Function', sequence(*[
        literal('def'),
        canonical(' '),
        match_as('Variable', 'name'),
        literal('('),
        enum0(
            separator=sequence(*[literal(','), canonical(' ')]),
            item=match_in('ParamGR', 'args')
        ),
        literal(')'),
        optional(sequence(*[
            canonical(' '),
            literal('->'),
            canonical(' '),
            match_as('Expression', 'returns')
        ])),
        literal(':'),
        match_as('Block', 'block'),
    ]))
)

SLICE_GR = (
    ABSTRACT_GR.group('SliceGR')
    .lemma('Slice', sequence(*[
        optional(match_as('Expression', 'first')),
        literal(':'),
        optional(match_as('Expression', 'second')),
        optional(sequence(*[
            literal(':'),
            match_as('Expression', 'third')
        ])),
    ]))
)

EXPRESSION = (
    SLICE_GR.group('Expression')
)

DISJUNCTION = EXPRESSION.group('Disjunction').lemma('Or', sequence(*[
    enum1(
        separator=sequence(canonical(' '), literal('or'), canonical(' ')),
        item=match_in('Conjunction', 'items')
    )
]))
CONJUNCTION = DISJUNCTION.group('Conjunction').lemma('And', sequence(*[
    enum1(
        separator=sequence(canonical(' '), literal('and'), canonical(' ')),
        item=match_in('Inversion', 'items')
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
    match_as('Primary', 'right'),
]))
PRIMARY = (
    AWAITED_PRIMARY.group('Primary')
    .lemma('GetAttr', sequence(*[
        match_as('Primary', 'left'),
        literal('.'),
        match_as('Variable', 'right')
    ]))
    .lemma('GetItem', sequence(*[
        match_as('Primary', 'left'),
        literal('['),
        enum0(
            separator=sequence(*[
                literal(','),
                canonical(' '),
            ]),
            item=match_in('SliceGR', 'items'),
        ),
        literal(']'),
    ]))
    .lemma('Call', sequence(*[
        match_as('Primary', 'left'),
        literal('('),
        enum0(
            separator=sequence(*[
                literal(','),
                canonical(' '),
            ]),
            item=match_in('ArgumentGR', 'args'),
        ),
        literal(')'),
    ]))
)

ABSTRACT_GR.lemma('IndentedListBody', sequence(*[
    repeat1(sequence(*[
        literal('\n'),
        match_in('Expression', 'items'),
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
        match_char(string.ascii_letters + '_'),
        repeat0(match_char(string.ascii_letters + string.digits + '_')),
    ]))
    .token('String', parallel(*[
        sequence(*[
            match_char('"'),
            match_char('"', True),
            match_char('"'),
        ]),
        sequence(*[
            match_char("'"),
            match_char("'", True),
            match_char("'"),
        ]),
    ]))
    .token('Integer', repeat1(match_char('0123456789')))
    .token('Decimal', parallel(*[
        sequence(*[
            repeat1(match_char(string.digits)),
            match_char('.'),
            repeat0(match_char(string.digits)),
        ]),
        sequence(*[
            match_char('.'),
            repeat1(match_char(string.digits)),
        ]),
    ]))
    .lemma('List', sequence(*[
        literal('['),
        optional(enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=match_in('Expression', 'items')
        )),
        literal(']'),
    ]))
    .lemma('Tuple', sequence(*[
        literal('('),
        enum1(
            separator=sequence(literal(','), canonical(' ')),
            item=match_in('Expression', 'items'),
        ),
        # TODO : include the case where the tuple has only a single item `(item,)`.
        literal(')'),
    ]))
    .lemma('IndentedList', sequence(*[
        literal('['),
        match_as('IndentedListBody', 'body'),
        literal('\n'),
        literal(']')
    ]))
)
ARGUMENT_GR = (
    ABSTRACT_GR.group('ArgumentGR')
    .lemma('Kwarg', sequence(*[
        match_as('Variable', 'name'),
        literal('='),
        match_as('Expression', 'value')
    ]))
    .lemma('StarredExpression', sequence(*[
        literal('*'),
        match_as('Expression', 'value')
    ]))
    .lemma('DoubleStarred', sequence(*[
        literal('**'),
        match_as('Expression', 'value')
    ]))
)
ARGUMENT_GR.ref('Expression')  # This make `Expression` inherits from `ArgumentGR` (introducing multiple inheritance).

ABSTRACT_GR.lemma('ImportPath', sequence(*[
    enum0(
        separator=literal('.'),
        item=match_in('Variable', 'parts'),
    ),
]))
IMPORT_STATEMENT = (
    STATEMENT.group('ImportStatement')
    .lemma('Import', sequence(*[
        literal('import'),
        canonical(' '),
        enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=match_in('ImportPath', 'targets'),
        ),
    ]))
    .lemma('ImportFrom', sequence(*[
        literal('from'),
        canonical(' '),
        match_as('ImportPath', 'origin'),
        canonical(' '),
        literal('import'),
        canonical(' '),
        enum0(
            separator=sequence(literal(','), canonical(' ')),
            item=match_in('ImportPath', 'targets'),
        ),
    ]))
)

definition = ABSTRACT_GR.engine()

builder = LangPackageBuilder('v3_10_0')

builder.build(
    definition
)
