import string

from language.base.bnf.v0_0_0 import *

__all__ = [
    'python_3_10_0_definition',
]


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


python_3_10_0_definition = (
    EngineBuilder('Module')
    
    # ATOM
    .group('Atom', ['Variable', '_True', '_False', '_None', 'String', 'Integer', 'Decimal'])
    .token('Variable', sequence(*[
        match_char(string.ascii_letters + '_'),
        repeat0(match_char(string.ascii_letters + string.digits + '_')),
    ]))
    .token('_True', literal('True'))
    .token('_False', literal('False'))
    .token('_None', literal('None'))
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
    
    .lemma('Module', sequence(*[
        enum1(
            separator=literal('\n'),
            item=match_in('Statement', 'statements')
        )
    ]))
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
    
    .group('Expression', ['Disjunction'])
    
    # Expressions
    .group('Disjunction', ['Or', 'Conjunction'])
    .lemma('Or', _op2('Disjunction', literal('or'), 'Conjunction'))
    
    .group('Conjunction', ['And', 'Inversion'])
    .lemma('And', _op2('Conjunction', literal('and'), 'Inversion'))
    
    .group('Inversion', ['Not', 'Comparison'])
    .lemma('Not', _op1('not', 'Inversion'))
    
    .group('Comparison', ['Eq', 'Ne', 'Le', 'Lt', 'Ge', 'Gt', 'In', 'NotIn', 'Is', 'IsNot', 'BitwiseOrGR'])
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
    
    # BITWISE OR
    .group('BitwiseOrGR', ['BitwiseOr', 'BitwiseXorGR'])
    .lemma('BitwiseOr', _op2('BitwiseOrGR', literal('|'), 'BitwiseXorGR'))
    
    # BITWISE XOR
    .group('BitwiseXorGR', ['BitwiseXor', 'BitwiseAndGR'])
    .lemma('BitwiseXor', _op2('BitwiseXorGR', literal('^'), 'BitwiseAndGR'))
    
    # BITWISE AND
    .group('BitwiseAndGR', ['BitwiseAnd', 'ShiftGR'])
    .lemma('BitwiseAnd', _op2('BitwiseAndGR', literal('&'), 'ShiftGR'))
    
    # SHIFT
    .group('ShiftGR', ['LShift', 'RShift', 'Sum'])
    .lemma('LShift', _op2('ShiftGR', literal('<<'), 'Sum'))
    .lemma('RShift', _op2('ShiftGR', literal('>>'), 'Sum'))
    
    # SUM
    .group('Sum', ['Add', 'Sub', 'Term'])
    .lemma('Add', _op2('Sum', literal('+'), 'Term'))
    .lemma('Sub', _op2('Sum', literal('-'), 'Term'))
    
    # TERM
    .group('Term', ['Mul', 'TrueDiv', 'FloorDiv', 'Mod', 'MatMul', 'Factor'])
    .lemma('Mul', _op2('Term', literal('*'), 'Factor'))
    .lemma('TrueDiv', _op2('Term', literal('/'), 'Factor'))
    .lemma('FloorDiv', _op2('Term', literal('//'), 'Factor'))
    .lemma('Mod', _op2('Term', literal('%'), 'Factor'))
    .lemma('MatMul', _op2('Term', literal('@'), 'Factor'))
    
    # FACTOR
    .group('Factor', ['Pos', 'Neg', 'Inv', 'Power'])
    .lemma('Pos', _op1('+', 'Factor'))
    .lemma('Neg', _op1('-', 'Factor'))
    .lemma('Inv', _op1('~', 'Factor'))
    
    # POWER
    .group('Power', ['Pow', 'AwaitPrimary'])
    .lemma('Pow', _op2('AwaitPrimary', literal('**'), 'Factor'))
    
    # AWAITED
    .group('AwaitPrimary', ['Awaited', 'Primary'])
    .lemma('Awaited', sequence(*[
        literal('await'),
        canonical(' '),
        match_as('Primary', 'right'),
    ]))
    
    # PRIMARY
    .group('Primary', ['GetAttr', 'GetItem', 'Call', 'Atom'])
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
    
    .lemma('Slice', sequence(*[
        optional(match_as('Expression', 'first')),
        literal(':'),
        optional(match_as('Expression', 'second')),
        optional(sequence(*[
            literal(':'),
            match_as('Expression', 'third')
        ])),
    ]))
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
    
    .group('AbstractGR', ['Module', 'Statement', 'SliceGR', 'ArgumentGR', 'Block'])
    .group('Statement', ['ReturningStatement', 'DecoratorGR'])
    .group('ReturningStatement', ['Return', 'Raise', 'Yield', 'YieldFrom'])
    .group('SliceGR', ['Slice', 'Expression'])
    .group('ArgumentGR', ['Kwarg', 'StarredExpression', 'DoubleStarred', 'Expression'])
    
    .group('DecoratorGR', ['Decorator', 'Class', 'Function'])
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
            item=match_in('Expression', 'args')
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
    .lemma('Block', repeat1(sequence(*[
        literal('\n'),
        match_in('Statement', 'statements'),
    ])))
    
    .build()
)

if __name__ == '__main__':
    from language.lang_package_builder import LangPackageBuilder
    
    DEBUG = False
    
    (
        LangPackageBuilder(
            # build_visitors=[]
            prefix='__ag__' if DEBUG else '',
            dataclass_frozen=False,
        )
        .build(
            python_3_10_0_definition
        )
    )
