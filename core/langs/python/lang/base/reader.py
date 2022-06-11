"""Auto generated module.Any manual changes might be overwritten."""
from core.langs.bnf.lang import *

__all__ = [
    'reader'
]
# PATTERNS

_STRING_DOLLAR = StringPattern(type=Variable(content='DOLLAR'), expr=String(content="'$'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_AS = KeywordPattern(type=Variable(content='KW_AS'), expr=String(content="'as'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_COMMA = StringPattern(type=Variable(content='COMMA'), expr=String(content="','"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_ASTERISK = StringPattern(type=Variable(content='ASTERISK'), expr=String(content="'*'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DOT = StringPattern(type=Variable(content='DOT'), expr=String(content="'.'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_FROM = KeywordPattern(type=Variable(content='KW_FROM'), expr=String(content="'from'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_IMPORT = KeywordPattern(type=Variable(content='KW_IMPORT'), expr=String(content="'import'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_DOT_DOT_DOT = StringPattern(type=Variable(content='DOT_DOT_DOT'), expr=String(content="'...'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_COLON = StringPattern(type=Variable(content='COLON'), expr=String(content="':'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EQ = StringPattern(type=Variable(content='EQ'), expr=String(content="'='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_ASTERISK_ASTERISK = StringPattern(type=Variable(content='ASTERISK_ASTERISK'), expr=String(content="'**'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_AT = StringPattern(type=Variable(content='AT'), expr=String(content="'@'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_DEF = KeywordPattern(type=Variable(content='KW_DEF'), expr=String(content="'def'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LEFT_PARENTHESIS = StringPattern(type=Variable(content='LEFT_PARENTHESIS'), expr=String(content="'('"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RIGHT_PARENTHESIS = StringPattern(type=Variable(content='RIGHT_PARENTHESIS'), expr=String(content="')'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DASH_RV = StringPattern(type=Variable(content='DASH_RV'), expr=String(content="'->'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_CLASS = KeywordPattern(type=Variable(content='KW_CLASS'), expr=String(content="'class'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_NONE = KeywordPattern(type=Variable(content='KW_NONE'), expr=String(content="'None'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_TRUE = KeywordPattern(type=Variable(content='KW_TRUE'), expr=String(content="'True'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_FALSE = KeywordPattern(type=Variable(content='KW_FALSE'), expr=String(content="'False'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_FOR = KeywordPattern(type=Variable(content='KW_FOR'), expr=String(content="'for'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_IN = KeywordPattern(type=Variable(content='KW_IN'), expr=String(content="'in'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_IF = KeywordPattern(type=Variable(content='KW_IF'), expr=String(content="'if'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_LB = StringPattern(type=Variable(content='LB'), expr=String(content="'['"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RB = StringPattern(type=Variable(content='RB'), expr=String(content="']'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LS = StringPattern(type=Variable(content='LS'), expr=String(content="'{'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RS = StringPattern(type=Variable(content='RS'), expr=String(content="'}'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_OR = KeywordPattern(type=Variable(content='KW_OR'), expr=String(content="'or'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_AND = KeywordPattern(type=Variable(content='KW_AND'), expr=String(content="'and'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_NOT = KeywordPattern(type=Variable(content='KW_NOT'), expr=String(content="'not'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_IS = KeywordPattern(type=Variable(content='KW_IS'), expr=String(content="'is'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_EQ_EQ = StringPattern(type=Variable(content='EQ_EQ'), expr=String(content="'=='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_EXC_EQ = StringPattern(type=Variable(content='EXC_EQ'), expr=String(content="'!='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LV_EQ = StringPattern(type=Variable(content='LV_EQ'), expr=String(content="'<='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LV = StringPattern(type=Variable(content='LV'), expr=String(content="'<'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RV_EQ = StringPattern(type=Variable(content='RV_EQ'), expr=String(content="'>='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RV = StringPattern(type=Variable(content='RV'), expr=String(content="'>'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_VBAR = StringPattern(type=Variable(content='VBAR'), expr=String(content="'|'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_HAT = StringPattern(type=Variable(content='HAT'), expr=String(content="'^'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_AMPERSAND = StringPattern(type=Variable(content='AMPERSAND'), expr=String(content="'&'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_LV_LV = StringPattern(type=Variable(content='LV_LV'), expr=String(content="'<<'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_RV_RV = StringPattern(type=Variable(content='RV_RV'), expr=String(content="'>>'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_PLUS = StringPattern(type=Variable(content='PLUS'), expr=String(content="'+'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DASH = StringPattern(type=Variable(content='DASH'), expr=String(content="'-'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_SLASH = StringPattern(type=Variable(content='SLASH'), expr=String(content="'/'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_SLASH_SLASH = StringPattern(type=Variable(content='SLASH_SLASH'), expr=String(content="'//'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_PERCENT = StringPattern(type=Variable(content='PERCENT'), expr=String(content="'%'"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_WAVE = StringPattern(type=Variable(content='WAVE'), expr=String(content="'~'"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_ELSE = KeywordPattern(type=Variable(content='KW_ELSE'), expr=String(content="'else'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_ELIF = KeywordPattern(type=Variable(content='KW_ELIF'), expr=String(content="'elif'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_TRY = KeywordPattern(type=Variable(content='KW_TRY'), expr=String(content="'try'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_WHILE = KeywordPattern(type=Variable(content='KW_WHILE'), expr=String(content="'while'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_WITH = KeywordPattern(type=Variable(content='KW_WITH'), expr=String(content="'with'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_YIELD = KeywordPattern(type=Variable(content='KW_YIELD'), expr=String(content="'yield'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_RETURN = KeywordPattern(type=Variable(content='KW_RETURN'), expr=String(content="'return'"), priority=Integer(content='200'), cast=None, ignore_=None)
_STRING_PLUS_EQ = StringPattern(type=Variable(content='PLUS_EQ'), expr=String(content="'+='"), priority=Integer(content='100'), cast=None, ignore_=None)
_STRING_DASH_EQ = StringPattern(type=Variable(content='DASH_EQ'), expr=String(content="'-='"), priority=Integer(content='100'), cast=None, ignore_=None)
_KEYWORD_KW_BREAK = KeywordPattern(type=Variable(content='KW_BREAK'), expr=String(content="'break'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_CONTINUE = KeywordPattern(type=Variable(content='KW_CONTINUE'), expr=String(content="'continue'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_RAISE = KeywordPattern(type=Variable(content='KW_RAISE'), expr=String(content="'raise'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_PASS = KeywordPattern(type=Variable(content='KW_PASS'), expr=String(content="'pass'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_ASSERT = KeywordPattern(type=Variable(content='KW_ASSERT'), expr=String(content="'assert'"), priority=Integer(content='200'), cast=None, ignore_=None)
_KEYWORD_KW_EXCEPT = KeywordPattern(type=Variable(content='KW_EXCEPT'), expr=String(content="'except'"), priority=Integer(content='200'), cast=None, ignore_=None)
_REGEX_VARIABLE = RegexPattern(type=Variable(content='Variable'), expr=String(content="'[a-zA-Z]\\w*'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_INTEGER = RegexPattern(type=Variable(content='Integer'), expr=String(content="'\\d+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_FLOAT = RegexPattern(type=Variable(content='Float'), expr=String(content="'\\d+\\.\\d*|\\.\\d+'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_COMMENT = RegexPattern(type=Variable(content='Comment'), expr=String(content="'#.*'"), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_MULTI_LINE_STRING = RegexPattern(type=Variable(content='MultiLineString'), expr=String(content='\'\\"\\"\\".*?\\"\\"\\"\''), priority=None, cast=None, ignore_=None, flags=Integer(content='16'))
_REGEX_STRING = RegexPattern(type=Variable(content='String'), expr=String(content='\'\\"(?:\\"|[^\\"])*?(?<!\\\\\\\\)\\"|\\\'(?:\\\'|[^\\\'])*?(?<!\\\\\\\\)\\\'\''), priority=None, cast=None, ignore_=None, flags=None)
_REGEX_WHITESPACE = RegexPattern(type=Variable(content='WHITESPACE'), expr=String(content="'[ \\t\\n\\r]+'"), priority=None, cast=None, ignore_=Ignore(), flags=None)

# BRANCHES

_BRANCH_LAMBDA_DEF = Branch(type=Variable(content='LambdaDef'), rule=Match(type=Variable(content='DOLLAR')), priority=None, line_prefix=None)
_BRANCH_ALIAS = Branch(type=Variable(content='Alias'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_AS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='as_name'))])))]), priority=None, line_prefix=None)
_BRANCH_IMPORT_ALIASES = Branch(type=Variable(content='ImportAliases'), rule=Sequence(rules=[MatchIn(type=Variable(content='Alias'), key=Variable(content='names')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Alias'), key=Variable(content='names'))])))]), priority=None, line_prefix=None)
_BRANCH_IMPORT_ALL = Branch(type=Variable(content='ImportAll'), rule=Match(type=Variable(content='ASTERISK')), priority=None, line_prefix=None)
_BRANCH_DOTTED_AS_NAME = Branch(type=Variable(content='DottedAsName'), rule=Sequence(rules=[MatchIn(type=Variable(content='Variable'), key=Variable(content='names')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='DOT')), MatchIn(type=Variable(content='Variable'), key=Variable(content='names'))]))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_AS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='as_name'))])))]), priority=None, line_prefix=None)
_BRANCH_IMPORT_FROM = Branch(type=Variable(content='ImportFrom'), rule=Sequence(rules=[Match(type=Variable(content='KW_FROM')), MatchAs(type=Variable(content='ImportPath'), key=Variable(content='path')), Match(type=Variable(content='KW_IMPORT')), MatchAs(type=Variable(content='ImportFromTargets'), key=Variable(content='targets'))]), priority=None, line_prefix=None)
_BRANCH_IMPORT = Branch(type=Variable(content='Import'), rule=Sequence(rules=[Match(type=Variable(content='KW_IMPORT')), MatchIn(type=Variable(content='DottedAsName'), key=Variable(content='targets')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='DottedAsName'), key=Variable(content='targets'))])))]), priority=None, line_prefix=None)
_BRANCH_IMPORT_DOT = Branch(type=Variable(content='ImportDot'), rule=Match(type=Variable(content='DOT')), priority=None, line_prefix=None)
_BRANCH_IMPORT_ELLIPSIS = Branch(type=Variable(content='ImportEllipsis'), rule=Match(type=Variable(content='DOT_DOT_DOT')), priority=None, line_prefix=None)
_BRANCH_ABSOLUTE_IMPORT_PATH = Branch(type=Variable(content='AbsoluteImportPath'), rule=Sequence(rules=[MatchIn(type=Variable(content='Variable'), key=Variable(content='variables')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='DOT')), MatchIn(type=Variable(content='Variable'), key=Variable(content='variables'))])))]), priority=None, line_prefix=None)
_BRANCH_RELATIVE_IMPORT_PATH = Branch(type=Variable(content='RelativeImportPath'), rule=Sequence(rules=[MatchIn(type=Variable(content='ImportRelative'), key=Variable(content='relatives')), RepeatStar(rule=MatchIn(type=Variable(content='ImportRelative'), key=Variable(content='relatives'))), MatchIn(type=Variable(content='Variable'), key=Variable(content='variables')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='DOT')), MatchIn(type=Variable(content='Variable'), key=Variable(content='variables'))])))]), priority=None, line_prefix=None)
_BRANCH_BLOCK = Branch(type=Variable(content='Block'), rule=RepeatStar(rule=MatchIn(type=Variable(content='Statement'), key=Variable(content='statements'))), priority=None, line_prefix=String(content="'    '"))
_BRANCH_ARGS = Branch(type=Variable(content='Args'), rule=Sequence(rules=[MatchIn(type=Variable(content='Variable'), key=Variable(content='variables')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Variable'), key=Variable(content='variables'))])))]), priority=None, line_prefix=None)
_BRANCH_ARGUMENT = Branch(type=Variable(content='Argument'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))]))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='default'))])))]), priority=None, line_prefix=None)
_BRANCH_NON_KEYWORD_ARGUMENT = Branch(type=Variable(content='NonKeywordArgument'), rule=Sequence(rules=[Match(type=Variable(content='ASTERISK')), MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))])))]), priority=None, line_prefix=None)
_BRANCH_KEYWORD_ARGUMENT = Branch(type=Variable(content='KeywordArgument'), rule=Sequence(rules=[Match(type=Variable(content='ASTERISK_ASTERISK')), MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))])))]), priority=None, line_prefix=None)
_BRANCH_DECORATOR = Branch(type=Variable(content='Decorator'), rule=Sequence(rules=[Match(type=Variable(content='AT')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_DEF = Branch(type=Variable(content='Def'), rule=Sequence(rules=[RepeatStar(rule=MatchIn(type=Variable(content='Decorator'), key=Variable(content='decorators'))), Match(type=Variable(content='KW_DEF')), MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Match(type=Variable(content='LEFT_PARENTHESIS')), Optional(rule=Grouping(rule=Sequence(rules=[MatchIn(type=Variable(content='DefArgumentGR'), key=Variable(content='args')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='DefArgumentGR'), key=Variable(content='args'))])))]))), Match(type=Variable(content='RIGHT_PARENTHESIS')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='DASH_RV')), MatchAs(type=Variable(content='Expression'), key=Variable(content='rtype'))]))), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block'))]), priority=None, line_prefix=None)
_BRANCH_CLASS = Branch(type=Variable(content='Class'), rule=Sequence(rules=[RepeatStar(rule=MatchIn(type=Variable(content='Decorator'), key=Variable(content='decorators'))), Match(type=Variable(content='KW_CLASS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Args'), key=Variable(content='mro')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]))), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block'))]), priority=None, line_prefix=None)
_BRANCH_DICT_ITEM = Branch(type=Variable(content='DictItem'), rule=Sequence(rules=[MatchAs(type=Variable(content='Expression'), key=Variable(content='key')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_NONE_CLASS = Branch(type=Variable(content='NoneClass'), rule=Match(type=Variable(content='KW_NONE')), priority=None, line_prefix=None)
_BRANCH_TRUE_CLASS = Branch(type=Variable(content='TrueClass'), rule=Match(type=Variable(content='KW_TRUE')), priority=None, line_prefix=None)
_BRANCH_FALSE_CLASS = Branch(type=Variable(content='FalseClass'), rule=Match(type=Variable(content='KW_FALSE')), priority=None, line_prefix=None)
_BRANCH_ELLIPSIS_CLASS = Branch(type=Variable(content='EllipsisClass'), rule=Match(type=Variable(content='DOT_DOT_DOT')), priority=None, line_prefix=None)
_BRANCH_STAR_TARGETS = Branch(type=Variable(content='StarTargets'), rule=Sequence(rules=[MatchIn(type=Variable(content='AtomGR'), key=Variable(content='elts')), Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='AtomGR'), key=Variable(content='elts')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='AtomGR'), key=Variable(content='elts'))])))]), priority=None, line_prefix=None)
_BRANCH_FOR_IF_CLAUSE = Branch(type=Variable(content='ForIfClause'), rule=Sequence(rules=[Match(type=Variable(content='KW_FOR')), MatchAs(type=Variable(content='StarTargetsGR'), key=Variable(content='target')), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='Disjunction'), key=Variable(content='iter')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_IF')), MatchIn(type=Variable(content='Disjunction'), key=Variable(content='ifs'))])))]), priority=None, line_prefix=None)
_BRANCH_TUPLE = Branch(type=Variable(content='Tuple'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items'))]))), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_GEN_EXP = Branch(type=Variable(content='GenExp'), rule=Sequence(rules=[Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='elt')), MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators')), RepeatStar(rule=MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators'))), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_INDENTED_LIST = Branch(type=Variable(content='IndentedList'), rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='IndentedExprEnum'), key=Variable(content='body')), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_LIST = Branch(type=Variable(content='List'), rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items'))]))), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_LIST_COMP = Branch(type=Variable(content='ListComp'), rule=Sequence(rules=[Match(type=Variable(content='LB')), MatchAs(type=Variable(content='Expression'), key=Variable(content='elt')), MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators')), RepeatStar(rule=MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators'))), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_DICT = Branch(type=Variable(content='Dict'), rule=Sequence(rules=[Match(type=Variable(content='LS')), MatchIn(type=Variable(content='DictItem'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='DictItem'), key=Variable(content='items'))]))), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_DICT_COMP = Branch(type=Variable(content='DictComp'), rule=Sequence(rules=[Match(type=Variable(content='LS')), MatchAs(type=Variable(content='DictItem'), key=Variable(content='elt')), MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators')), RepeatStar(rule=MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators'))), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_SET = Branch(type=Variable(content='Set'), rule=Sequence(rules=[Match(type=Variable(content='LS')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items'))]))), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_SET_COMP = Branch(type=Variable(content='SetComp'), rule=Sequence(rules=[Match(type=Variable(content='LS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='elt')), MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators')), RepeatStar(rule=MatchIn(type=Variable(content='ForIfClause'), key=Variable(content='generators'))), Match(type=Variable(content='RS'))]), priority=None, line_prefix=None)
_BRANCH_INDENTED_EXPR_ENUM = Branch(type=Variable(content='IndentedExprEnum'), rule=Sequence(rules=[MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items'))])))]), priority=None, line_prefix=String(content="'    '"))
_BRANCH_SLICE = Branch(type=Variable(content='Slice'), rule=Sequence(rules=[Optional(rule=MatchAs(type=Variable(content='Expression'), key=Variable(content='lower'))), Match(type=Variable(content='COLON')), Optional(rule=MatchAs(type=Variable(content='Expression'), key=Variable(content='upper'))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='step'))])))]), priority=None, line_prefix=None)
_BRANCH_SUBSCRIPT = Branch(type=Variable(content='Subscript'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='left')), Match(type=Variable(content='LB')), MatchAs(type=Variable(content='SliceGR'), key=Variable(content='right')), Match(type=Variable(content='RB'))]), priority=None, line_prefix=None)
_BRANCH_GET_ATTR = Branch(type=Variable(content='GetAttr'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='left')), Match(type=Variable(content='DOT')), MatchAs(type=Variable(content='Variable'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_CALL = Branch(type=Variable(content='Call'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='left')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchIn(type=Variable(content='CallArgumentGR'), key=Variable(content='args')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='CallArgumentGR'), key=Variable(content='args'))]))), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_INDENTED_CALL_BODY = Branch(type=Variable(content='IndentedCallBody'), rule=Sequence(rules=[MatchIn(type=Variable(content='CallArgumentGR'), key=Variable(content='args')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='CallArgumentGR'), key=Variable(content='args'))])))]), priority=None, line_prefix=String(content="'    '"))
_BRANCH_INDENTED_CALL = Branch(type=Variable(content='IndentedCall'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='left')), Match(type=Variable(content='LEFT_PARENTHESIS')), MatchAs(type=Variable(content='IndentedCallBody'), key=Variable(content='body')), Match(type=Variable(content='RIGHT_PARENTHESIS'))]), priority=None, line_prefix=None)
_BRANCH_OR = Branch(type=Variable(content='Or'), rule=Sequence(rules=[MatchAs(type=Variable(content='Disjunction'), key=Variable(content='left')), Match(type=Variable(content='KW_OR')), MatchAs(type=Variable(content='Conjunction'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_AND = Branch(type=Variable(content='And'), rule=Sequence(rules=[MatchAs(type=Variable(content='Conjunction'), key=Variable(content='left')), Match(type=Variable(content='KW_AND')), MatchAs(type=Variable(content='Inversion'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_NOT = Branch(type=Variable(content='Not'), rule=Sequence(rules=[Match(type=Variable(content='KW_NOT')), MatchAs(type=Variable(content='Inversion'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_IN = Branch(type=Variable(content='In'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_IS = Branch(type=Variable(content='Is'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='KW_IS')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_NOT_IN = Branch(type=Variable(content='NotIn'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='KW_NOT')), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_IS_NOT = Branch(type=Variable(content='IsNot'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='KW_IS')), Match(type=Variable(content='KW_NOT')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_EQ = Branch(type=Variable(content='Eq'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='EQ_EQ')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_NE = Branch(type=Variable(content='Ne'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='EXC_EQ')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_LE = Branch(type=Variable(content='Le'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='LV_EQ')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_LT = Branch(type=Variable(content='Lt'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='LV')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_GE = Branch(type=Variable(content='Ge'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='RV_EQ')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_GT = Branch(type=Variable(content='Gt'), rule=Sequence(rules=[MatchAs(type=Variable(content='Comparison'), key=Variable(content='left')), Match(type=Variable(content='RV')), MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_BITWISE_OR = Branch(type=Variable(content='BitwiseOr'), rule=Sequence(rules=[MatchAs(type=Variable(content='BitwiseOrGR'), key=Variable(content='left')), Match(type=Variable(content='VBAR')), MatchAs(type=Variable(content='BitwiseXorGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_BITWISE_XOR = Branch(type=Variable(content='BitwiseXor'), rule=Sequence(rules=[MatchAs(type=Variable(content='BitwiseXorGR'), key=Variable(content='left')), Match(type=Variable(content='HAT')), MatchAs(type=Variable(content='BitwiseAndGR'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_BITWISE_AND = Branch(type=Variable(content='BitwiseAnd'), rule=Sequence(rules=[MatchAs(type=Variable(content='BitwiseAndGR'), key=Variable(content='left')), Match(type=Variable(content='AMPERSAND')), MatchAs(type=Variable(content='ShiftExpr'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_LSHIFT = Branch(type=Variable(content='LShift'), rule=Sequence(rules=[MatchAs(type=Variable(content='ShiftExpr'), key=Variable(content='left')), Match(type=Variable(content='LV_LV')), MatchAs(type=Variable(content='Sum'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_RSHIFT = Branch(type=Variable(content='RShift'), rule=Sequence(rules=[MatchAs(type=Variable(content='ShiftExpr'), key=Variable(content='left')), Match(type=Variable(content='RV_RV')), MatchAs(type=Variable(content='Sum'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_ADD = Branch(type=Variable(content='Add'), rule=Sequence(rules=[MatchAs(type=Variable(content='Sum'), key=Variable(content='left')), Match(type=Variable(content='PLUS')), MatchAs(type=Variable(content='Term'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_SUB = Branch(type=Variable(content='Sub'), rule=Sequence(rules=[MatchAs(type=Variable(content='Sum'), key=Variable(content='left')), Match(type=Variable(content='DASH')), MatchAs(type=Variable(content='Term'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_MUL = Branch(type=Variable(content='Mul'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='ASTERISK')), MatchAs(type=Variable(content='Factor'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_TRUE_DIV = Branch(type=Variable(content='TrueDiv'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='SLASH')), MatchAs(type=Variable(content='Factor'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_FLOOR_DIV = Branch(type=Variable(content='FloorDiv'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='SLASH_SLASH')), MatchAs(type=Variable(content='Factor'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_MOD = Branch(type=Variable(content='Mod'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='PERCENT')), MatchAs(type=Variable(content='Factor'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_MAT_MUL = Branch(type=Variable(content='MatMul'), rule=Sequence(rules=[MatchAs(type=Variable(content='Term'), key=Variable(content='left')), Match(type=Variable(content='AT')), MatchAs(type=Variable(content='Factor'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_UADD = Branch(type=Variable(content='UAdd'), rule=Sequence(rules=[Match(type=Variable(content='PLUS')), MatchAs(type=Variable(content='Factor'), key=Variable(content='factor'))]), priority=None, line_prefix=None)
_BRANCH_USUB = Branch(type=Variable(content='USub'), rule=Sequence(rules=[Match(type=Variable(content='DASH')), MatchAs(type=Variable(content='Factor'), key=Variable(content='factor'))]), priority=None, line_prefix=None)
_BRANCH_INVERT = Branch(type=Variable(content='Invert'), rule=Sequence(rules=[Match(type=Variable(content='WAVE')), MatchAs(type=Variable(content='Factor'), key=Variable(content='factor'))]), priority=None, line_prefix=None)
_BRANCH_POW = Branch(type=Variable(content='Pow'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='left')), Match(type=Variable(content='ASTERISK_ASTERISK')), MatchAs(type=Variable(content='Factor'), key=Variable(content='right'))]), priority=None, line_prefix=None)
_BRANCH_IF_EXP = Branch(type=Variable(content='IfExp'), rule=Sequence(rules=[MatchAs(type=Variable(content='Disjunction'), key=Variable(content='body')), Match(type=Variable(content='KW_IF')), MatchAs(type=Variable(content='Disjunction'), key=Variable(content='test')), Match(type=Variable(content='KW_ELSE')), MatchAs(type=Variable(content='Disjunction'), key=Variable(content='or_else'))]), priority=None, line_prefix=None)
_BRANCH_ELSE = Branch(type=Variable(content='Else'), rule=Sequence(rules=[Match(type=Variable(content='KW_ELSE')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block'))]), priority=None, line_prefix=None)
_BRANCH_ELIF = Branch(type=Variable(content='Elif'), rule=Sequence(rules=[Match(type=Variable(content='KW_ELIF')), MatchAs(type=Variable(content='Expression'), key=Variable(content='condition')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Optional(rule=MatchAs(type=Variable(content='ElseGR'), key=Variable(content='alt')))]), priority=None, line_prefix=None)
_BRANCH_WITH_ITEM = Branch(type=Variable(content='WithItem'), rule=Sequence(rules=[MatchAs(type=Variable(content='Expression'), key=Variable(content='context_expr')), Match(type=Variable(content='KW_AS')), MatchAs(type=Variable(content='Expression'), key=Variable(content='optional_vars'))]), priority=None, line_prefix=None)
_BRANCH_TRY = Branch(type=Variable(content='Try'), rule=Sequence(rules=[Match(type=Variable(content='KW_TRY')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), RepeatStar(rule=MatchIn(type=Variable(content='Except'), key=Variable(content='excepts')))]), priority=None, line_prefix=None)
_BRANCH_IF = Branch(type=Variable(content='If'), rule=Sequence(rules=[Match(type=Variable(content='KW_IF')), MatchAs(type=Variable(content='Expression'), key=Variable(content='condition')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Optional(rule=MatchAs(type=Variable(content='ElseGR'), key=Variable(content='alt')))]), priority=None, line_prefix=None)
_BRANCH_WHILE = Branch(type=Variable(content='While'), rule=Sequence(rules=[Match(type=Variable(content='KW_WHILE')), MatchAs(type=Variable(content='Expression'), key=Variable(content='condition')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Optional(rule=MatchAs(type=Variable(content='Else'), key=Variable(content='alt')))]), priority=None, line_prefix=None)
_BRANCH_FOR = Branch(type=Variable(content='For'), rule=Sequence(rules=[Match(type=Variable(content='KW_FOR')), MatchAs(type=Variable(content='StarTargetsGR'), key=Variable(content='target')), Match(type=Variable(content='KW_IN')), MatchAs(type=Variable(content='Expression'), key=Variable(content='iterator')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block')), Optional(rule=MatchAs(type=Variable(content='Else'), key=Variable(content='alt')))]), priority=None, line_prefix=None)
_BRANCH_WITH = Branch(type=Variable(content='With'), rule=Sequence(rules=[Match(type=Variable(content='KW_WITH')), MatchIn(type=Variable(content='WithItem'), key=Variable(content='items')), Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='WithItem'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='WithItem'), key=Variable(content='items'))]))), Match(type=Variable(content='COLON')), Optional(rule=MatchAs(type=Variable(content='Comment'), key=Variable(content='type_comment'))), MatchAs(type=Variable(content='Block'), key=Variable(content='block'))]), priority=None, line_prefix=None)
_BRANCH_YIELD = Branch(type=Variable(content='Yield'), rule=Sequence(rules=[Match(type=Variable(content='KW_YIELD')), MatchAs(type=Variable(content='Returnable'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_YIELD_FROM = Branch(type=Variable(content='YieldFrom'), rule=Sequence(rules=[Match(type=Variable(content='KW_YIELD')), Match(type=Variable(content='KW_FROM')), MatchAs(type=Variable(content='Returnable'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_RETURN = Branch(type=Variable(content='Return'), rule=Sequence(rules=[Match(type=Variable(content='KW_RETURN')), Optional(rule=MatchAs(type=Variable(content='Returnable'), key=Variable(content='expr')))]), priority=None, line_prefix=None)
_BRANCH_ANN_ASSIGN = Branch(type=Variable(content='AnnAssign'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='target')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='annotation'))]))), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))])))]), priority=None, line_prefix=None)
_BRANCH_ASSIGN_TUPLE = Branch(type=Variable(content='AssignTuple'), rule=Sequence(rules=[MatchIn(type=Variable(content='Primary'), key=Variable(content='args')), Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Primary'), key=Variable(content='args')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Primary'), key=Variable(content='args'))]))), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='value'))]), priority=None, line_prefix=None)
_BRANCH_IADD = Branch(type=Variable(content='IAdd'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='obj')), Match(type=Variable(content='PLUS_EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_ISUB = Branch(type=Variable(content='ISub'), rule=Sequence(rules=[MatchAs(type=Variable(content='Primary'), key=Variable(content='obj')), Match(type=Variable(content='DASH_EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_BREAK_CLASS = Branch(type=Variable(content='BreakClass'), rule=Match(type=Variable(content='KW_BREAK')), priority=None, line_prefix=None)
_BRANCH_CONTINUE_CLASS = Branch(type=Variable(content='ContinueClass'), rule=Match(type=Variable(content='KW_CONTINUE')), priority=None, line_prefix=None)
_BRANCH_ANNOTATION = Branch(type=Variable(content='Annotation'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Expression'), key=Variable(content='type'))]), priority=None, line_prefix=None)
_BRANCH_RAISE = Branch(type=Variable(content='Raise'), rule=Sequence(rules=[Match(type=Variable(content='KW_RAISE')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_FROM')), MatchAs(type=Variable(content='Expression'), key=Variable(content='cause'))])))]), priority=None, line_prefix=None)
_BRANCH_PASS_CLASS = Branch(type=Variable(content='PassClass'), rule=Match(type=Variable(content='KW_PASS')), priority=None, line_prefix=None)
_BRANCH_ASSERT = Branch(type=Variable(content='Assert'), rule=Sequence(rules=[Match(type=Variable(content='KW_ASSERT')), MatchAs(type=Variable(content='Expression'), key=Variable(content='test')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchAs(type=Variable(content='Expression'), key=Variable(content='msg'))])))]), priority=None, line_prefix=None)
_BRANCH_STATEMENT_EXPR = Branch(type=Variable(content='StatementExpr'), rule=MatchAs(type=Variable(content='Expression'), key=Variable(content='expr')), priority=None, line_prefix=None)
_BRANCH_EXPR_ENUM = Branch(type=Variable(content='ExprEnum'), rule=Sequence(rules=[MatchIn(type=Variable(content='Expression'), key=Variable(content='items')), RepeatStar(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='COMMA')), MatchIn(type=Variable(content='Expression'), key=Variable(content='items'))])))]), priority=None, line_prefix=None)
_BRANCH_NAMED_ARGUMENT = Branch(type=Variable(content='NamedArgument'), rule=Sequence(rules=[MatchAs(type=Variable(content='Variable'), key=Variable(content='name')), Match(type=Variable(content='EQ')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_SARGUMENT = Branch(type=Variable(content='SArgument'), rule=Sequence(rules=[Match(type=Variable(content='ASTERISK')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_SSARGUMENT = Branch(type=Variable(content='SSArgument'), rule=Sequence(rules=[Match(type=Variable(content='ASTERISK_ASTERISK')), MatchAs(type=Variable(content='Expression'), key=Variable(content='expr'))]), priority=None, line_prefix=None)
_BRANCH_EXCEPT = Branch(type=Variable(content='Except'), rule=Sequence(rules=[Match(type=Variable(content='KW_EXCEPT')), MatchAs(type=Variable(content='Expression'), key=Variable(content='error')), Optional(rule=Grouping(rule=Sequence(rules=[Match(type=Variable(content='KW_AS')), MatchAs(type=Variable(content='Variable'), key=Variable(content='as_'))]))), Match(type=Variable(content='COLON')), MatchAs(type=Variable(content='Block'), key=Variable(content='block'))]), priority=None, line_prefix=None)
_BRANCH_MODULE = Branch(type=Variable(content='Module'), rule=Sequence(rules=[MatchIn(type=Variable(content='Statement'), key=Variable(content='statements')), RepeatStar(rule=MatchIn(type=Variable(content='Statement'), key=Variable(content='statements')))]), priority=None, line_prefix=None)

# GROUPS

_GROUP_IMPORT_FROM_TARGETS = Group(type=Variable('ImportFromTargets'), types=[
    Variable('ImportAliases'),
    Variable('ImportAll')
])
_GROUP_IMPORT_GR = Group(type=Variable('ImportGR'), types=[
    Variable('ImportFrom'),
    Variable('Import')
])
_GROUP_IMPORT_RELATIVE = Group(type=Variable('ImportRelative'), types=[
    Variable('ImportDot'),
    Variable('ImportEllipsis')
])
_GROUP_IMPORT_PATH = Group(type=Variable('ImportPath'), types=[
    Variable('AbsoluteImportPath'),
    Variable('RelativeImportPath')
])
_GROUP_DEF_ARGUMENT_GR = Group(type=Variable('DefArgumentGR'), types=[
    Variable('Argument'),
    Variable('NonKeywordArgument'),
    Variable('KeywordArgument')
])
_GROUP_CLASS_GR = Group(type=Variable('ClassGR'), types=[
    Variable('Def'),
    Variable('Class')
])
_GROUP_MULTI_LINE_STATEMENT = Group(type=Variable('MultiLineStatement'), types=[
    Variable('ClassGR'),
    Variable('MultiLineString')
])
_GROUP_CONSTANT = Group(type=Variable('Constant'), types=[
    Variable('NoneClass'),
    Variable('TrueClass'),
    Variable('FalseClass'),
    Variable('EllipsisClass'),
    Variable('Integer'),
    Variable('Float'),
    Variable('String')
])
_GROUP_ATOM_GR = Group(type=Variable('AtomGR'), types=[
    Variable('Variable'),
    Variable('Constant')
])
_GROUP_STAR_TARGETS_GR = Group(type=Variable('StarTargetsGR'), types=[
    Variable('StarTargets'),
    Variable('Variable')
])
_GROUP_DATA_GR = Group(type=Variable('DataGR'), types=[
    Variable('Tuple'),
    Variable('GenExp'),
    Variable('List'),
    Variable('ListComp'),
    Variable('Dict'),
    Variable('DictComp'),
    Variable('Set'),
    Variable('SetComp'),
    Variable('IndentedList'),
    Variable('AtomGR')
])
_GROUP_SLICE_GR = Group(type=Variable('SliceGR'), types=[
    Variable('Slice'),
    Variable('Expression')
])
_GROUP_PRIMARY = Group(type=Variable('Primary'), types=[
    Variable('Subscript'),
    Variable('GetAttr'),
    Variable('Call'),
    Variable('IndentedCall'),
    Variable('DataGR')
])
_GROUP_DISJUNCTION = Group(type=Variable('Disjunction'), types=[
    Variable('Or'),
    Variable('Conjunction')
])
_GROUP_CONJUNCTION = Group(type=Variable('Conjunction'), types=[
    Variable('And'),
    Variable('Inversion')
])
_GROUP_INVERSION = Group(type=Variable('Inversion'), types=[
    Variable('Not'),
    Variable('Comparison')
])
_GROUP_COMPARISON = Group(type=Variable('Comparison'), types=[
    Variable('NotIn'),
    Variable('In'),
    Variable('IsNot'),
    Variable('Is'),
    Variable('Eq'),
    Variable('Ne'),
    Variable('Le'),
    Variable('Lt'),
    Variable('Ge'),
    Variable('Gt'),
    Variable('BitwiseOrGR')
])
_GROUP_BITWISE_OR_GR = Group(type=Variable('BitwiseOrGR'), types=[
    Variable('BitwiseOr'),
    Variable('BitwiseXorGR')
])
_GROUP_BITWISE_XOR_GR = Group(type=Variable('BitwiseXorGR'), types=[
    Variable('BitwiseXor'),
    Variable('BitwiseAndGR')
])
_GROUP_BITWISE_AND_GR = Group(type=Variable('BitwiseAndGR'), types=[
    Variable('BitwiseAnd'),
    Variable('ShiftExpr')
])
_GROUP_SHIFT_EXPR = Group(type=Variable('ShiftExpr'), types=[
    Variable('LShift'),
    Variable('RShift'),
    Variable('Sum')
])
_GROUP_SUM = Group(type=Variable('Sum'), types=[
    Variable('Add'),
    Variable('Sub'),
    Variable('Term')
])
_GROUP_TERM = Group(type=Variable('Term'), types=[
    Variable('Mul'),
    Variable('TrueDiv'),
    Variable('FloorDiv'),
    Variable('Mod'),
    Variable('MatMul'),
    Variable('Factor')
])
_GROUP_FACTOR = Group(type=Variable('Factor'), types=[
    Variable('UAdd'),
    Variable('USub'),
    Variable('Invert'),
    Variable('Power')
])
_GROUP_POWER = Group(type=Variable('Power'), types=[
    Variable('Pow'),
    Variable('Primary')
])
_GROUP_EXPRESSION = Group(type=Variable('Expression'), types=[
    Variable('IfExp'),
    Variable('LambdaDef'),
    Variable('Disjunction')
])
_GROUP_ELSE_GR = Group(type=Variable('ElseGR'), types=[
    Variable('Else'),
    Variable('Elif')
])
_GROUP_SCOPE_GR = Group(type=Variable('ScopeGR'), types=[
    Variable('Try'),
    Variable('If'),
    Variable('While'),
    Variable('For'),
    Variable('With')
])
_GROUP_RETURN_GR = Group(type=Variable('ReturnGR'), types=[
    Variable('Return'),
    Variable('YieldFrom'),
    Variable('Yield')
])
_GROUP_ASSIGN_GR = Group(type=Variable('AssignGR'), types=[
    Variable('AnnAssign'),
    Variable('AssignTuple')
])
_GROUP_AUG_ASSIGN = Group(type=Variable('AugAssign'), types=[
    Variable('IAdd'),
    Variable('ISub')
])
_GROUP_LOOP_CONTROL_GR = Group(type=Variable('LoopControlGR'), types=[
    Variable('BreakClass'),
    Variable('ContinueClass')
])
_GROUP_STATEMENT = Group(type=Variable('Statement'), types=[
    Variable('ReturnGR'),
    Variable('AssignGR'),
    Variable('AugAssign'),
    Variable('ScopeGR'),
    Variable('Assert'),
    Variable('Comment'),
    Variable('Annotation'),
    Variable('ImportGR'),
    Variable('Raise'),
    Variable('PassClass'),
    Variable('LoopControlGR'),
    Variable('Call'),
    Variable('StatementExpr'),
    Variable('MultiLineStatement')
])
_GROUP_RETURNABLE = Group(type=Variable('Returnable'), types=[
    Variable('Expression'),
    Variable('ExprEnum')
])
_GROUP_CALL_ARGUMENT_GR = Group(type=Variable('CallArgumentGR'), types=[
    Variable('NamedArgument'),
    Variable('SArgument'),
    Variable('SSArgument'),
    Variable('Expression')
])
_GROUP_CODE_GR = Group(type=Variable('CodeGR'), types=[
    Variable('DottedAsName'),
    Variable('EmptyLine'),
    Variable('ForIfClause'),
    Variable('Args'),
    Variable('ImportFromTargets'),
    Variable('ImportRelative'),
    Variable('StarTargetsGR'),
    Variable('SliceGR'),
    Variable('IndentedCallBody'),
    Variable('Decorator'),
    Variable('WithItem'),
    Variable('Alias'),
    Variable('EmptyLine'),
    Variable('CallArgumentGR'),
    Variable('DefArgumentGR'),
    Variable('Module'),
    Variable('Statement'),
    Variable('Block'),
    Variable('ElseGR'),
    Variable('DictItem'),
    Variable('ImportPath'),
    Variable('Except'),
    Variable('Returnable'),
    Variable('IndentedExprEnum')
])


reader = Reader(
    lexer=Lexer(
        patterns=[
            _STRING_DOLLAR,
            _KEYWORD_KW_AS,
            _STRING_COMMA,
            _STRING_ASTERISK,
            _STRING_DOT,
            _KEYWORD_KW_FROM,
            _KEYWORD_KW_IMPORT,
            _STRING_DOT_DOT_DOT,
            _STRING_COLON,
            _STRING_EQ,
            _STRING_ASTERISK_ASTERISK,
            _STRING_AT,
            _KEYWORD_KW_DEF,
            _STRING_LEFT_PARENTHESIS,
            _STRING_RIGHT_PARENTHESIS,
            _STRING_DASH_RV,
            _KEYWORD_KW_CLASS,
            _KEYWORD_KW_NONE,
            _KEYWORD_KW_TRUE,
            _KEYWORD_KW_FALSE,
            _KEYWORD_KW_FOR,
            _KEYWORD_KW_IN,
            _KEYWORD_KW_IF,
            _STRING_LB,
            _STRING_RB,
            _STRING_LS,
            _STRING_RS,
            _KEYWORD_KW_OR,
            _KEYWORD_KW_AND,
            _KEYWORD_KW_NOT,
            _KEYWORD_KW_IS,
            _STRING_EQ_EQ,
            _STRING_EXC_EQ,
            _STRING_LV_EQ,
            _STRING_LV,
            _STRING_RV_EQ,
            _STRING_RV,
            _STRING_VBAR,
            _STRING_HAT,
            _STRING_AMPERSAND,
            _STRING_LV_LV,
            _STRING_RV_RV,
            _STRING_PLUS,
            _STRING_DASH,
            _STRING_SLASH,
            _STRING_SLASH_SLASH,
            _STRING_PERCENT,
            _STRING_WAVE,
            _KEYWORD_KW_ELSE,
            _KEYWORD_KW_ELIF,
            _KEYWORD_KW_TRY,
            _KEYWORD_KW_WHILE,
            _KEYWORD_KW_WITH,
            _KEYWORD_KW_YIELD,
            _KEYWORD_KW_RETURN,
            _STRING_PLUS_EQ,
            _STRING_DASH_EQ,
            _KEYWORD_KW_BREAK,
            _KEYWORD_KW_CONTINUE,
            _KEYWORD_KW_RAISE,
            _KEYWORD_KW_PASS,
            _KEYWORD_KW_ASSERT,
            _KEYWORD_KW_EXCEPT,
            _REGEX_VARIABLE,
            _REGEX_INTEGER,
            _REGEX_FLOAT,
            _REGEX_COMMENT,
            _REGEX_MULTI_LINE_STRING,
            _REGEX_STRING,
            _REGEX_WHITESPACE
        ]
    ),
    parser=Parser(
        branches=[
            _BRANCH_LAMBDA_DEF,
            _BRANCH_ALIAS,
            _BRANCH_IMPORT_ALIASES,
            _BRANCH_IMPORT_ALL,
            _GROUP_IMPORT_FROM_TARGETS,
            _BRANCH_DOTTED_AS_NAME,
            _BRANCH_IMPORT_FROM,
            _BRANCH_IMPORT,
            _GROUP_IMPORT_GR,
            _BRANCH_IMPORT_DOT,
            _BRANCH_IMPORT_ELLIPSIS,
            _GROUP_IMPORT_RELATIVE,
            _BRANCH_ABSOLUTE_IMPORT_PATH,
            _BRANCH_RELATIVE_IMPORT_PATH,
            _GROUP_IMPORT_PATH,
            _BRANCH_BLOCK,
            _BRANCH_ARGS,
            _BRANCH_ARGUMENT,
            _BRANCH_NON_KEYWORD_ARGUMENT,
            _BRANCH_KEYWORD_ARGUMENT,
            _GROUP_DEF_ARGUMENT_GR,
            _BRANCH_DECORATOR,
            _BRANCH_DEF,
            _BRANCH_CLASS,
            _GROUP_CLASS_GR,
            _GROUP_MULTI_LINE_STATEMENT,
            _BRANCH_DICT_ITEM,
            _BRANCH_NONE_CLASS,
            _BRANCH_TRUE_CLASS,
            _BRANCH_FALSE_CLASS,
            _BRANCH_ELLIPSIS_CLASS,
            _GROUP_CONSTANT,
            _GROUP_ATOM_GR,
            _BRANCH_STAR_TARGETS,
            _GROUP_STAR_TARGETS_GR,
            _BRANCH_FOR_IF_CLAUSE,
            _BRANCH_TUPLE,
            _BRANCH_GEN_EXP,
            _BRANCH_INDENTED_LIST,
            _BRANCH_LIST,
            _BRANCH_LIST_COMP,
            _BRANCH_DICT,
            _BRANCH_DICT_COMP,
            _BRANCH_SET,
            _BRANCH_SET_COMP,
            _GROUP_DATA_GR,
            _BRANCH_INDENTED_EXPR_ENUM,
            _BRANCH_SLICE,
            _GROUP_SLICE_GR,
            _BRANCH_SUBSCRIPT,
            _BRANCH_GET_ATTR,
            _BRANCH_CALL,
            _BRANCH_INDENTED_CALL_BODY,
            _BRANCH_INDENTED_CALL,
            _GROUP_PRIMARY,
            _BRANCH_OR,
            _GROUP_DISJUNCTION,
            _BRANCH_AND,
            _GROUP_CONJUNCTION,
            _BRANCH_NOT,
            _GROUP_INVERSION,
            _BRANCH_IN,
            _BRANCH_IS,
            _BRANCH_NOT_IN,
            _BRANCH_IS_NOT,
            _BRANCH_EQ,
            _BRANCH_NE,
            _BRANCH_LE,
            _BRANCH_LT,
            _BRANCH_GE,
            _BRANCH_GT,
            _GROUP_COMPARISON,
            _BRANCH_BITWISE_OR,
            _GROUP_BITWISE_OR_GR,
            _BRANCH_BITWISE_XOR,
            _GROUP_BITWISE_XOR_GR,
            _BRANCH_BITWISE_AND,
            _GROUP_BITWISE_AND_GR,
            _BRANCH_LSHIFT,
            _BRANCH_RSHIFT,
            _GROUP_SHIFT_EXPR,
            _BRANCH_ADD,
            _BRANCH_SUB,
            _GROUP_SUM,
            _BRANCH_MUL,
            _BRANCH_TRUE_DIV,
            _BRANCH_FLOOR_DIV,
            _BRANCH_MOD,
            _BRANCH_MAT_MUL,
            _GROUP_TERM,
            _BRANCH_UADD,
            _BRANCH_USUB,
            _BRANCH_INVERT,
            _GROUP_FACTOR,
            _BRANCH_POW,
            _GROUP_POWER,
            _BRANCH_IF_EXP,
            _GROUP_EXPRESSION,
            _BRANCH_ELSE,
            _BRANCH_ELIF,
            _GROUP_ELSE_GR,
            _BRANCH_WITH_ITEM,
            _BRANCH_TRY,
            _BRANCH_IF,
            _BRANCH_WHILE,
            _BRANCH_FOR,
            _BRANCH_WITH,
            _GROUP_SCOPE_GR,
            _BRANCH_YIELD,
            _BRANCH_YIELD_FROM,
            _BRANCH_RETURN,
            _GROUP_RETURN_GR,
            _BRANCH_ANN_ASSIGN,
            _BRANCH_ASSIGN_TUPLE,
            _GROUP_ASSIGN_GR,
            _BRANCH_IADD,
            _BRANCH_ISUB,
            _GROUP_AUG_ASSIGN,
            _BRANCH_BREAK_CLASS,
            _BRANCH_CONTINUE_CLASS,
            _GROUP_LOOP_CONTROL_GR,
            _BRANCH_ANNOTATION,
            _BRANCH_RAISE,
            _BRANCH_PASS_CLASS,
            _BRANCH_ASSERT,
            _BRANCH_STATEMENT_EXPR,
            _GROUP_STATEMENT,
            _BRANCH_EXPR_ENUM,
            _GROUP_RETURNABLE,
            _BRANCH_NAMED_ARGUMENT,
            _BRANCH_SARGUMENT,
            _BRANCH_SSARGUMENT,
            _GROUP_CALL_ARGUMENT_GR,
            _BRANCH_EXCEPT,
            _BRANCH_MODULE,
            _GROUP_CODE_GR
        ],
        start=Variable('Module')
    )
)
