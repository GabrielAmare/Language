from website.language.bnf.lang.models import *

__all__ = [
    'Regex_String',
    'Regex_Integer',
    'Regex_Variable',
    'Regex_WHITESPACE',
    'Regex_COMMENT',
]

Regex_String = RegexPattern(Variable('String'), String("'\\\"(?:\\\"|[^\\\"])*?(?<!\\\\\\\\)\\\""
                                                       "|\\\'(?:\\\'|[^\\\'])*?(?<!\\\\\\\\)\\\''"))
Regex_Integer = RegexPattern(Variable('Integer'), String("'\\-?\\d+'"))
Regex_Variable = RegexPattern(Variable('Variable'), String("'[a-zA-Z_]\\w*'"))
Regex_WHITESPACE = RegexPattern(Variable('WHITESPACE'), String("'\\s+'"), ignore_=Ignore())
Regex_COMMENT = RegexPattern(Variable('COMMENT'), String("'#.*'"), ignore_=Ignore())
