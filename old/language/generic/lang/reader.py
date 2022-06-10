"""Auto generated module.Any manual changes might be overwritten."""
from website.language.bnf.lang.models import *

__all__ = [
    'reader'
]
# PATTERNS

_KEYWORD_KW_TRUE = KeywordPattern(type=Variable(content='KW_TRUE'), expr=String(content="'true'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_FALSE = KeywordPattern(type=Variable(content='KW_FALSE'), expr=String(content="'false'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_NULL = KeywordPattern(type=Variable(content='KW_NULL'), expr=String(content="'null'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_COLON = StringPattern(type=Variable(content='COLON'), expr=String(content="':'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LB = StringPattern(type=Variable(content='LB'), expr=String(content="'['"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COMMA = StringPattern(type=Variable(content='COMMA'), expr=String(content="','"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RB = StringPattern(type=Variable(content='RB'), expr=String(content="']'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LS = StringPattern(type=Variable(content='LS'), expr=String(content="'{'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RS = StringPattern(type=Variable(content='RS'), expr=String(content="'}'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LEFT_PARENTHESIS = StringPattern(type=Variable(content='LEFT_PARENTHESIS'), expr=String(content="'('"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RIGHT_PARENTHESIS = StringPattern(type=Variable(content='RIGHT_PARENTHESIS'), expr=String(content="')'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DOT = StringPattern(type=Variable(content='DOT'), expr=String(content="'.'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_APPEND = KeywordPattern(type=Variable(content='KW_APPEND'), expr=String(content="'append'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_LENGTH = KeywordPattern(type=Variable(content='KW_LENGTH'), expr=String(content="'length'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_ASTERISK = StringPattern(type=Variable(content='ASTERISK'), expr=String(content="'*'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_SLASH = StringPattern(type=Variable(content='SLASH'), expr=String(content="'/'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_PLUS = StringPattern(type=Variable(content='PLUS'), expr=String(content="'+'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DASH = StringPattern(type=Variable(content='DASH'), expr=String(content="'-'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EQ_EQ = StringPattern(type=Variable(content='EQ_EQ'), expr=String(content="'=='"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_IN = KeywordPattern(type=Variable(content='KW_IN'), expr=String(content="'in'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_EXCEPT = KeywordPattern(type=Variable(content='KW_EXCEPT'), expr=String(content="'except'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_NEWLINE = StringPattern(type=Variable(content='NEWLINE'), expr=String(content="'\\n'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EQ = StringPattern(type=Variable(content='EQ'), expr=String(content="'='"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_ELIF = KeywordPattern(type=Variable(content='KW_ELIF'), expr=String(content="'elif'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_ELSE = KeywordPattern(type=Variable(content='KW_ELSE'), expr=String(content="'else'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_IF = KeywordPattern(type=Variable(content='KW_IF'), expr=String(content="'if'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_FOR = KeywordPattern(type=Variable(content='KW_FOR'), expr=String(content="'for'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_FROM = KeywordPattern(type=Variable(content='KW_FROM'), expr=String(content="'from'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_TO = KeywordPattern(type=Variable(content='KW_TO'), expr=String(content="'to'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_BY = KeywordPattern(type=Variable(content='KW_BY'), expr=String(content="'by'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_ENUM = KeywordPattern(type=Variable(content='KW_ENUM'), expr=String(content="'enum'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_WHILE = KeywordPattern(type=Variable(content='KW_WHILE'), expr=String(content="'while'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_TRY = KeywordPattern(type=Variable(content='KW_TRY'), expr=String(content="'try'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_FUN = KeywordPattern(type=Variable(content='KW_FUN'), expr=String(content="'fun'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_VAR = KeywordPattern(type=Variable(content='KW_VAR'), expr=String(content="'var'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_CON = KeywordPattern(type=Variable(content='KW_CON'), expr=String(content="'con'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_SET = KeywordPattern(type=Variable(content='KW_SET'), expr=String(content="'set'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_RETURN = KeywordPattern(type=Variable(content='KW_RETURN'), expr=String(content="'return'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_RAISE = KeywordPattern(type=Variable(content='KW_RAISE'), expr=String(content="'raise'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_EXPORT = KeywordPattern(type=Variable(content='KW_EXPORT'), expr=String(content="'export'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_DOC = KeywordPattern(type=Variable(content='KW_DOC'), expr=String(content="'doc'"), priority=Integer(content='200'), cast=None, ignore_=None)
_REGEX_STRING = RegexPattern(type=Variable(content='String'), expr=String(content='\'\\".*?\\"|\\\'.*?\\\'\''), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_INTEGER = RegexPattern(type=Variable(content='Integer'), expr=String(content="'\\-?\\d+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_VARIABLE = RegexPattern(type=Variable(content='Variable'), expr=String(content="'[a-zA-Z_]\\w*'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_META_VARIABLE = RegexPattern(type=Variable(content='MetaVariable'), expr=String(content="'\\$[a-zA-Z_]\\w*'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_WHITESPACE = RegexPattern(type=Variable(content='WHITESPACE'), expr=String(content="'\\s+'"), priority=None, cast=None, ignore_=Ignore(), flags=None)
_REGEX_COMMENT = RegexPattern(type=Variable(content='COMMENT'), expr=String(content="'#.*'"), priority=None, cast=None, ignore_=Ignore(), flags=None)

# BRANCHES

_BRANCH_TRUE_CONSTANT = Branch(type=Variable(content='TrueConstant'), rule=Match(type=Variable(content='KW_TRUE')), priority=None, line_prefix=None)
_BRANCH_FALSE_CONSTANT = Branch(type=Variable(content='FalseConstant'), rule=Match(type=Variable(content='KW_FALSE')), priority=None, line_prefix=None)
_BRANCH_NULL_CONSTANT = Branch(type=Variable(content='NullConstant'), rule=Match(type=Variable(content='KW_NULL')), priority=None, line_prefix=None)
_BRANCH_VAR_KEY_PAIR = Branch(type=Variable(content='VarKeyPair'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='key')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_STR_KEY_PAIR = Branch(type=Variable(content='StrKeyPair'), rule=Sequence(rules=[MatchAs(type=Variable(content='String'), key=Variable(content='key')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_LIST = Branch(type=Variable(content='List'), rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items'))]))), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_DICT = Branch(type=Variable(content='Dict'), rule=Sequence(rules=[Match(type=Variable(content='LS')), MatchIn(type=Variable(content='KeyPair'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='KeyPair'), key=Variable(content='items'))]))), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_CALL = Branch(type=Variable(content='Call'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='obj')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchIn(type=Variable(content='Expression'), key=Variable(content='args')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='args'))]))), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_APPEND = Branch(type=Variable(content='Append'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='obj')), Match(type=Variable(content='DOT')), Match(type=Variable(content='KW_APPEND')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='item')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_LENGTH = Branch(type=Variable(content='Length'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='obj')), Match(type=Variable(content='DOT')), Match(type=Variable(content='KW_LENGTH')), Match(type=Variable(content='LEFT_PARENTHESIS')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_MUL = Branch(type=Variable(content='Mul'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='ASTERISK')), MatchAs(type=Variable(content='Secondary'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_DIV = Branch(type=Variable(content='Div'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='SLASH')), MatchAs(type=Variable(content='Secondary'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_ADD = Branch(type=Variable(content='Add'), rule=Sequence(rules=[MatchAs(type=Variable(content='Sum'), key=Variable(content='left')), Match(type=Variable(content='PLUS')), MatchAs(type=Variable(content='Term'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_SUB = Branch(type=Variable(content='Sub'), rule=Sequence(rules=[MatchAs(type=Variable(content='Sum'), key=Variable(content='left')), Match(type=Variable(content='DASH')), MatchAs(type=Variable(content='Term'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_EQ = Branch(type=Variable(content='Eq'), rule=Sequence(rules=[MatchAs(type=Variable(content='Sum'), key=Variable(content='left')), Match(type=Variable(content='EQ_EQ')), MatchAs(type=Variable(content='Sum'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_IN = Branch(type=Variable(content='In'), rule=Sequence(rules=[MatchAs(type=Variable(content='Sum'), key=Variable(content='left')), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='Sum'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_EXCEPT = Branch(type=Variable(content='Except'), rule=Sequence(rules=[Match(type=Variable(content='KW_EXCEPT')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type')), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_BLOCK = Branch(type=Variable(content='Block'), rule=RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='NEWLINE')), MatchIn(type=Variable(content='Statement'), key=Variable(content='statements'))]))), priority=None, line_prefix=String(content="'    '"))
_BRANCH_ARGUMENT = Branch(type=Variable(content='Argument'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))]))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))])))]), priority=None, line_prefix=None)
_BRANCH_ELIF = Branch(type=Variable(content='Elif'), rule=Sequence(rules=[Match(type=Variable(content='KW_ELIF')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='test')), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS')), MatchAs(type=Variable(content='Alt'), key=Variable(content='alt'))]), priority=None, line_prefix=None)
_BRANCH_ELSE = Branch(type=Variable(content='Else'), rule=Sequence(rules=[Match(type=Variable(content='KW_ELSE')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_IF = Branch(type=Variable(content='If'), rule=Sequence(rules=[Match(type=Variable(content='KW_IF')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='test')), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS')), MatchAs(type=Variable(content='Alt'), key=Variable(content='alt'))]), priority=None, line_prefix=None)
_BRANCH_FOR = Branch(type=Variable(content='For'), rule=Sequence(rules=[Match(type=Variable(content='KW_FOR')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='index')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_FROM')), MatchAs(type=Variable(content='Integer'), key=Variable(content='start'))]))), Match(type=Variable(content='KW_TO')), MatchAs(type=Variable(content='Integer'), key=Variable(content='end')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_BY')), MatchAs(type=Variable(content='Integer'), key=Variable(content='step'))]))), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_ENUM = Branch(type=Variable(content='Enum'), rule=Sequence(rules=[Match(type=Variable(content='KW_ENUM')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='item')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchAs(type=Variable(content='Variable'), key=Variable(content='index'))]))), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='Expression'), key=Variable(content='iterable')), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_WHILE = Branch(type=Variable(content='While'), rule=Sequence(rules=[Match(type=Variable(content='KW_WHILE')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='test')), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_TRY = Branch(type=Variable(content='Try'), rule=Sequence(rules=[Match(type=Variable(content='KW_TRY')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS')), MatchIn(type=Variable(content='Except'), key=Variable(content='excepts')), RepeatStar(rule=MatchIn(type=Variable(content='Except'), key=Variable(content='excepts')))]), priority=None, line_prefix=None)
_BRANCH_FUNCTION = Branch(type=Variable(content='Function'), rule=Sequence(rules=[Match(type=Variable(content='KW_FUN')), MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchIn(type=Variable(content='Argument'), key=Variable(content='args')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Argument'), key=Variable(content='args'))]))), Match(type=Variable(content='RIGHT_PARENTHESIS')), Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Match(type=Variable(content='NEWLINE')), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_VARIABLE_DEF = Branch(type=Variable(content='VariableDef'), rule=Sequence(rules=[Match(type=Variable(content='KW_VAR')), MatchAs(type=Variable(content='Variable'), key=Variable(content='target')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))]))), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_CONSTANT_DEF = Branch(type=Variable(content='ConstantDef'), rule=Sequence(rules=[Match(type=Variable(content='KW_CON')), MatchAs(type=Variable(content='Variable'), key=Variable(content='target')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))]))), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_ASSIGN = Branch(type=Variable(content='Assign'), rule=Sequence(rules=[Match(type=Variable(content='KW_SET')), MatchIn(type=Variable(content='Primary'), key=Variable(content='targets')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Primary'), key=Variable(content='targets'))]))), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_RETURN = Branch(type=Variable(content='Return'), rule=Sequence(rules=[Match(type=Variable(content='KW_RETURN')), Optional(rule=Grouping(rule=Sequence(rules=[MatchIn(type=Variable(content='Expression'), key=Variable(content='values')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='values'))])))])))]), priority=None, line_prefix=None)
_BRANCH_RAISE = Branch(type=Variable(content='Raise'), rule=Sequence(rules=[Match(type=Variable(content='KW_RAISE')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_EXPORT = Branch(type=Variable(content='Export'), rule=Sequence(rules=[Match(type=Variable(content='KW_EXPORT')), MatchIn(type=Variable(content='Variable'), key=Variable(content='names')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Variable'), key=Variable(content='names'))])))]), priority=None, line_prefix=None)
_BRANCH_DOCSTRING = Branch(type=Variable(content='Docstring'), rule=Sequence(rules=[Match(type=Variable(content='KW_DOC')), MatchAs(type=Variable(content='String'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_MODULE = Branch(type=Variable(content='Module'), rule=Sequence(rules=[MatchIn(type=Variable(content='Statement'), key=Variable(content='statements')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='NEWLINE')), MatchIn(type=Variable(content='Statement'), key=Variable(content='statements'))])))]), priority=None, line_prefix=None)

# GROUPS

_GROUP_CONSTANT = Group(type=Variable('Constant'), types=[
    Variable('Integer'),
    Variable('String'),
    Variable('TrueConstant'),
    Variable('FalseConstant'),
    Variable('NullConstant')
])
_GROUP_ATOM = Group(type=Variable('Atom'), types=[
    Variable('Variable'),
    Variable('Constant')
])
_GROUP_KEY_PAIR = Group(type=Variable('KeyPair'), types=[
    Variable('VarKeyPair'),
    Variable('StrKeyPair')
])
_GROUP_PRIMARY = Group(type=Variable('Primary'), types=[
    Variable('List'),
    Variable('Dict'),
    Variable('Constant')
])
_GROUP_SECONDARY = Group(type=Variable('Secondary'), types=[
    Variable('Append'),
    Variable('Length'),
    Variable('Primary')
])
_GROUP_TERM = Group(type=Variable('Term'), types=[
    Variable('Mul'),
    Variable('Div'),
    Variable('Secondary')
])
_GROUP_SUM = Group(type=Variable('Sum'), types=[
    Variable('Add'),
    Variable('Sub'),
    Variable('Term')
])
_GROUP_COMPARISON = Group(type=Variable('Comparison'), types=[
    Variable('Eq'),
    Variable('In'),
    Variable('Sum')
])
_GROUP_EXPRESSION = Group(type=Variable('Expression'), types=[
    Variable('Comparison')
])
_GROUP_ALT = Group(type=Variable('Alt'), types=[
    Variable('Elif'),
    Variable('Else')
])
_GROUP_CONTROL_STMT = Group(type=Variable('ControlSTMT'), types=[
    Variable('If'),
    Variable('For'),
    Variable('Enum'),
    Variable('While'),
    Variable('Try')
])
_GROUP_UPDATE_STMT = Group(type=Variable('UpdateSTMT'), types=[
    Variable('Function'),
    Variable('VariableDef'),
    Variable('ConstantDef'),
    Variable('Assign'),
    Variable('ControlSTMT')
])
_GROUP_STATEMENT = Group(type=Variable('Statement'), types=[
    Variable('Docstring'),
    Variable('Return'),
    Variable('Raise'),
    Variable('Export'),
    Variable('UpdateSTMT')
])
_GROUP_CODE = Group(type=Variable('Code'), types=[
    Variable('Module'),
    Variable('Statement'),
    Variable('Expression')
])


reader = Reader(
    lexer=Lexer(
        patterns=[
            _KEYWORD_KW_TRUE,
            _KEYWORD_KW_FALSE,
            _KEYWORD_KW_NULL,
            _STRING_COLON,
            _STRING_LB,
            _STRING_COMMA,
            _STRING_RB,
            _STRING_LS,
            _STRING_RS,
            _STRING_LEFT_PARENTHESIS,
            _STRING_RIGHT_PARENTHESIS,
            _STRING_DOT,
            _KEYWORD_KW_APPEND,
            _KEYWORD_KW_LENGTH,
            _STRING_ASTERISK,
            _STRING_SLASH,
            _STRING_PLUS,
            _STRING_DASH,
            _STRING_EQ_EQ,
            _KEYWORD_KW_IN,
            _KEYWORD_KW_EXCEPT,
            _STRING_NEWLINE,
            _STRING_EQ,
            _KEYWORD_KW_ELIF,
            _KEYWORD_KW_ELSE,
            _KEYWORD_KW_IF,
            _KEYWORD_KW_FOR,
            _KEYWORD_KW_FROM,
            _KEYWORD_KW_TO,
            _KEYWORD_KW_BY,
            _KEYWORD_KW_ENUM,
            _KEYWORD_KW_WHILE,
            _KEYWORD_KW_TRY,
            _KEYWORD_KW_FUN,
            _KEYWORD_KW_VAR,
            _KEYWORD_KW_CON,
            _KEYWORD_KW_SET,
            _KEYWORD_KW_RETURN,
            _KEYWORD_KW_RAISE,
            _KEYWORD_KW_EXPORT,
            _KEYWORD_KW_DOC,
            _REGEX_STRING,
            _REGEX_INTEGER,
            _REGEX_VARIABLE,
            _REGEX_META_VARIABLE,
            _REGEX_WHITESPACE,
            _REGEX_COMMENT
        ]
    ),
    parser=Parser(
        branches=[
            _BRANCH_TRUE_CONSTANT,
            _BRANCH_FALSE_CONSTANT,
            _BRANCH_NULL_CONSTANT,
            _GROUP_CONSTANT,
            _GROUP_ATOM,
            _BRANCH_VAR_KEY_PAIR,
            _BRANCH_STR_KEY_PAIR,
            _GROUP_KEY_PAIR,
            _BRANCH_LIST,
            _BRANCH_DICT,
            _BRANCH_CALL,
            _GROUP_PRIMARY,
            _BRANCH_APPEND,
            _BRANCH_LENGTH,
            _GROUP_SECONDARY,
            _BRANCH_MUL,
            _BRANCH_DIV,
            _GROUP_TERM,
            _BRANCH_ADD,
            _BRANCH_SUB,
            _GROUP_SUM,
            _BRANCH_EQ,
            _BRANCH_IN,
            _GROUP_COMPARISON,
            _GROUP_EXPRESSION,
            _BRANCH_EXCEPT,
            _BRANCH_BLOCK,
            _BRANCH_ARGUMENT,
            _BRANCH_ELIF,
            _BRANCH_ELSE,
            _GROUP_ALT,
            _BRANCH_IF,
            _BRANCH_FOR,
            _BRANCH_ENUM,
            _BRANCH_WHILE,
            _BRANCH_TRY,
            _GROUP_CONTROL_STMT,
            _BRANCH_FUNCTION,
            _BRANCH_VARIABLE_DEF,
            _BRANCH_CONSTANT_DEF,
            _BRANCH_ASSIGN,
            _GROUP_UPDATE_STMT,
            _BRANCH_RETURN,
            _BRANCH_RAISE,
            _BRANCH_EXPORT,
            _BRANCH_DOCSTRING,
            _GROUP_STATEMENT,
            _BRANCH_MODULE,
            _GROUP_CODE
        ],
        start=Variable('Module')
    )
)
