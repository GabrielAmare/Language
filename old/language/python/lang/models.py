"""
    This module has been auto-generated. Do not change manually.
    WARNING : Manual changes to this file are likely to be overwritten.
"""
from __future__ import annotations

import abc
import ast
import dataclasses
import functools
import itertools
import queries
import typing

from website.language.base.processing import Element, Lemma, Token

__all__ = [
    'AbsoluteImportPath',
    'Add',
    'Alias',
    'And',
    'AnnAssign',
    'Annotation',
    'Args',
    'Argument',
    'Assert',
    'AssignGR',
    'AssignTuple',
    'AtomGR',
    'AugAssign',
    'BREAK',
    'BitwiseAnd',
    'BitwiseAndGR',
    'BitwiseOr',
    'BitwiseOrGR',
    'BitwiseXor',
    'BitwiseXorGR',
    'Block',
    'BreakClass',
    'CONTINUE',
    'Call',
    'CallArgumentGR',
    'Class',
    'ClassGR',
    'CodeGR',
    'Comment',
    'Comparison',
    'Conjunction',
    'Constant',
    'ContinueClass',
    'DataGR',
    'Decorator',
    'Def',
    'DefArgumentGR',
    'Dict',
    'DictComp',
    'DictItem',
    'Disjunction',
    'DottedAsName',
    'ERR_0',
    'ERR_1',
    'ERR_10',
    'ERR_11',
    'ERR_2',
    'ERR_3',
    'ERR_4',
    'ERR_5',
    'ERR_6',
    'ERR_7',
    'ERR_8',
    'ERR_9',
    'Elif',
    'EllipsisClass',
    'Else',
    'ElseGR',
    'EmptyLine',
    'Eq',
    'Except',
    'ExprEnum',
    'Expression',
    'FALSE',
    'Factor',
    'FalseClass',
    'Float',
    'FloorDiv',
    'For',
    'ForIfClause',
    'Ge',
    'GenExp',
    'GetAttr',
    'Gt',
    'IAdd',
    'ISub',
    'If',
    'IfExp',
    'Import',
    'ImportAliases',
    'ImportAll',
    'ImportDot',
    'ImportEllipsis',
    'ImportFrom',
    'ImportFromTargets',
    'ImportGR',
    'ImportPath',
    'ImportRelative',
    'In',
    'IndentedCall',
    'IndentedCallBody',
    'IndentedExprEnum',
    'IndentedList',
    'Integer',
    'Inversion',
    'Invert',
    'Is',
    'IsNot',
    'KeywordArgument',
    'LShift',
    'LambdaDef',
    'Le',
    'List',
    'ListComp',
    'LoopControlGR',
    'Lt',
    'MatMul',
    'Mod',
    'Module',
    'Mul',
    'MultiLineStatement',
    'MultiLineString',
    'NONE',
    'NamedArgument',
    'Ne',
    'NonKeywordArgument',
    'NoneClass',
    'Not',
    'NotIn',
    'Or',
    'PassClass',
    'Pow',
    'Power',
    'Primary',
    'RShift',
    'Raise',
    'RelativeImportPath',
    'Return',
    'ReturnGR',
    'Returnable',
    'SArgument',
    'SSArgument',
    'ScopeGR',
    'Set',
    'SetComp',
    'ShiftExpr',
    'Slice',
    'SliceGR',
    'StarTargets',
    'StarTargetsGR',
    'Statement',
    'StatementExpr',
    'String',
    'Sub',
    'Subscript',
    'Sum',
    'TRUE',
    'Term',
    'TrueClass',
    'TrueDiv',
    'Try',
    'Tuple',
    'UAdd',
    'USub',
    'Variable',
    'While',
    'With',
    'WithItem',
    'Yield',
    'YieldFrom'
]


def _flat_str(method):
    def wrapped(self) -> str:
        return ''.join(method(self))
    return wrapped


def _indented(prefix: str):
    def wrapper(method):
        def wrapped(self) -> str:
            return method(self).replace('\n', '\n' + prefix)
        return wrapped
    return wrapper


@dataclasses.dataclass(frozen=True, order=True)
class CodeGR(abc.ABC):
    """
        >>> DottedAsName  # concrete
        >>> EmptyLine  # concrete
        >>> ForIfClause  # concrete
        >>> Args  # concrete
        >>> ImportFromTargets  # abstract
        >>> ImportRelative  # abstract
        >>> StarTargetsGR  # abstract
        >>> SliceGR  # abstract
        >>> IndentedCallBody  # concrete
        >>> Decorator  # concrete
        >>> WithItem  # concrete
        >>> Alias  # concrete
        >>> EmptyLine  # concrete
        >>> CallArgumentGR  # abstract
        >>> DefArgumentGR  # abstract
        >>> Module  # concrete
        >>> Statement  # abstract
        >>> Block  # concrete
        >>> ElseGR  # abstract
        >>> DictItem  # concrete
        >>> ImportPath  # abstract
        >>> Except  # concrete
        >>> Returnable  # abstract
        >>> IndentedExprEnum  # concrete
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Alias(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Alias := <Variable as name> ?$' ' <KW_AS> $' ' <Variable as as_name>
    """
    name: Variable
    as_name: Variable | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.name)
        if self.as_name:
            yield ' '
            yield 'as'
            yield ' '
            yield str(self.as_name)
    
    @classmethod
    def parse(cls, obj: Element) -> Alias:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            as_name=Variable.parse(obj.data['as_name']) if 'as_name' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.alias) -> Alias:
        return cls(name=Variable.from_str(obj.name), as_name=Variable.from_str(obj.asname) if obj.asname else None)


@dataclasses.dataclass(frozen=True, order=True)
class Args(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Args := <COMMA> $' '.<Variable in variables>
    """
    variables: list[Variable]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.variables:
            for i, e in enumerate(self.variables):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Args:
        assert isinstance(obj, Lemma)
        return cls(
            variables=[Variable.parse(item) for item in obj.data['variables']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> Args:
        if isinstance(obj, ast.Tuple):
            return cls(variables=list(map(Variable.from_ast, obj.elts)))
        elif isinstance(obj, ast.Name):
            return cls(variables=[Variable.from_ast(obj)])
        else:
            raise NotImplementedError(ERR_8, obj)


@dataclasses.dataclass(frozen=True, order=True)
class Block(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Block '    ' := *[$'\\n' <Statement in statements>]
    """
    statements: list[Statement] | None = None
    
    @_indented('    ')
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.statements:
            for e in self.statements:
                yield '\n'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Block:
        assert isinstance(obj, Lemma)
        return cls(
            statements=[Statement.parse(item) for item in obj.data['statements']] if 'statements' in obj.data else None
        )
    
    def is_empty(self) -> bool:
        if not self.statements:
            return True
        for statement in self.statements:
            if isinstance(statement, (PassClass, EllipsisClass, EmptyLine)):
                continue
            else:
                return False
        else:
            return True
    
    def do_if(self, test: Expression) -> If:
        return If(block=self, condition=test, alt=None)
    
    def do_for(self, args: list[Variable], iterator: Expression) -> For:
        if len(args) == 0:
            raise NotImplementedError('Cant do a for loop without arguments.')
        elif len(args) == 1:
            target = args[0]
        else:
            target = StarTargets(elts=args)
        return For(block=self, target=target, iterator=iterator, alt=None)
    
    @classmethod
    def from_ast(cls, statements: list[ast.stmt]) -> Block:
        return Block(statements=list(map(Statement.__from_ast__, statements)))


@dataclasses.dataclass(frozen=True, order=True)
class CallArgumentGR(CodeGR, abc.ABC):
    """
        >>> NamedArgument  # concrete
        >>> SArgument  # concrete
        >>> SSArgument  # concrete
        >>> Expression  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> CallArgumentGR:
        if obj.type == 'NamedArgument':
            return NamedArgument.parse(obj)
        elif obj.type == 'SArgument':
            return SArgument.parse(obj)
        elif obj.type == 'SSArgument':
            return SSArgument.parse(obj)
        else:
            return Expression.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: typing.Union[ast.expr, ast.keyword]) -> CallArgumentGR:
        if isinstance(obj, ast.keyword):
            if obj.arg is None:
                return SSArgument.from_ast(obj.value)
            else:
                return NamedArgument.from_ast(obj)
        elif isinstance(obj, ast.Starred):
            return SArgument(expr=Expression.__from_ast__(obj.value))
        elif isinstance(obj, ast.expr):
            return Expression.__from_ast__(obj)
        else:
            raise NotImplementedError


@dataclasses.dataclass(frozen=True, order=True)
class Decorator(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Decorator := <AT> <Expression as expr>
    """
    expr: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '@'
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> Decorator:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Expression.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> Decorator:
        return cls(expr=Expression.__from_ast__(obj))


@dataclasses.dataclass(frozen=True, order=True)
class DefArgumentGR(CodeGR, abc.ABC):
    """
        >>> Argument  # concrete
        >>> NonKeywordArgument  # concrete
        >>> KeywordArgument  # concrete
    """
    name: Variable
    type: Expression | None = None
    
    @classmethod
    def parse(cls, obj: Element) -> DefArgumentGR:
        if obj.type == 'Argument':
            return Argument.parse(obj)
        elif obj.type == 'NonKeywordArgument':
            return NonKeywordArgument.parse(obj)
        elif obj.type == 'KeywordArgument':
            return KeywordArgument.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @classmethod
    def from_ast_list(cls, obj: ast.arguments) -> list[DefArgumentGR]:
        result = []
        for arg, default in reversed(list(itertools.zip_longest(reversed(obj.args), reversed(obj.defaults), fillvalue=None))):
            result.append(Argument.from_ast(arg, default))
        if obj.vararg:
            arg = Argument.from_ast(obj.vararg)
            result.append(NonKeywordArgument(name=arg.name, type=arg.type))
        if obj.kwarg:
            arg = Argument.from_ast(obj.kwarg)
            result.append(KeywordArgument(name=arg.name, type=arg.type))
        return result


@dataclasses.dataclass(frozen=True, order=True)
class DictItem(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch DictItem := <Expression as key> <COLON> $' ' <Expression as value>
    """
    key: Expression
    value: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.key)
        yield ':'
        yield ' '
        yield str(self.value)
    
    @classmethod
    def parse(cls, obj: Element) -> DictItem:
        assert isinstance(obj, Lemma)
        return cls(
            key=Expression.parse(obj.data['key']),
            value=Expression.parse(obj.data['value'])
        )
    
    @classmethod
    def from_ast(cls, key: ast.expr, value: ast.expr) -> DictItem:
        return cls(key=Expression.__from_ast__(key), value=Expression.__from_ast__(value))


@dataclasses.dataclass(frozen=True, order=True)
class DottedAsName(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch DottedAsName := <DOT>.<Variable in names> ?$' ' <KW_AS> $' ' <Variable as as_name>
    """
    names: list[Variable]
    as_name: Variable | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.names:
            for i, e in enumerate(self.names):
                if i:
                    yield '.'
                yield str(e)
        if self.as_name:
            yield ' '
            yield 'as'
            yield ' '
            yield str(self.as_name)
    
    @classmethod
    def parse(cls, obj: Element) -> DottedAsName:
        assert isinstance(obj, Lemma)
        return cls(
            names=[Variable.parse(item) for item in obj.data['names']],
            as_name=Variable.parse(obj.data['as_name']) if 'as_name' in obj.data else None
        )
    
    def order(self) -> tuple[str, str]:
        return '.'.join((name.content for name in self.names)), self.as_name.content if self.as_name else ''
    
    @classmethod
    def from_ast(cls, obj: ast.alias) -> DottedAsName:
        return DottedAsName(names=list(map(Variable, obj.name.split('.'))), as_name=obj.asname)


@dataclasses.dataclass(frozen=True, order=True)
class ElseGR(CodeGR, abc.ABC):
    """
        >>> Else  # concrete
        >>> Elif  # concrete
    """
    block: Block
    
    @classmethod
    def parse(cls, obj: Element) -> ElseGR:
        if obj.type == 'Else':
            return Else.parse(obj)
        elif obj.type == 'Elif':
            return Elif.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @classmethod
    def __from_ast__(cls, statements: list[ast.stmt]) -> ElseGR:
        if len(statements) == 1:
            statement = statements[0]
            if isinstance(statement, ast.If):
                return Elif.from_ast(statement)
        return Else.from_ast(statements)


@dataclasses.dataclass(frozen=True, order=True)
class EmptyLine(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch EmptyLine := $''
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield ''
    
    @classmethod
    def parse(cls, obj: Element) -> EmptyLine:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class Except(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Except := $'\\n' <KW_EXCEPT> $' ' <Expression as error> ?[$' ' <KW_AS> $' ' <Variable as as_>] <COLON> <…
    """
    error: Expression
    block: Block
    as_: Variable | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '\n'
        yield 'except'
        yield ' '
        yield str(self.error)
        if self.as_:
            yield ' '
            yield 'as'
            yield ' '
            yield str(self.as_)
        yield ':'
        yield str(self.block)
    
    @classmethod
    def parse(cls, obj: Element) -> Except:
        assert isinstance(obj, Lemma)
        return cls(
            error=Expression.parse(obj.data['error']),
            block=Block.parse(obj.data['block']),
            as_=Variable.parse(obj.data['as_']) if 'as_' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.ExceptHandler) -> Except:
        return cls(error=Expression.__from_ast__(obj.type), as_=Variable.from_str(obj.name) if obj.name else None, block=Block.from_ast(obj.body))


@dataclasses.dataclass(frozen=True, order=True)
class ForIfClause(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch ForIfClause := $' ' <KW_FOR> $' ' <StarTargetsGR as target> $' ' <KW_IN> $' ' <Disjunction as iter> *[$'…
    """
    target: StarTargetsGR
    iter: Disjunction
    ifs: list[Disjunction] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield ' '
        yield 'for'
        yield ' '
        yield str(self.target)
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.iter)
        if self.ifs:
            for e in self.ifs:
                yield ' '
                yield 'if'
                yield ' '
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> ForIfClause:
        assert isinstance(obj, Lemma)
        return cls(
            target=StarTargetsGR.parse(obj.data['target']),
            iter=Disjunction.parse(obj.data['iter']),
            ifs=[Disjunction.parse(item) for item in obj.data['ifs']] if 'ifs' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.comprehension) -> ForIfClause:
        return cls(target=StarTargetsGR.__from_ast__(obj.target), iter=Disjunction.__from_ast__(obj.iter), ifs=list(map(Disjunction.__from_ast__, obj.ifs)) if obj.ifs else None)


@dataclasses.dataclass(frozen=True, order=True)
class ImportFromTargets(CodeGR, abc.ABC):
    """
        >>> ImportAliases  # concrete
        >>> ImportAll  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> ImportFromTargets:
        if obj.type == 'ImportAliases':
            return ImportAliases.parse(obj)
        elif obj.type == 'ImportAll':
            return ImportAll.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class ImportPath(CodeGR, abc.ABC):
    """
        >>> AbsoluteImportPath  # concrete
        >>> RelativeImportPath  # concrete
    """
    variables: list[Variable]
    
    @classmethod
    def parse(cls, obj: Element) -> ImportPath:
        if obj.type == 'AbsoluteImportPath':
            return AbsoluteImportPath.parse(obj)
        elif obj.type == 'RelativeImportPath':
            return RelativeImportPath.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @classmethod
    def from_str(cls, __value: str) -> ImportPath:
        relatives = []
        while __value.startswith('...'):
            relatives.append(ImportEllipsis())
            __value = __value[3:]
        while __value.startswith('.'):
            relatives.append(ImportDot())
            __value = __value[1:]
        variables = []
        if __value:
            variables.extend(map(Variable, __value.split('.')))
        if relatives:
            return RelativeImportPath(relatives=relatives, variables=variables)
        elif variables:
            return AbsoluteImportPath(variables=variables)
        else:
            raise ValueError('Invalid empty path !')
    
    @abc.abstractmethod
    def order(self) -> tuple[int, str]:
        pass


@dataclasses.dataclass(frozen=True, order=True)
class ImportRelative(CodeGR, abc.ABC):
    """
        >>> ImportDot  # concrete
        >>> ImportEllipsis  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> ImportRelative:
        if obj.type == 'ImportDot':
            return ImportDot.parse(obj)
        elif obj.type == 'ImportEllipsis':
            return ImportEllipsis.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class IndentedCallBody(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch IndentedCallBody '    ' := $'\\n' <COMMA> $'\\n'.<CallArgumentGR in args>
    """
    args: list[CallArgumentGR]
    
    @_indented('    ')
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '\n'
        if self.args:
            for i, e in enumerate(self.args):
                if i:
                    yield ','
                    yield '\n'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> IndentedCallBody:
        assert isinstance(obj, Lemma)
        return cls(
            args=[CallArgumentGR.parse(item) for item in obj.data['args']]
        )


@dataclasses.dataclass(frozen=True, order=True)
class IndentedExprEnum(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch IndentedExprEnum '    ' := $'\\n' <COMMA> $'\\n'.<Expression in items>
    """
    items: list[Expression]
    
    @_indented('    ')
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '\n'
        if self.items:
            for i, e in enumerate(self.items):
                if i:
                    yield ','
                    yield '\n'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> IndentedExprEnum:
        assert isinstance(obj, Lemma)
        return cls(
            items=[Expression.parse(item) for item in obj.data['items']]
        )


@dataclasses.dataclass(frozen=True, order=True)
class Module(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Module := $'\\n'.<Statement in statements>
    """
    statements: list[Statement]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.statements:
            for i, e in enumerate(self.statements):
                if i:
                    yield '\n'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Module:
        assert isinstance(obj, Lemma)
        return cls(
            statements=[Statement.parse(item) for item in obj.data['statements']]
        )
    
    @property
    def q_statements(self) -> queries.QueryList[Statement]:
        return queries.QueryList(self.statements)
    
    @property
    def classes(self) -> queries.Query[Class]:
        return self.q_statements.instanceof(Class)
    
    @property
    def functions(self) -> queries.Query[Def]:
        return self.q_statements.instanceof(Def)
    
    def get_class(self, name: Variable) -> Class:
        for cls in self.classes:
            if cls.name == name:
                return cls
        else:
            raise KeyError(name)
    
    def get_function(self, name: Variable) -> Def:
        for cls in self.functions:
            if cls.name == name:
                return cls
        else:
            raise KeyError(name)
    
    @classmethod
    def from_ast(cls, obj: ast.Module) -> Module:
        return cls(statements=list(map(Statement.__from_ast__, obj.body)))
    
    @classmethod
    def from_text(cls, src: str) -> Module:
        obj = ast.parse(source=src)
        return cls.from_ast(obj)
    
    @classmethod
    def from_file(cls, __fp: str) -> Module:
        with open(__fp, mode='r', encoding='utf-8') as file:
            src = file.read()
        return cls.from_text(src)


@dataclasses.dataclass(frozen=True, order=True)
class Returnable(CodeGR, abc.ABC):
    """
        >>> Expression  # abstract
        >>> ExprEnum  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> Returnable:
        if obj.type == 'ExprEnum':
            return ExprEnum.parse(obj)
        else:
            return Expression.parse(obj)
    
    @property
    def as_return(self) -> Return:
        return Return(expr=self)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Returnable:
        if isinstance(obj, ast.Tuple):
            return ExprEnum.from_ast(obj)
        else:
            return Expression.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class SliceGR(CodeGR, abc.ABC):
    """
        >>> Slice  # concrete
        >>> Expression  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> SliceGR:
        if obj.type == 'Slice':
            return Slice.parse(obj)
        else:
            return Expression.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: typing.Union[ast.Slice, ast.expr]) -> typing.Union[SliceGR, ExprEnum]:
        if isinstance(obj, ast.Slice):
            if isinstance(obj, ast.Slice):
                return Slice.from_ast(obj)
            elif isinstance(obj, ast.Index):
                if isinstance(obj.value, ast.Tuple):
                    return ExprEnum(items=list(map(Expression.__from_ast__, obj.value.elts)))
                else:
                    return Expression.__from_ast__(obj.value)
            elif isinstance(obj, ast.ExtSlice):
                raise NotImplementedError(ERR_1, obj)
            else:
                raise NotImplementedError(ERR_2, obj)
        elif isinstance(obj, ast.Tuple):
            return ExprEnum(items=list(map(Expression.__from_ast__, obj.elts)))
        else:
            return Expression.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class StarTargetsGR(CodeGR, abc.ABC):
    """
        >>> StarTargets  # concrete
        >>> Variable  # atomic
    """
    @classmethod
    def parse(cls, obj: Element) -> StarTargetsGR:
        if obj.type == 'StarTargets':
            return StarTargets.parse(obj)
        elif obj.type == 'Variable':
            return Variable.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> StarTargetsGR:
        if isinstance(obj, ast.Tuple):
            return StarTargets.from_ast(obj)
        else:
            return Variable.from_ast(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Statement(CodeGR, abc.ABC):
    """
        >>> ReturnGR  # abstract
        >>> AssignGR  # abstract
        >>> AugAssign  # abstract
        >>> ScopeGR  # abstract
        >>> Assert  # concrete
        >>> Comment  # atomic
        >>> Annotation  # concrete
        >>> ImportGR  # abstract
        >>> Raise  # concrete
        >>> PassClass  # concrete
        >>> LoopControlGR  # abstract
        >>> Call  # concrete
        >>> StatementExpr  # concrete
        >>> MultiLineStatement  # abstract
    """
    
    def is_type_switch(self) -> bool:
        if not isinstance(self, If):
            return False
        tests, cases, default = self.flatten()
        arg: typing.Optional[Expression] = None
        types: list[Expression] = []
        for index, test in enumerate(tests):
            if not isinstance(test, Call):
                return False
            if test.left != Variable('isinstance'):
                return False
            if len(test.args) != 2:
                return False
            arg1, arg2 = test.args
            if not isinstance(arg1, Expression):
                return False
            if index == 0:
                arg = arg1
            elif arg != arg1:
                return False
            types.append(arg2)
        if arg is None:
            return False
        return True
    
    def as_type_switch(self) -> tuple[Expression, list[Expression], list[Block], typing.Optional[Block]]:
        _error = ValueError('not a type switch -> ' + repr(str(self)))
        if not isinstance(self, If):
            raise _error
        tests, cases, default = self.flatten()
        arg: typing.Optional[Expression] = None
        types: list[Expression] = []
        for index, test in enumerate(tests):
            if not isinstance(test, Call):
                raise _error
            if test.left != Variable('isinstance'):
                raise _error
            if len(test.args) != 2:
                raise _error
            arg1, arg2 = test.args
            if not isinstance(arg1, Expression):
                raise _error
            if index == 0:
                arg = arg1
            elif arg != arg1:
                raise _error
            types.append(arg2)
        if arg is None:
            raise _error
        return arg, types, cases, default
    
    @classmethod
    def __from_ast__(cls, obj: ast.stmt) -> Statement:
        if isinstance(obj, ast.Expr):
            return StatementExpr.from_ast(obj)
        elif isinstance(obj, ast.Import):
            return Import.from_ast(obj)
        elif isinstance(obj, ast.ImportFrom):
            return ImportFrom.from_ast(obj)
        elif isinstance(obj, ast.Return):
            return Return.from_ast(obj)
        elif isinstance(obj, ast.Raise):
            return Raise.from_ast(obj)
        elif isinstance(obj, ast.Assert):
            return Assert.from_ast(obj)
        elif isinstance(obj, ast.Pass):
            return PassClass.from_ast(obj)
        elif isinstance(obj, ast.Continue):
            return ContinueClass.from_ast(obj)
        elif isinstance(obj, ast.Break):
            return BreakClass.from_ast(obj)
        elif isinstance(obj, ast.If):
            return If.from_ast(obj)
        elif isinstance(obj, ast.For):
            return For.from_ast(obj)
        elif isinstance(obj, ast.While):
            return While.from_ast(obj)
        elif isinstance(obj, ast.With):
            return With.from_ast(obj)
        elif isinstance(obj, (ast.Assign, ast.AnnAssign)):
            return AnnAssign.from_ast(obj)
        elif isinstance(obj, ast.FunctionDef):
            return Def.from_ast(obj)
        elif isinstance(obj, ast.ClassDef):
            return Class.from_ast(obj)
        elif isinstance(obj, ast.AugAssign):
            return AugAssign.__from_ast__(obj)
        elif isinstance(obj, ast.Try):
            return Try.from_ast(obj)
        else:
            raise NotImplementedError(ERR_5, obj)


@dataclasses.dataclass(frozen=True, order=True)
class WithItem(CodeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch WithItem := <Expression as context_expr> $' ' <KW_AS> $' ' <Expression as optional_vars>
    """
    context_expr: Expression
    optional_vars: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.context_expr)
        yield ' '
        yield 'as'
        yield ' '
        yield str(self.optional_vars)
    
    @classmethod
    def parse(cls, obj: Element) -> WithItem:
        assert isinstance(obj, Lemma)
        return cls(
            context_expr=Expression.parse(obj.data['context_expr']),
            optional_vars=Expression.parse(obj.data['optional_vars'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.withitem) -> WithItem:
        return cls(context_expr=Expression.__from_ast__(obj.context_expr), optional_vars=Expression.__from_ast__(obj.optional_vars))


@dataclasses.dataclass(frozen=True, order=True)
class AbsoluteImportPath(ImportPath):
    """
        This class has been generated automatically from the bnf rule :
        branch AbsoluteImportPath := <DOT>.<Variable in variables>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.variables:
            for i, e in enumerate(self.variables):
                if i:
                    yield '.'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> AbsoluteImportPath:
        assert isinstance(obj, Lemma)
        return cls(
            variables=[Variable.parse(item) for item in obj.data['variables']]
        )
    
    def order(self) -> tuple[int, str]:
        return 0, str(self)


@dataclasses.dataclass(frozen=True, order=True)
class Annotation(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Annotation := <Variable as name> <COLON> $' ' <Expression as type>
    """
    name: Variable
    type: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.name)
        yield ':'
        yield ' '
        yield str(self.type)
    
    @classmethod
    def parse(cls, obj: Element) -> Annotation:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            type=Expression.parse(obj.data['type'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Argument(DefArgumentGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Argument := <Variable as name> ?[<COLON> $' ' <Expression as type>] ?[$' ' <EQ> $' ' <Expression as defa…
    """
    default: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield str(self.type)
        if self.default:
            yield ' '
            yield '='
            yield ' '
            yield str(self.default)
    
    @classmethod
    def parse(cls, obj: Element) -> Argument:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            type=Expression.parse(obj.data['type']) if 'type' in obj.data else None,
            default=Expression.parse(obj.data['default']) if 'default' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.arg, default = None) -> Argument:
        return cls(name=Variable.from_str(obj.arg), type=Expression.__from_ast__(obj.annotation) if obj.annotation else None, default=None if default is None else Expression.__from_ast__(default))


@dataclasses.dataclass(frozen=True, order=True)
class Assert(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Assert := <KW_ASSERT> $' ' <Expression as test> ?[<COMMA> $' ' <Expression as msg>]
    """
    test: Expression
    msg: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'assert'
        yield ' '
        yield str(self.test)
        if self.msg:
            yield ','
            yield ' '
            yield str(self.msg)
    
    @classmethod
    def parse(cls, obj: Element) -> Assert:
        assert isinstance(obj, Lemma)
        return cls(
            test=Expression.parse(obj.data['test']),
            msg=Expression.parse(obj.data['msg']) if 'msg' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Assert) -> Assert:
        return cls(test=Expression.__from_ast__(obj.test), msg=Expression.__from_ast__(obj.msg) if obj.msg else None)


@dataclasses.dataclass(frozen=True, order=True)
class AssignGR(Statement, abc.ABC):
    """
        >>> AnnAssign  # concrete
        >>> AssignTuple  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> AssignGR:
        if obj.type == 'AnnAssign':
            return AnnAssign.parse(obj)
        elif obj.type == 'AssignTuple':
            return AssignTuple.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class AugAssign(Statement, abc.ABC):
    """
        >>> IAdd  # concrete
        >>> ISub  # concrete
    """
    obj: Primary
    expr: Expression
    
    @classmethod
    def parse(cls, obj: Element) -> AugAssign:
        if obj.type == 'IAdd':
            return IAdd.parse(obj)
        elif obj.type == 'ISub':
            return ISub.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @classmethod
    def __from_ast__(cls, obj: ast.AugAssign) -> AugAssign:
        if isinstance(obj.op, ast.Add):
            return IAdd.from_ast(obj)
        elif isinstance(obj.op, ast.Sub):
            return ISub.from_ast(obj)
        else:
            raise NotImplementedError(ERR_6, obj)


@dataclasses.dataclass(frozen=True, order=True)
class Comment(Statement):
    """
        This class has been generated automatically from the bnf rule :
        regex   Comment '#.*'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Comment:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    @classmethod
    def from_str(cls, obj: typing.Optional[str]) -> typing.Optional[Comment]:
        if obj is None:
            return None
        return cls(content='# {}'.format(obj))


@dataclasses.dataclass(frozen=True, order=True)
class Elif(ElseGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Elif := $'\\n' <KW_ELIF> $' ' <Expression as condition> <COLON> <Block as block> ?<ElseGR as alt>
    """
    condition: Expression
    alt: ElseGR | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '\n'
        yield 'elif'
        yield ' '
        yield str(self.condition)
        yield ':'
        yield str(self.block)
        if self.alt:
            yield str(self.alt)
    
    @classmethod
    def parse(cls, obj: Element) -> Elif:
        assert isinstance(obj, Lemma)
        return cls(
            condition=Expression.parse(obj.data['condition']),
            block=Block.parse(obj.data['block']),
            alt=ElseGR.parse(obj.data['alt']) if 'alt' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.If) -> Elif:
        return cls(condition=Expression.__from_ast__(obj.test), block=Block.from_ast(obj.body), alt=ElseGR.__from_ast__(obj.orelse) if obj.orelse else None)


@dataclasses.dataclass(frozen=True, order=True)
class Else(ElseGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Else := $'\\n' <KW_ELSE> <COLON> <Block as block>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '\n'
        yield 'else'
        yield ':'
        yield str(self.block)
    
    @classmethod
    def parse(cls, obj: Element) -> Else:
        assert isinstance(obj, Lemma)
        return cls(
            block=Block.parse(obj.data['block'])
        )
    
    @classmethod
    def from_ast(cls, statements: list[ast.stmt]) -> Else:
        return cls(block=Block.from_ast(statements))


@dataclasses.dataclass(frozen=True, order=True)
class ExprEnum(Returnable):
    """
        This class has been generated automatically from the bnf rule :
        branch ExprEnum := <COMMA> $' '.<Expression in items>
    """
    items: list[Expression]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.items:
            for i, e in enumerate(self.items):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> ExprEnum:
        assert isinstance(obj, Lemma)
        return cls(
            items=[Expression.parse(item) for item in obj.data['items']]
        )
    
    @classmethod
    def from_ast_slice(cls, obj: typing.Union[ast.expr, ast.slice]):
        if isinstance(obj, ast.expr):
            return Expression.__from_ast__(obj)
        elif isinstance(obj, ast.Index):
            return Returnable.__from_ast__(obj.value)
        else:
            NotImplementedError(obj)
    
    @classmethod
    def from_ast(cls, obj: ast.Tuple) -> ExprEnum:
        return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@dataclasses.dataclass(frozen=True, order=True)
class Expression(CallArgumentGR, Returnable, SliceGR, abc.ABC):
    """
        >>> IfExp  # concrete
        >>> LambdaDef  # concrete
        >>> Disjunction  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Expression:
        if obj.type == 'IfExp':
            return IfExp.parse(obj)
        elif obj.type == 'LambdaDef':
            return LambdaDef.parse(obj)
        else:
            return Disjunction.parse(obj)
    
    @property
    def as_raise(self) -> Raise:
        return Raise(expr=self)
    
    @property
    def as_yield(self) -> Yield:
        return Yield(expr=self)
    
    @property
    def as_yield_from(self) -> YieldFrom:
        return YieldFrom(expr=self)
    
    @property
    def as_decorator(self) -> Decorator:
        return Decorator(expr=self)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Expression:
        if isinstance(obj, ast.IfExp):
            return IfExp.from_ast(obj)
        elif isinstance(obj, ast.Lambda):
            raise NotImplementedError(ERR_0, obj)
        else:
            return Disjunction.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class ImportAliases(ImportFromTargets):
    """
        This class has been generated automatically from the bnf rule :
        branch ImportAliases := <COMMA> $' '.<Alias in names>
    """
    names: list[Alias]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.names:
            for i, e in enumerate(self.names):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> ImportAliases:
        assert isinstance(obj, Lemma)
        return cls(
            names=[Alias.parse(item) for item in obj.data['names']]
        )


@dataclasses.dataclass(frozen=True, order=True)
class ImportAll(ImportFromTargets):
    """
        This class has been generated automatically from the bnf rule :
        branch ImportAll := <ASTERISK>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '*'
    
    @classmethod
    def parse(cls, obj: Element) -> ImportAll:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class ImportDot(ImportRelative):
    """
        This class has been generated automatically from the bnf rule :
        branch ImportDot := <DOT>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '.'
    
    @classmethod
    def parse(cls, obj: Element) -> ImportDot:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class ImportEllipsis(ImportRelative):
    """
        This class has been generated automatically from the bnf rule :
        branch ImportEllipsis := <DOT_DOT_DOT>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '...'
    
    @classmethod
    def parse(cls, obj: Element) -> ImportEllipsis:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class ImportGR(Statement, abc.ABC):
    """
        >>> ImportFrom  # concrete
        >>> Import  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> ImportGR:
        if obj.type == 'ImportFrom':
            return ImportFrom.parse(obj)
        elif obj.type == 'Import':
            return Import.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class KeywordArgument(DefArgumentGR):
    """
        This class has been generated automatically from the bnf rule :
        branch KeywordArgument := <ASTERISK_ASTERISK> <Variable as name> ?[<COLON> $' ' <Expression as type>]
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '**'
        yield str(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield str(self.type)
    
    @classmethod
    def parse(cls, obj: Element) -> KeywordArgument:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            type=Expression.parse(obj.data['type']) if 'type' in obj.data else None
        )


@dataclasses.dataclass(frozen=True, order=True)
class LoopControlGR(Statement, abc.ABC):
    """
        >>> BreakClass  # concrete
        >>> ContinueClass  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> LoopControlGR:
        if obj.type == 'BreakClass':
            return BreakClass.parse(obj)
        elif obj.type == 'ContinueClass':
            return ContinueClass.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class MultiLineStatement(Statement, abc.ABC):
    """
        >>> ClassGR  # abstract
        >>> MultiLineString  # atomic
    """
    @classmethod
    def parse(cls, obj: Element) -> MultiLineStatement:
        if obj.type == 'MultiLineString':
            return MultiLineString.parse(obj)
        else:
            return ClassGR.parse(obj)


@dataclasses.dataclass(frozen=True, order=True)
class NamedArgument(CallArgumentGR):
    """
        This class has been generated automatically from the bnf rule :
        branch NamedArgument := <Variable as name> <EQ> <Expression as expr>
    """
    name: Variable
    expr: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.name)
        yield '='
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> NamedArgument:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            expr=Expression.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.keyword) -> NamedArgument:
        return cls(name=Variable.from_str(obj.arg), expr=Expression.__from_ast__(obj.value))


@dataclasses.dataclass(frozen=True, order=True)
class NonKeywordArgument(DefArgumentGR):
    """
        This class has been generated automatically from the bnf rule :
        branch NonKeywordArgument := <ASTERISK> <Variable as name> ?[<COLON> $' ' <Expression as type>]
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '*'
        yield str(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield str(self.type)
    
    @classmethod
    def parse(cls, obj: Element) -> NonKeywordArgument:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            type=Expression.parse(obj.data['type']) if 'type' in obj.data else None
        )


@dataclasses.dataclass(frozen=True, order=True)
class PassClass(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch PassClass := <KW_PASS>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'pass'
    
    @classmethod
    def parse(cls, obj: Element) -> PassClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )
    
    @classmethod
    def from_ast(cls, _: ast.Pass) -> PassClass:
        return cls()


@dataclasses.dataclass(frozen=True, order=True)
class Raise(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Raise := <KW_RAISE> $' ' <Expression as expr> ?[$' ' <KW_FROM> $' ' <Expression as cause>]
    """
    expr: Expression
    cause: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'raise'
        yield ' '
        yield str(self.expr)
        if self.cause:
            yield ' '
            yield 'from'
            yield ' '
            yield str(self.cause)
    
    @classmethod
    def parse(cls, obj: Element) -> Raise:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Expression.parse(obj.data['expr']),
            cause=Expression.parse(obj.data['cause']) if 'cause' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Raise) -> Raise:
        return cls(expr=Expression.__from_ast__(obj.exc), cause=Expression.__from_ast__(obj.cause) if obj.cause else None)


@dataclasses.dataclass(frozen=True, order=True)
class RelativeImportPath(ImportPath):
    """
        This class has been generated automatically from the bnf rule :
        branch RelativeImportPath := +<ImportRelative in relatives> <DOT>.<Variable in variables>
    """
    relatives: list[ImportRelative]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for e in self.relatives:
            yield str(e)
        if self.variables:
            for i, e in enumerate(self.variables):
                if i:
                    yield '.'
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> RelativeImportPath:
        assert isinstance(obj, Lemma)
        return cls(
            relatives=[ImportRelative.parse(item) for item in obj.data['relatives']],
            variables=[Variable.parse(item) for item in obj.data['variables']]
        )
    
    def relative_level(self) -> int:
        count = 0
        for relative in self.relatives:
            if isinstance(relative, ImportDot):
                count += 1
            elif isinstance(relative, ImportEllipsis):
                count += 3
            else:
                raise NotImplementedError
        return count
    
    def order(self) -> tuple[int, str]:
        return 1, str(self)


@dataclasses.dataclass(frozen=True, order=True)
class ReturnGR(Statement, abc.ABC):
    """
        >>> Return  # concrete
        >>> YieldFrom  # concrete
        >>> Yield  # concrete
    """
    @classmethod
    def parse(cls, obj: Element) -> ReturnGR:
        if obj.type == 'Return':
            return Return.parse(obj)
        elif obj.type == 'YieldFrom':
            return YieldFrom.parse(obj)
        elif obj.type == 'Yield':
            return Yield.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class SArgument(CallArgumentGR):
    """
        This class has been generated automatically from the bnf rule :
        branch SArgument := <ASTERISK> <Expression as expr>
    """
    expr: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '*'
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> SArgument:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Expression.parse(obj.data['expr'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class SSArgument(CallArgumentGR):
    """
        This class has been generated automatically from the bnf rule :
        branch SSArgument := <ASTERISK_ASTERISK> <Expression as expr>
    """
    expr: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '**'
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> SSArgument:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Expression.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> SSArgument:
        return cls(expr=Expression.__from_ast__(obj))


@dataclasses.dataclass(frozen=True, order=True)
class ScopeGR(Statement, abc.ABC):
    """
        >>> Try  # concrete
        >>> If  # concrete
        >>> While  # concrete
        >>> For  # concrete
        >>> With  # concrete
    """
    block: Block
    
    @classmethod
    def parse(cls, obj: Element) -> ScopeGR:
        if obj.type == 'Try':
            return Try.parse(obj)
        elif obj.type == 'If':
            return If.parse(obj)
        elif obj.type == 'While':
            return While.parse(obj)
        elif obj.type == 'For':
            return For.parse(obj)
        elif obj.type == 'With':
            return With.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class Slice(SliceGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Slice := ?<Expression as lower> <COLON> ?<Expression as upper> ?[<COLON> $' ' <Expression as step>]
    """
    lower: Expression | None = None
    upper: Expression | None = None
    step: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.lower:
            yield str(self.lower)
        yield ':'
        if self.upper:
            yield str(self.upper)
        if self.step:
            yield ':'
            yield ' '
            yield str(self.step)
    
    @classmethod
    def parse(cls, obj: Element) -> Slice:
        assert isinstance(obj, Lemma)
        return cls(
            lower=Expression.parse(obj.data['lower']) if 'lower' in obj.data else None,
            upper=Expression.parse(obj.data['upper']) if 'upper' in obj.data else None,
            step=Expression.parse(obj.data['step']) if 'step' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Slice) -> Slice:
        return cls(lower=Expression.__from_ast__(obj.lower), upper=Expression.__from_ast__(obj.upper) if obj.upper else None, step=Expression.__from_ast__(obj.step) if obj.step else None)


@dataclasses.dataclass(frozen=True, order=True)
class StarTargets(StarTargetsGR):
    """
        This class has been generated automatically from the bnf rule :
        branch StarTargets := <COMMA> $' '..<AtomGR in elts>
    """
    elts: list[AtomGR]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.elts):
            if i:
                yield ','
                yield ' '
            yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> StarTargets:
        assert isinstance(obj, Lemma)
        return cls(
            elts=[AtomGR.parse(item) for item in obj.data['elts']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Tuple) -> StarTargets:
        return cls(elts=list(map(Variable.from_ast, obj.elts)))


@dataclasses.dataclass(frozen=True, order=True)
class StatementExpr(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch StatementExpr := <Expression as expr>
    """
    expr: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> StatementExpr:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Expression.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Expr) -> typing.Union[StatementExpr, Yield, YieldFrom]:
        if isinstance(obj.value, ast.Yield):
            return Yield.from_ast(obj.value)
        elif isinstance(obj.value, ast.YieldFrom):
            return YieldFrom.from_ast(obj.value)
        else:
            return cls(expr=Expression.__from_ast__(obj.value))


@dataclasses.dataclass(frozen=True, order=True)
class AnnAssign(AssignGR):
    """
        This class has been generated automatically from the bnf rule :
        branch AnnAssign := <Primary as target> ?[<COLON> $' ' <Expression as annotation>] ?[$' ' <EQ> $' ' <Expression…
    """
    target: Primary
    annotation: Expression | None = None
    value: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.target)
        if self.annotation:
            yield ':'
            yield ' '
            yield str(self.annotation)
        if self.value:
            yield ' '
            yield '='
            yield ' '
            yield str(self.value)
    
    @classmethod
    def parse(cls, obj: Element) -> AnnAssign:
        assert isinstance(obj, Lemma)
        return cls(
            target=Primary.parse(obj.data['target']),
            annotation=Expression.parse(obj.data['annotation']) if 'annotation' in obj.data else None,
            value=Expression.parse(obj.data['value']) if 'value' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: typing.Union[ast.Assign, ast.AnnAssign]) -> AnnAssign:
        if isinstance(obj, ast.Assign):
            if len(obj.targets) == 1:
                return cls(target=Returnable.__from_ast__(obj.targets[0]), annotation=None, value=Expression.__from_ast__(obj.value))
            else:
                raise NotImplementedError(ERR_9, obj)
        elif isinstance(obj, ast.AnnAssign):
            return cls(target=Primary.__from_ast__(obj.target), annotation=Expression.__from_ast__(obj.annotation), value=Expression.__from_ast__(obj.value) if obj.value else None)
        else:
            raise NotImplementedError(ERR_10, obj)


@dataclasses.dataclass(frozen=True, order=True)
class AssignTuple(AssignGR):
    """
        This class has been generated automatically from the bnf rule :
        branch AssignTuple := <COMMA> $' '..<Primary in args> $' ' <EQ> $' ' <Expression as value>
    """
    args: list[Primary]
    value: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        for i, e in enumerate(self.args):
            if i:
                yield ','
                yield ' '
            yield str(e)
        yield ' '
        yield '='
        yield ' '
        yield str(self.value)
    
    @classmethod
    def parse(cls, obj: Element) -> AssignTuple:
        assert isinstance(obj, Lemma)
        return cls(
            args=[Primary.parse(item) for item in obj.data['args']],
            value=Expression.parse(obj.data['value'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class BreakClass(LoopControlGR):
    """
        This class has been generated automatically from the bnf rule :
        branch BreakClass := <KW_BREAK>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'break'
    
    @classmethod
    def parse(cls, obj: Element) -> BreakClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )
    
    @classmethod
    def from_ast(cls, _: ast.Break) -> BreakClass:
        return cls()


@dataclasses.dataclass(frozen=True, order=True)
class ClassGR(MultiLineStatement, abc.ABC):
    """
        >>> Def  # concrete
        >>> Class  # concrete
    """
    name: Variable
    block: Block
    decorators: list[Decorator] | None = None
    
    @classmethod
    def parse(cls, obj: Element) -> ClassGR:
        if obj.type == 'Def':
            return Def.parse(obj)
        elif obj.type == 'Class':
            return Class.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))


@dataclasses.dataclass(frozen=True, order=True)
class ContinueClass(LoopControlGR):
    """
        This class has been generated automatically from the bnf rule :
        branch ContinueClass := <KW_CONTINUE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'continue'
    
    @classmethod
    def parse(cls, obj: Element) -> ContinueClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )
    
    @classmethod
    def from_ast(cls, _: ast.Continue) -> ContinueClass:
        return cls()


@dataclasses.dataclass(frozen=True, order=True)
class Disjunction(Expression, abc.ABC):
    """
        >>> Or  # concrete
        >>> Conjunction  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Disjunction:
        if obj.type == 'Or':
            return Or.parse(obj)
        else:
            return Conjunction.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Disjunction:
        if isinstance(obj, ast.BoolOp):
            if isinstance(obj.op, ast.Or):
                return Or.from_ast(obj)
        return Conjunction.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class For(ScopeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch For := <KW_FOR> $' ' <StarTargetsGR as target> $' ' <KW_IN> $' ' <Expression as iterator> <COLON> <Block…
    """
    target: StarTargetsGR
    iterator: Expression
    alt: Else | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'for'
        yield ' '
        yield str(self.target)
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.iterator)
        yield ':'
        yield str(self.block)
        if self.alt:
            yield str(self.alt)
    
    @classmethod
    def parse(cls, obj: Element) -> For:
        assert isinstance(obj, Lemma)
        return cls(
            target=StarTargetsGR.parse(obj.data['target']),
            iterator=Expression.parse(obj.data['iterator']),
            block=Block.parse(obj.data['block']),
            alt=Else.parse(obj.data['alt']) if 'alt' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.For) -> For:
        return cls(target=StarTargetsGR.__from_ast__(obj.target), iterator=Expression.__from_ast__(obj.iter), block=Block.from_ast(obj.body), alt=Else.from_ast(obj.orelse) if obj.orelse else None)


@dataclasses.dataclass(frozen=True, order=True)
class IAdd(AugAssign):
    """
        This class has been generated automatically from the bnf rule :
        branch IAdd := <Primary as obj> $' ' <PLUS_EQ> $' ' <Expression as expr>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.obj)
        yield ' '
        yield '+='
        yield ' '
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> IAdd:
        assert isinstance(obj, Lemma)
        return cls(
            obj=Primary.parse(obj.data['obj']),
            expr=Expression.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.AugAssign) -> IAdd:
        return cls(obj=Primary.__from_ast__(obj.target), expr=Expression.__from_ast__(obj.value))


@dataclasses.dataclass(frozen=True, order=True)
class ISub(AugAssign):
    """
        This class has been generated automatically from the bnf rule :
        branch ISub := <Primary as obj> $' ' <DASH_EQ> $' ' <Expression as expr>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.obj)
        yield ' '
        yield '-='
        yield ' '
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> ISub:
        assert isinstance(obj, Lemma)
        return cls(
            obj=Primary.parse(obj.data['obj']),
            expr=Expression.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.AugAssign) -> ISub:
        return cls(obj=Primary.__from_ast__(obj.target), expr=Expression.__from_ast__(obj.value))


@dataclasses.dataclass(frozen=True, order=True)
class If(ScopeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch If := <KW_IF> $' ' <Expression as condition> <COLON> <Block as block> ?<ElseGR as alt>
    """
    condition: Expression
    alt: ElseGR | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'if'
        yield ' '
        yield str(self.condition)
        yield ':'
        yield str(self.block)
        if self.alt:
            yield str(self.alt)
    
    @classmethod
    def parse(cls, obj: Element) -> If:
        assert isinstance(obj, Lemma)
        return cls(
            condition=Expression.parse(obj.data['condition']),
            block=Block.parse(obj.data['block']),
            alt=ElseGR.parse(obj.data['alt']) if 'alt' in obj.data else None
        )
    
    def flatten(self) -> tuple[list[Expression], list[Block], typing.Optional[Block]]:
        tests: list[Expression] = []
        codes: list[Block] = []
        default: typing.Optional[Block] = None
        curr = self
        while curr:
            if isinstance(curr, (If, Elif)):
                tests.append(curr.condition)
                codes.append(curr.block)
                curr = curr.alt
            elif isinstance(curr, Else):
                default = curr.block
                curr = None
            else:
                raise NotImplementedError
        return tests, codes, default
    
    @classmethod
    def switch(cls, if_list: list[If], default: typing.Optional[Block]) -> If:
        if not if_list:
            raise ValueError("Can't build a switch without If instances.")
        if isinstance(default, Block):
            result = Else(block=default)
        else:
            result = None
        first_if = if_list[0]
        if_list = if_list[1:]
        for if_stmt in reversed(if_list):
            assert if_stmt.alt is None, 'cannot make a switch with an if statement which already has an alt block.'
            result = Elif(condition=if_stmt.condition, block=if_stmt.block, alt=result)
        return cls(condition=first_if.condition, block=first_if.block, alt=result)
    
    @classmethod
    def from_ast(cls, obj: ast.If) -> If:
        return cls(condition=Expression.__from_ast__(obj.test), block=Block.from_ast(obj.body), alt=ElseGR.__from_ast__(obj.orelse) if obj.orelse else None)


@dataclasses.dataclass(frozen=True, order=True)
class IfExp(Expression):
    """
        This class has been generated automatically from the bnf rule :
        branch IfExp := <Disjunction as body> $' ' <KW_IF> $' ' <Disjunction as test> $' ' <KW_ELSE> $' ' <Disjunction …
    """
    body: Disjunction
    test: Disjunction
    or_else: Disjunction
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.body)
        yield ' '
        yield 'if'
        yield ' '
        yield str(self.test)
        yield ' '
        yield 'else'
        yield ' '
        yield str(self.or_else)
    
    @classmethod
    def parse(cls, obj: Element) -> IfExp:
        assert isinstance(obj, Lemma)
        return cls(
            body=Disjunction.parse(obj.data['body']),
            test=Disjunction.parse(obj.data['test']),
            or_else=Disjunction.parse(obj.data['or_else'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.IfExp) -> IfExp:
        return cls(body=Disjunction.__from_ast__(obj.body), test=Disjunction.__from_ast__(obj.test), or_else=Disjunction.__from_ast__(obj.orelse))


@dataclasses.dataclass(frozen=True, order=True)
class Import(ImportGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Import := <KW_IMPORT> $' ' <COMMA> $' '.<DottedAsName in targets>
    """
    targets: list[DottedAsName]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'import'
        yield ' '
        if self.targets:
            for i, e in enumerate(self.targets):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Import:
        assert isinstance(obj, Lemma)
        return cls(
            targets=[DottedAsName.parse(item) for item in obj.data['targets']]
        )
    
    def order(self):
        return ' '.join(map(str, self.targets))
    
    @classmethod
    def from_ast(cls, obj: ast.Import) -> Import:
        return cls(targets=list(map(DottedAsName.from_ast, obj.names)))


@dataclasses.dataclass(frozen=True, order=True)
class ImportFrom(ImportGR):
    """
        This class has been generated automatically from the bnf rule :
        branch ImportFrom := <KW_FROM> $' ' <ImportPath as path> $' ' <KW_IMPORT> $' ' <ImportFromTargets as targets>
    """
    path: ImportPath
    targets: ImportFromTargets
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'from'
        yield ' '
        yield str(self.path)
        yield ' '
        yield 'import'
        yield ' '
        yield str(self.targets)
    
    @classmethod
    def parse(cls, obj: Element) -> ImportFrom:
        assert isinstance(obj, Lemma)
        return cls(
            path=ImportPath.parse(obj.data['path']),
            targets=ImportFromTargets.parse(obj.data['targets'])
        )
    
    def order(self):
        return self.path.order()
    
    @classmethod
    def from_ast(cls, obj: ast.ImportFrom) -> ImportFrom:
        if obj.module.startswith('.'):
            raise NotImplementedError(ERR_11, obj)
        variables = []
        for name in obj.module.split('.'):
            variables.append(Variable(content=name))
        if len(obj.names) == 1 and obj.names[0].name == '*' and obj.names[0].asname is None:
            targets = ImportAll()
        else:
            targets = ImportAliases(names=list(map(Alias.from_ast, obj.names)))
        return cls(path=AbsoluteImportPath(variables=variables), targets=targets)


@dataclasses.dataclass(frozen=True, order=True)
class LambdaDef(Expression):
    """
        This class has been generated automatically from the bnf rule :
        branch LambdaDef := <DOLLAR>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '$'
    
    @classmethod
    def parse(cls, obj: Element) -> LambdaDef:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class MultiLineString(MultiLineStatement):
    """
        This class has been generated automatically from the bnf rule :
        regex   MultiLineString '\\"\\"\\".*?\\"\\"\\"' 16
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> MultiLineString:
        assert isinstance(obj, Token)
        return cls(content=obj.content)


@dataclasses.dataclass(frozen=True, order=True)
class Return(ReturnGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Return := <KW_RETURN> ?[$' ' <Returnable as expr>]
    """
    expr: Returnable | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'return'
        if self.expr:
            yield ' '
            yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> Return:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Returnable.parse(obj.data['expr']) if 'expr' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Return) -> Return:
        return cls(expr=Returnable.__from_ast__(obj.value))


@dataclasses.dataclass(frozen=True, order=True)
class Try(ScopeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Try := <KW_TRY> <COLON> <Block as block> *<Except in excepts>
    """
    excepts: list[Except] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'try'
        yield ':'
        yield str(self.block)
        if self.excepts:
            for e in self.excepts:
                yield str(e)
    
    @classmethod
    def parse(cls, obj: Element) -> Try:
        assert isinstance(obj, Lemma)
        return cls(
            block=Block.parse(obj.data['block']),
            excepts=[Except.parse(item) for item in obj.data['excepts']] if 'excepts' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Try) -> Try:
        return cls(block=Block.from_ast(obj.body), excepts=list(map(Except.from_ast, obj.handlers)) if obj.handlers else None)


@dataclasses.dataclass(frozen=True, order=True)
class While(ScopeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch While := <KW_WHILE> $' ' <Expression as condition> <COLON> <Block as block> ?<Else as alt>
    """
    condition: Expression
    alt: Else | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'while'
        yield ' '
        yield str(self.condition)
        yield ':'
        yield str(self.block)
        if self.alt:
            yield str(self.alt)
    
    @classmethod
    def parse(cls, obj: Element) -> While:
        assert isinstance(obj, Lemma)
        return cls(
            condition=Expression.parse(obj.data['condition']),
            block=Block.parse(obj.data['block']),
            alt=Else.parse(obj.data['alt']) if 'alt' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.While) -> While:
        return cls(condition=Expression.__from_ast__(obj.test), block=Block.from_ast(obj.body), alt=Else.from_ast(obj.orelse) if obj.orelse else None)


@dataclasses.dataclass(frozen=True, order=True)
class With(ScopeGR):
    """
        This class has been generated automatically from the bnf rule :
        branch With := <KW_WITH> $' ' <COMMA> $' '..<WithItem in items> <COLON> ?<Comment as type_comment> <Block as bl…
    """
    items: list[WithItem]
    type_comment: Comment | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'with'
        yield ' '
        for i, e in enumerate(self.items):
            if i:
                yield ','
                yield ' '
            yield str(e)
        yield ':'
        if self.type_comment:
            yield str(self.type_comment)
        yield str(self.block)
    
    @classmethod
    def parse(cls, obj: Element) -> With:
        assert isinstance(obj, Lemma)
        return cls(
            items=[WithItem.parse(item) for item in obj.data['items']],
            block=Block.parse(obj.data['block']),
            type_comment=Comment.parse(obj.data['type_comment']) if 'type_comment' in obj.data else None
        )
    
    @classmethod
    def from_ast(cls, obj: ast.With) -> With:
        return cls(items=list(map(WithItem.from_ast, obj.items)), block=Block.from_ast(obj.body), type_comment=Comment.from_str(obj.type_comment))


@dataclasses.dataclass(frozen=True, order=True)
class Yield(ReturnGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Yield := <KW_YIELD> $' ' <Returnable as expr>
    """
    expr: Returnable
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'yield'
        yield ' '
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> Yield:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Returnable.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Yield) -> Yield:
        return cls(expr=Returnable.__from_ast__(obj.value) if obj.value else None)


@dataclasses.dataclass(frozen=True, order=True)
class YieldFrom(ReturnGR):
    """
        This class has been generated automatically from the bnf rule :
        branch YieldFrom := <KW_YIELD> $' ' <KW_FROM> $' ' <Returnable as expr>
    """
    expr: Returnable
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'yield'
        yield ' '
        yield 'from'
        yield ' '
        yield str(self.expr)
    
    @classmethod
    def parse(cls, obj: Element) -> YieldFrom:
        assert isinstance(obj, Lemma)
        return cls(
            expr=Returnable.parse(obj.data['expr'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.YieldFrom) -> YieldFrom:
        return cls(expr=Returnable.__from_ast__(obj.value) if obj.value else None)


@dataclasses.dataclass(frozen=True, order=True)
class Class(ClassGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Class := *[<Decorator in decorators> $'\\n'] <KW_CLASS> $' ' <Variable as name> ?[<LEFT_PARENTHESIS> <Ar…
    """
    mro: Args | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.decorators:
            for e in self.decorators:
                yield str(e)
                yield '\n'
        yield 'class'
        yield ' '
        yield str(self.name)
        if self.mro:
            yield '('
            yield str(self.mro)
            yield ')'
        yield ':'
        yield str(self.block)
    
    @classmethod
    def parse(cls, obj: Element) -> Class:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            block=Block.parse(obj.data['block']),
            decorators=[Decorator.parse(item) for item in obj.data['decorators']] if 'decorators' in obj.data else None,
            mro=Args.parse(obj.data['mro']) if 'mro' in obj.data else None
        )
    
    def append_method(self, method: Def) -> None:
        if not method.is_method() and not method.is_class_method():
            raise ValueError()
        if self.block.is_empty():
            self.block.statements.clear()
        if self.block.statements:
            self.block.statements.append(EmptyLine())
        self.block.statements.append(method)
    
    @classmethod
    def from_ast(cls, obj: ast.ClassDef) -> Class:
        bases = Args(variables=list(map(Variable.from_ast, obj.bases))) if obj.bases else None
        return cls(decorators=list(map(Decorator.from_ast, obj.decorator_list)) if obj.decorator_list else None, name=Variable(obj.name), mro=bases, block=Block(statements=list(map(Statement.__from_ast__, obj.body))))


@dataclasses.dataclass(frozen=True, order=True)
class Conjunction(Disjunction, abc.ABC):
    """
        >>> And  # concrete
        >>> Inversion  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Conjunction:
        if obj.type == 'And':
            return And.parse(obj)
        else:
            return Inversion.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Conjunction:
        if isinstance(obj, ast.BoolOp):
            if isinstance(obj.op, ast.And):
                return And.from_ast(obj)
        return Inversion.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Def(ClassGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Def := *[<Decorator in decorators> $'\\n'] <KW_DEF> $' ' <Variable as name> <LEFT_PARENTHESIS> ?[<COMMA>…
    """
    args: list[DefArgumentGR] | None = None
    rtype: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.decorators:
            for e in self.decorators:
                yield str(e)
                yield '\n'
        yield 'def'
        yield ' '
        yield str(self.name)
        yield '('
        if self.args:
            if self.args:
                for i, e in enumerate(self.args):
                    if i:
                        yield ','
                        yield ' '
                    yield str(e)
        yield ')'
        if self.rtype:
            yield ' '
            yield '->'
            yield ' '
            yield str(self.rtype)
        yield ':'
        yield str(self.block)
    
    @classmethod
    def parse(cls, obj: Element) -> Def:
        assert isinstance(obj, Lemma)
        return cls(
            name=Variable.parse(obj.data['name']),
            block=Block.parse(obj.data['block']),
            decorators=[Decorator.parse(item) for item in obj.data['decorators']] if 'decorators' in obj.data else None,
            args=[DefArgumentGR.parse(item) for item in obj.data['args']] if 'args' in obj.data else None,
            rtype=Expression.parse(obj.data['rtype']) if 'rtype' in obj.data else None
        )
    
    def is_method(self):
        return self.args and self.args[0].name == Variable('self')
    
    def is_class_method(self):
        return self.args and self.args[0].name == Variable('cls')
    
    def get_argument(self, name: Variable) -> DefArgumentGR:
        for arg in self.args:
            if arg.name == name:
                return arg
        else:
            raise KeyError(name)
    
    @classmethod
    def from_ast(cls, obj: ast.FunctionDef) -> Def:
        return cls(decorators=list(map(Decorator.from_ast, obj.decorator_list)) if obj.decorator_list else None, name=Variable(obj.name), args=DefArgumentGR.from_ast_list(obj.args), block=Block(statements=list(map(Statement.__from_ast__, obj.body))), rtype=Expression.__from_ast__(obj.returns) if obj.returns else None)


@dataclasses.dataclass(frozen=True, order=True)
class Or(Disjunction):
    """
        This class has been generated automatically from the bnf rule :
        branch Or := <Disjunction as left> $' ' <KW_OR> $' ' <Conjunction as right>
    """
    left: Disjunction
    right: Conjunction
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'or'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Or:
        assert isinstance(obj, Lemma)
        return cls(
            left=Disjunction.parse(obj.data['left']),
            right=Conjunction.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BoolOp) -> Or:
        values = list(map(Conjunction.__from_ast__, obj.values))
        left = values[0]
        rights = values[1:]
        for right in rights:
            left = cls(left=left, right=right)
        return left


@dataclasses.dataclass(frozen=True, order=True)
class And(Conjunction):
    """
        This class has been generated automatically from the bnf rule :
        branch And := <Conjunction as left> $' ' <KW_AND> $' ' <Inversion as right>
    """
    left: Conjunction
    right: Inversion
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'and'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> And:
        assert isinstance(obj, Lemma)
        return cls(
            left=Conjunction.parse(obj.data['left']),
            right=Inversion.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BoolOp) -> And:
        values = list(map(Inversion.__from_ast__, obj.values))
        left = values[0]
        rights = values[1:]
        for right in rights:
            left = cls(left=left, right=right)
        return left


@dataclasses.dataclass(frozen=True, order=True)
class Inversion(Conjunction, abc.ABC):
    """
        >>> Not  # concrete
        >>> Comparison  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Inversion:
        if obj.type == 'Not':
            return Not.parse(obj)
        else:
            return Comparison.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Inversion:
        if isinstance(obj, ast.UnaryOp):
            if isinstance(obj.op, ast.Not):
                return Not.from_ast(obj.operand)
        return Comparison.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Comparison(Inversion, abc.ABC):
    """
        >>> NotIn  # concrete
        >>> In  # concrete
        >>> IsNot  # concrete
        >>> Is  # concrete
        >>> Eq  # concrete
        >>> Ne  # concrete
        >>> Le  # concrete
        >>> Lt  # concrete
        >>> Ge  # concrete
        >>> Gt  # concrete
        >>> BitwiseOrGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Comparison:
        if obj.type == 'NotIn':
            return NotIn.parse(obj)
        elif obj.type == 'In':
            return In.parse(obj)
        elif obj.type == 'IsNot':
            return IsNot.parse(obj)
        elif obj.type == 'Is':
            return Is.parse(obj)
        elif obj.type == 'Eq':
            return Eq.parse(obj)
        elif obj.type == 'Ne':
            return Ne.parse(obj)
        elif obj.type == 'Le':
            return Le.parse(obj)
        elif obj.type == 'Lt':
            return Lt.parse(obj)
        elif obj.type == 'Ge':
            return Ge.parse(obj)
        elif obj.type == 'Gt':
            return Gt.parse(obj)
        else:
            return BitwiseOrGR.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Comparison:
        if isinstance(obj, ast.Compare):
            left = Comparison.__from_ast__(obj.left)
            for comparator, op in zip(obj.comparators, obj.ops):
                if isinstance(op, ast.Eq):
                    factory = Eq
                elif isinstance(op, ast.NotEq):
                    factory = Ne
                elif isinstance(op, ast.Is):
                    factory = Is
                elif isinstance(op, ast.IsNot):
                    factory = IsNot
                elif isinstance(op, ast.In):
                    factory = In
                elif isinstance(op, ast.NotIn):
                    factory = NotIn
                elif isinstance(op, ast.Gt):
                    factory = Gt
                elif isinstance(op, ast.Lt):
                    factory = Lt
                elif isinstance(op, ast.GtE):
                    factory = Ge
                elif isinstance(op, ast.LtE):
                    factory = Le
                else:
                    raise TypeError(type(op))
                left = factory(left=left, right=BitwiseOrGR.__from_ast__(comparator))
            return left
        else:
            return BitwiseOrGR.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Not(Inversion):
    """
        This class has been generated automatically from the bnf rule :
        branch Not := <KW_NOT> $' ' <Inversion as right>
    """
    right: Inversion
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'not'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Not:
        assert isinstance(obj, Lemma)
        return cls(
            right=Inversion.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> Not:
        return cls(right=Inversion.__from_ast__(obj))


@dataclasses.dataclass(frozen=True, order=True)
class BitwiseOrGR(Comparison, abc.ABC):
    """
        >>> BitwiseOr  # concrete
        >>> BitwiseXorGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> BitwiseOrGR:
        if obj.type == 'BitwiseOr':
            return BitwiseOr.parse(obj)
        else:
            return BitwiseXorGR.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> BitwiseOrGR:
        if isinstance(obj, ast.BinOp):
            if isinstance(obj.op, ast.BitOr):
                return BitwiseOr.from_ast(obj)
        return BitwiseXorGR.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Eq(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Eq := <Comparison as left> $' ' <EQ_EQ> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '=='
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Eq:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Ge(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Ge := <Comparison as left> $' ' <RV_EQ> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '>='
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Ge:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Gt(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Gt := <Comparison as left> $' ' <RV> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '>'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Gt:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class In(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch In := <Comparison as left> $' ' <KW_IN> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> In:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Is(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Is := <Comparison as left> $' ' <KW_IS> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'is'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Is:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class IsNot(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch IsNot := <Comparison as left> $' ' <KW_IS> $' ' <KW_NOT> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'is'
        yield ' '
        yield 'not'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> IsNot:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Le(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Le := <Comparison as left> $' ' <LV_EQ> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '<='
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Le:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Lt(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Lt := <Comparison as left> $' ' <LV> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '<'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Lt:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Ne(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Ne := <Comparison as left> $' ' <EXC_EQ> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '!='
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Ne:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class NotIn(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch NotIn := <Comparison as left> $' ' <KW_NOT> $' ' <KW_IN> $' ' <BitwiseOrGR as right>
    """
    left: Comparison
    right: BitwiseOrGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'not'
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> NotIn:
        assert isinstance(obj, Lemma)
        return cls(
            left=Comparison.parse(obj.data['left']),
            right=BitwiseOrGR.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class BitwiseOr(BitwiseOrGR):
    """
        This class has been generated automatically from the bnf rule :
        branch BitwiseOr := <BitwiseOrGR as left> $' ' <VBAR> $' ' <BitwiseXorGR as right>
    """
    left: BitwiseOrGR
    right: BitwiseXorGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '|'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> BitwiseOr:
        assert isinstance(obj, Lemma)
        return cls(
            left=BitwiseOrGR.parse(obj.data['left']),
            right=BitwiseXorGR.parse(obj.data['right'])
        )
    
    @classmethod
    def from_list(cls, args: list[BitwiseXorGR]) -> BitwiseOrGR:
        if len(args) == 0:
            raise NotImplementedError
        if len(args) == 1:
            return args[0]
        return functools.reduce(cls, args)
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> BitwiseOr:
        return cls(left=BitwiseOrGR.__from_ast__(obj.left), right=BitwiseXorGR.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class BitwiseXorGR(BitwiseOrGR, abc.ABC):
    """
        >>> BitwiseXor  # concrete
        >>> BitwiseAndGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> BitwiseXorGR:
        if obj.type == 'BitwiseXor':
            return BitwiseXor.parse(obj)
        else:
            return BitwiseAndGR.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> BitwiseXorGR:
        if isinstance(obj, ast.BinOp):
            if isinstance(obj.op, ast.BitXor):
                return BitwiseXor.from_ast(obj)
        return BitwiseAndGR.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class BitwiseAndGR(BitwiseXorGR, abc.ABC):
    """
        >>> BitwiseAnd  # concrete
        >>> ShiftExpr  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> BitwiseAndGR:
        if obj.type == 'BitwiseAnd':
            return BitwiseAnd.parse(obj)
        else:
            return ShiftExpr.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> BitwiseAndGR:
        if isinstance(obj, ast.BinOp):
            if isinstance(obj.op, ast.BitAnd):
                return BitwiseAnd.from_ast(obj)
        return ShiftExpr.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class BitwiseXor(BitwiseXorGR):
    """
        This class has been generated automatically from the bnf rule :
        branch BitwiseXor := <BitwiseXorGR as left> $' ' <HAT> $' ' <BitwiseAndGR as right>
    """
    left: BitwiseXorGR
    right: BitwiseAndGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '^'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> BitwiseXor:
        assert isinstance(obj, Lemma)
        return cls(
            left=BitwiseXorGR.parse(obj.data['left']),
            right=BitwiseAndGR.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> BitwiseXor:
        return cls(left=BitwiseXorGR.__from_ast__(obj.left), right=BitwiseAndGR.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class BitwiseAnd(BitwiseAndGR):
    """
        This class has been generated automatically from the bnf rule :
        branch BitwiseAnd := <BitwiseAndGR as left> $' ' <AMPERSAND> $' ' <ShiftExpr as right>
    """
    left: BitwiseAndGR
    right: ShiftExpr
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '&'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> BitwiseAnd:
        assert isinstance(obj, Lemma)
        return cls(
            left=BitwiseAndGR.parse(obj.data['left']),
            right=ShiftExpr.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> BitwiseAnd:
        return cls(left=BitwiseAndGR.__from_ast__(obj.left), right=ShiftExpr.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class ShiftExpr(BitwiseAndGR, abc.ABC):
    """
        >>> LShift  # concrete
        >>> RShift  # concrete
        >>> Sum  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> ShiftExpr:
        if obj.type == 'LShift':
            return LShift.parse(obj)
        elif obj.type == 'RShift':
            return RShift.parse(obj)
        else:
            return Sum.parse(obj)
    
    def __lshift__(self, other: Sum) -> LShift:
        return LShift(left=self, right=other)
    
    def __rshift__(self, other: Sum) -> RShift:
        return RShift(left=self, right=other)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> ShiftExpr:
        return Sum.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class LShift(ShiftExpr):
    """
        This class has been generated automatically from the bnf rule :
        branch LShift := <ShiftExpr as left> $' ' <LV_LV> $' ' <Sum as right>
    """
    left: ShiftExpr
    right: Sum
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '<<'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> LShift:
        assert isinstance(obj, Lemma)
        return cls(
            left=ShiftExpr.parse(obj.data['left']),
            right=Sum.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class RShift(ShiftExpr):
    """
        This class has been generated automatically from the bnf rule :
        branch RShift := <ShiftExpr as left> $' ' <RV_RV> $' ' <Sum as right>
    """
    left: ShiftExpr
    right: Sum
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '>>'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> RShift:
        assert isinstance(obj, Lemma)
        return cls(
            left=ShiftExpr.parse(obj.data['left']),
            right=Sum.parse(obj.data['right'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Sum(ShiftExpr, abc.ABC):
    """
        >>> Add  # concrete
        >>> Sub  # concrete
        >>> Term  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Sum:
        if obj.type == 'Add':
            return Add.parse(obj)
        elif obj.type == 'Sub':
            return Sub.parse(obj)
        else:
            return Term.parse(obj)
    
    def __add__(self, other: Term) -> Add:
        return Add(left=self, right=other)
    
    def __sub__(self, other: Term) -> Sub:
        return Sub(left=self, right=other)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Sum:
        if isinstance(obj, ast.BinOp):
            if isinstance(obj.op, ast.Add):
                return Add.from_ast(obj)
            elif isinstance(obj.op, ast.Sub):
                return Sub.from_ast(obj)
        return Term.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Add(Sum):
    """
        This class has been generated automatically from the bnf rule :
        branch Add := <Sum as left> $' ' <PLUS> $' ' <Term as right>
    """
    left: Sum
    right: Term
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '+'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Add:
        assert isinstance(obj, Lemma)
        return cls(
            left=Sum.parse(obj.data['left']),
            right=Term.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> Add:
        return cls(left=Sum.__from_ast__(obj.left), right=Term.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class Sub(Sum):
    """
        This class has been generated automatically from the bnf rule :
        branch Sub := <Sum as left> $' ' <DASH> $' ' <Term as right>
    """
    left: Sum
    right: Term
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '-'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Sub:
        assert isinstance(obj, Lemma)
        return cls(
            left=Sum.parse(obj.data['left']),
            right=Term.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> Sub:
        return cls(left=Sum.__from_ast__(obj.left), right=Term.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class Term(Sum, abc.ABC):
    """
        >>> Mul  # concrete
        >>> TrueDiv  # concrete
        >>> FloorDiv  # concrete
        >>> Mod  # concrete
        >>> MatMul  # concrete
        >>> Factor  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Term:
        if obj.type == 'Mul':
            return Mul.parse(obj)
        elif obj.type == 'TrueDiv':
            return TrueDiv.parse(obj)
        elif obj.type == 'FloorDiv':
            return FloorDiv.parse(obj)
        elif obj.type == 'Mod':
            return Mod.parse(obj)
        elif obj.type == 'MatMul':
            return MatMul.parse(obj)
        else:
            return Factor.parse(obj)
    
    def __mul__(self, other: Factor) -> Mul:
        return Mul(left=self, right=other)
    
    def __truediv__(self, other: Factor) -> TrueDiv:
        return TrueDiv(left=self, right=other)
    
    def __mod__(self, other: Factor) -> Mod:
        return Mod(left=self, right=other)
    
    def __matmul__(self, other: Factor) -> MatMul:
        return MatMul(left=self, right=other)
    
    def __floordiv__(self, other: Factor) -> FloorDiv:
        return FloorDiv(left=self, right=other)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Term:
        if isinstance(obj, ast.BinOp):
            if isinstance(obj.op, ast.Mult):
                return Mul.from_ast(obj)
            elif isinstance(obj.op, ast.Div):
                return TrueDiv.from_ast(obj)
            elif isinstance(obj.op, ast.FloorDiv):
                return FloorDiv.from_ast(obj)
            elif isinstance(obj.op, ast.MatMult):
                return MatMul.from_ast(obj)
            elif isinstance(obj.op, ast.Mod):
                return Mod.from_ast(obj)
        return Factor.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Factor(Term, abc.ABC):
    """
        >>> UAdd  # concrete
        >>> USub  # concrete
        >>> Invert  # concrete
        >>> Power  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Factor:
        if obj.type == 'UAdd':
            return UAdd.parse(obj)
        elif obj.type == 'USub':
            return USub.parse(obj)
        elif obj.type == 'Invert':
            return Invert.parse(obj)
        else:
            return Power.parse(obj)
    
    def __pos__(self) -> UAdd:
        return UAdd(factor=self)
    
    def __neg__(self) -> USub:
        return USub(factor=self)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Factor:
        if isinstance(obj, ast.UnaryOp):
            if isinstance(obj.op, ast.UAdd):
                return UAdd.from_ast(obj.operand)
            elif isinstance(obj.op, ast.USub):
                return USub.from_ast(obj.operand)
            elif isinstance(obj.op, ast.Invert):
                return Invert.from_ast(obj.operand)
        return Power.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class FloorDiv(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch FloorDiv := <Term as left> $' ' <SLASH_SLASH> $' ' <Factor as right>
    """
    left: Term
    right: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '//'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> FloorDiv:
        assert isinstance(obj, Lemma)
        return cls(
            left=Term.parse(obj.data['left']),
            right=Factor.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> FloorDiv:
        return cls(left=Term.__from_ast__(obj.left), right=Factor.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class MatMul(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch MatMul := <Term as left> $' ' <AT> $' ' <Factor as right>
    """
    left: Term
    right: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '@'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> MatMul:
        assert isinstance(obj, Lemma)
        return cls(
            left=Term.parse(obj.data['left']),
            right=Factor.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> MatMul:
        return cls(left=Term.__from_ast__(obj.left), right=Factor.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class Mod(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch Mod := <Term as left> $' ' <PERCENT> $' ' <Factor as right>
    """
    left: Term
    right: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '%'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Mod:
        assert isinstance(obj, Lemma)
        return cls(
            left=Term.parse(obj.data['left']),
            right=Factor.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> Mod:
        return cls(left=Term.__from_ast__(obj.left), right=Factor.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class Mul(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch Mul := <Term as left> $' ' <ASTERISK> $' ' <Factor as right>
    """
    left: Term
    right: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '*'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Mul:
        assert isinstance(obj, Lemma)
        return cls(
            left=Term.parse(obj.data['left']),
            right=Factor.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> Mul:
        return cls(left=Term.__from_ast__(obj.left), right=Factor.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class TrueDiv(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch TrueDiv := <Term as left> $' ' <SLASH> $' ' <Factor as right>
    """
    left: Term
    right: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '/'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> TrueDiv:
        assert isinstance(obj, Lemma)
        return cls(
            left=Term.parse(obj.data['left']),
            right=Factor.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> TrueDiv:
        return cls(left=Term.__from_ast__(obj.left), right=Factor.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class Invert(Factor):
    """
        This class has been generated automatically from the bnf rule :
        branch Invert := <WAVE> <Factor as factor>
    """
    factor: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '~'
        yield str(self.factor)
    
    @classmethod
    def parse(cls, obj: Element) -> Invert:
        assert isinstance(obj, Lemma)
        return cls(
            factor=Factor.parse(obj.data['factor'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> Invert:
        return cls(factor=Factor.__from_ast__(obj))


@dataclasses.dataclass(frozen=True, order=True)
class Power(Factor, abc.ABC):
    """
        >>> Pow  # concrete
        >>> Primary  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Power:
        if obj.type == 'Pow':
            return Pow.parse(obj)
        else:
            return Primary.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Factor:
        if isinstance(obj, ast.BinOp):
            if isinstance(obj.op, ast.Pow):
                return Pow.from_ast(obj)
        return Primary.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class UAdd(Factor):
    """
        This class has been generated automatically from the bnf rule :
        branch UAdd := <PLUS> <Factor as factor>
    """
    factor: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '+'
        yield str(self.factor)
    
    @classmethod
    def parse(cls, obj: Element) -> UAdd:
        assert isinstance(obj, Lemma)
        return cls(
            factor=Factor.parse(obj.data['factor'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> UAdd:
        return cls(factor=Factor.__from_ast__(obj))


@dataclasses.dataclass(frozen=True, order=True)
class USub(Factor):
    """
        This class has been generated automatically from the bnf rule :
        branch USub := <DASH> <Factor as factor>
    """
    factor: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '-'
        yield str(self.factor)
    
    @classmethod
    def parse(cls, obj: Element) -> USub:
        assert isinstance(obj, Lemma)
        return cls(
            factor=Factor.parse(obj.data['factor'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> USub:
        return cls(factor=Factor.__from_ast__(obj))


@dataclasses.dataclass(frozen=True, order=True)
class Pow(Power):
    """
        This class has been generated automatically from the bnf rule :
        branch Pow := <Primary as left> $' ' <ASTERISK_ASTERISK> $' ' <Factor as right>
    """
    left: Primary
    right: Factor
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '**'
        yield ' '
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> Pow:
        assert isinstance(obj, Lemma)
        return cls(
            left=Primary.parse(obj.data['left']),
            right=Factor.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.BinOp) -> Pow:
        return cls(left=Primary.__from_ast__(obj.left), right=Factor.__from_ast__(obj.right))


@dataclasses.dataclass(frozen=True, order=True)
class Primary(Power, abc.ABC):
    """
        >>> Subscript  # concrete
        >>> GetAttr  # concrete
        >>> Call  # concrete
        >>> IndentedCall  # concrete
        >>> DataGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> Primary:
        if obj.type == 'Subscript':
            return Subscript.parse(obj)
        elif obj.type == 'GetAttr':
            return GetAttr.parse(obj)
        elif obj.type == 'Call':
            return Call.parse(obj)
        elif obj.type == 'IndentedCall':
            return IndentedCall.parse(obj)
        else:
            return DataGR.parse(obj)
    
    def call(self, *args: CallArgumentGR) -> Call:
        return Call(left=self, args=list(args))
    
    def subscript(self, __other: Expression) -> Subscript:
        return Subscript(left=self, right=__other)
    
    def getattr(self, __other: typing.Union[str, Variable]) -> GetAttr:
        if isinstance(__other, str):
            __other = Variable(content=__other)
        return GetAttr(left=self, right=__other)
    
    def __pow__(self, other: Factor) -> Pow:
        return Pow(left=self, right=other)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Primary:
        if isinstance(obj, ast.Subscript):
            return Subscript.from_ast(obj)
        elif isinstance(obj, ast.Attribute):
            return GetAttr.from_ast(obj)
        elif isinstance(obj, ast.Call):
            return Call.from_ast(obj)
        else:
            return DataGR.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Call(Primary, Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Call := <Primary as left> <LEFT_PARENTHESIS> <COMMA> $' '.<CallArgumentGR in args> <RIGHT_PARENTHESIS>
    """
    left: Primary
    args: list[CallArgumentGR]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield '('
        if self.args:
            for i, e in enumerate(self.args):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> Call:
        assert isinstance(obj, Lemma)
        return cls(
            left=Primary.parse(obj.data['left']),
            args=[CallArgumentGR.parse(item) for item in obj.data['args']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Call) -> Call:
        args = []
        for arg in obj.args:
            args.append(CallArgumentGR.__from_ast__(arg))
        for keyword in obj.keywords:
            args.append(CallArgumentGR.__from_ast__(keyword))
        return cls(left=Primary.__from_ast__(obj.func), args=args)


@dataclasses.dataclass(frozen=True, order=True)
class DataGR(Primary, abc.ABC):
    """
        >>> Tuple  # concrete
        >>> GenExp  # concrete
        >>> List  # concrete
        >>> ListComp  # concrete
        >>> Dict  # concrete
        >>> DictComp  # concrete
        >>> Set  # concrete
        >>> SetComp  # concrete
        >>> IndentedList  # concrete
        >>> AtomGR  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> DataGR:
        if obj.type == 'Tuple':
            return Tuple.parse(obj)
        elif obj.type == 'GenExp':
            return GenExp.parse(obj)
        elif obj.type == 'List':
            return List.parse(obj)
        elif obj.type == 'ListComp':
            return ListComp.parse(obj)
        elif obj.type == 'Dict':
            return Dict.parse(obj)
        elif obj.type == 'DictComp':
            return DictComp.parse(obj)
        elif obj.type == 'Set':
            return Set.parse(obj)
        elif obj.type == 'SetComp':
            return SetComp.parse(obj)
        elif obj.type == 'IndentedList':
            return IndentedList.parse(obj)
        else:
            return AtomGR.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> DataGR:
        if isinstance(obj, ast.List):
            return List.from_ast(obj)
        elif isinstance(obj, ast.ListComp):
            return ListComp.from_ast(obj)
        elif isinstance(obj, ast.Dict):
            return Dict.from_ast(obj)
        elif isinstance(obj, ast.DictComp):
            return DictComp.from_ast(obj)
        elif isinstance(obj, ast.Set):
            return Set.from_ast(obj)
        elif isinstance(obj, ast.SetComp):
            return SetComp.from_ast(obj)
        elif isinstance(obj, ast.Tuple):
            return Tuple.from_ast(obj)
        elif isinstance(obj, ast.GeneratorExp):
            return GenExp.from_ast(obj)
        else:
            return AtomGR.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class GetAttr(Primary):
    """
        This class has been generated automatically from the bnf rule :
        branch GetAttr := <Primary as left> <DOT> <Variable as right>
    """
    left: Primary
    right: Variable
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield '.'
        yield str(self.right)
    
    @classmethod
    def parse(cls, obj: Element) -> GetAttr:
        assert isinstance(obj, Lemma)
        return cls(
            left=Primary.parse(obj.data['left']),
            right=Variable.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Attribute) -> GetAttr:
        return cls(left=Primary.__from_ast__(obj.value), right=Variable.from_str(obj.attr))


@dataclasses.dataclass(frozen=True, order=True)
class IndentedCall(Primary):
    """
        This class has been generated automatically from the bnf rule :
        branch IndentedCall := <Primary as left> <LEFT_PARENTHESIS> <IndentedCallBody as body> $'\\n' <RIGHT_PARENTHESI…
    """
    left: Primary
    body: IndentedCallBody
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield '('
        yield str(self.body)
        yield '\n'
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> IndentedCall:
        assert isinstance(obj, Lemma)
        return cls(
            left=Primary.parse(obj.data['left']),
            body=IndentedCallBody.parse(obj.data['body'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class Subscript(Primary):
    """
        This class has been generated automatically from the bnf rule :
        branch Subscript := <Primary as left> <LB> <SliceGR as right> <RB>
    """
    left: Primary
    right: SliceGR
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield '['
        yield str(self.right)
        yield ']'
    
    @classmethod
    def parse(cls, obj: Element) -> Subscript:
        assert isinstance(obj, Lemma)
        return cls(
            left=Primary.parse(obj.data['left']),
            right=SliceGR.parse(obj.data['right'])
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Subscript) -> Subscript:
        return cls(left=Primary.__from_ast__(obj.value), right=SliceGR.__from_ast__(obj.slice))


@dataclasses.dataclass(frozen=True, order=True)
class AtomGR(DataGR, abc.ABC):
    """
        >>> Variable  # atomic
        >>> Constant  # abstract
    """
    @classmethod
    def parse(cls, obj: Element) -> AtomGR:
        if obj.type == 'Variable':
            return Variable.parse(obj)
        else:
            return Constant.parse(obj)
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> AtomGR:
        if isinstance(obj, ast.Name):
            return Variable.from_ast(obj)
        else:
            return Constant.__from_ast__(obj)


@dataclasses.dataclass(frozen=True, order=True)
class Dict(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Dict := <LS> <COMMA> $' '.<DictItem in items> <RS>
    """
    items: list[DictItem]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '{'
        if self.items:
            for i, e in enumerate(self.items):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield '}'
    
    @classmethod
    def parse(cls, obj: Element) -> Dict:
        assert isinstance(obj, Lemma)
        return cls(
            items=[DictItem.parse(item) for item in obj.data['items']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Dict) -> Dict:
        return cls(items=[DictItem.from_ast(key, value) for key, value in zip(obj.keys, obj.values)])


@dataclasses.dataclass(frozen=True, order=True)
class DictComp(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch DictComp := <LS> <DictItem as elt> +<ForIfClause in generators> <RS>
    """
    elt: DictItem
    generators: list[ForIfClause]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '{'
        yield str(self.elt)
        for e in self.generators:
            yield str(e)
        yield '}'
    
    @classmethod
    def parse(cls, obj: Element) -> DictComp:
        assert isinstance(obj, Lemma)
        return cls(
            elt=DictItem.parse(obj.data['elt']),
            generators=[ForIfClause.parse(item) for item in obj.data['generators']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.DictComp) -> DictComp:
        return cls(elt=DictItem.from_ast(obj.key, obj.value), generators=list(map(ForIfClause.from_ast, obj.generators)))


@dataclasses.dataclass(frozen=True, order=True)
class GenExp(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch GenExp := <LEFT_PARENTHESIS> <Expression as elt> +<ForIfClause in generators> <RIGHT_PARENTHESIS>
    """
    elt: Expression
    generators: list[ForIfClause]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        yield str(self.elt)
        for e in self.generators:
            yield str(e)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> GenExp:
        assert isinstance(obj, Lemma)
        return cls(
            elt=Expression.parse(obj.data['elt']),
            generators=[ForIfClause.parse(item) for item in obj.data['generators']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.GeneratorExp) -> GenExp:
        return cls(elt=Expression.__from_ast__(obj.elt), generators=list(map(ForIfClause.from_ast, obj.generators)))


@dataclasses.dataclass(frozen=True, order=True)
class IndentedList(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch IndentedList := <LB> <IndentedExprEnum as body> $'\\n' <RB>
    """
    body: IndentedExprEnum
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '['
        yield str(self.body)
        yield '\n'
        yield ']'
    
    @classmethod
    def parse(cls, obj: Element) -> IndentedList:
        assert isinstance(obj, Lemma)
        return cls(
            body=IndentedExprEnum.parse(obj.data['body'])
        )


@dataclasses.dataclass(frozen=True, order=True)
class List(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch List := <LB> <COMMA> $' '.<Expression in items> <RB>
    """
    items: list[Expression]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '['
        if self.items:
            for i, e in enumerate(self.items):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield ']'
    
    @classmethod
    def parse(cls, obj: Element) -> List:
        assert isinstance(obj, Lemma)
        return cls(
            items=[Expression.parse(item) for item in obj.data['items']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.List) -> List:
        return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@dataclasses.dataclass(frozen=True, order=True)
class ListComp(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch ListComp := <LB> <Expression as elt> +<ForIfClause in generators> <RB>
    """
    elt: Expression
    generators: list[ForIfClause]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '['
        yield str(self.elt)
        for e in self.generators:
            yield str(e)
        yield ']'
    
    @classmethod
    def parse(cls, obj: Element) -> ListComp:
        assert isinstance(obj, Lemma)
        return cls(
            elt=Expression.parse(obj.data['elt']),
            generators=[ForIfClause.parse(item) for item in obj.data['generators']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.ListComp) -> ListComp:
        return cls(elt=Expression.__from_ast__(obj.elt), generators=list(map(ForIfClause.from_ast, obj.generators)))


@dataclasses.dataclass(frozen=True, order=True)
class Set(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Set := <LS> <COMMA> $' '.<Expression in items> <RS>
    """
    items: list[Expression]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '{'
        if self.items:
            for i, e in enumerate(self.items):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield '}'
    
    @classmethod
    def parse(cls, obj: Element) -> Set:
        assert isinstance(obj, Lemma)
        return cls(
            items=[Expression.parse(item) for item in obj.data['items']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Set) -> Set:
        return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@dataclasses.dataclass(frozen=True, order=True)
class SetComp(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch SetComp := <LS> <Expression as elt> +<ForIfClause in generators> <RS>
    """
    elt: Expression
    generators: list[ForIfClause]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '{'
        yield str(self.elt)
        for e in self.generators:
            yield str(e)
        yield '}'
    
    @classmethod
    def parse(cls, obj: Element) -> SetComp:
        assert isinstance(obj, Lemma)
        return cls(
            elt=Expression.parse(obj.data['elt']),
            generators=[ForIfClause.parse(item) for item in obj.data['generators']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.SetComp) -> SetComp:
        return cls(elt=Expression.__from_ast__(obj.elt), generators=list(map(ForIfClause.from_ast, obj.generators)))


@dataclasses.dataclass(frozen=True, order=True)
class Tuple(DataGR):
    """
        This class has been generated automatically from the bnf rule :
        branch Tuple := <LEFT_PARENTHESIS> <COMMA> $' '..<Expression in items> <RIGHT_PARENTHESIS>
    """
    items: list[Expression]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '('
        for i, e in enumerate(self.items):
            if i:
                yield ','
                yield ' '
            yield str(e)
        yield ')'
    
    @classmethod
    def parse(cls, obj: Element) -> Tuple:
        assert isinstance(obj, Lemma)
        return cls(
            items=[Expression.parse(item) for item in obj.data['items']]
        )
    
    @classmethod
    def from_ast(cls, obj: ast.Tuple) -> Tuple:
        return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@dataclasses.dataclass(frozen=True, order=True)
class Constant(AtomGR, abc.ABC):
    """
        >>> NoneClass  # concrete
        >>> TrueClass  # concrete
        >>> FalseClass  # concrete
        >>> EllipsisClass  # concrete
        >>> Integer  # atomic
        >>> Float  # atomic
        >>> String  # atomic
    """
    @classmethod
    def parse(cls, obj: Element) -> Constant:
        if obj.type == 'NoneClass':
            return NoneClass.parse(obj)
        elif obj.type == 'TrueClass':
            return TrueClass.parse(obj)
        elif obj.type == 'FalseClass':
            return FalseClass.parse(obj)
        elif obj.type == 'EllipsisClass':
            return EllipsisClass.parse(obj)
        elif obj.type == 'Integer':
            return Integer.parse(obj)
        elif obj.type == 'Float':
            return Float.parse(obj)
        elif obj.type == 'String':
            return String.parse(obj)
        else:
            raise ValueError(cls.__name__, 'parse', repr(obj.type))
    
    @classmethod
    def from_value(cls, __value: object) -> Constant:
        if __value is None:
            return NONE
        elif __value is False:
            return FALSE
        elif __value is True:
            return TRUE
        elif isinstance(__value, int):
            return Integer(content=repr(__value))
        elif isinstance(__value, float):
            assert str(__value) not in ('inf', 'nan')
            return Float(content=repr(__value))
        elif isinstance(__value, str):
            return String(content=repr(__value))
        else:
            raise TypeError('Unsupported type to convert from.')
    
    @classmethod
    def __from_ast__(cls, obj: ast.expr) -> Constant:
        if isinstance(obj, ast.Constant):
            value = obj.value
            if value is None:
                return NoneClass()
            elif value is True:
                return TrueClass()
            elif value is False:
                return FalseClass()
            elif value is Ellipsis:
                return EllipsisClass()
            elif isinstance(value, int):
                return Integer(content=repr(value))
            elif isinstance(value, str):
                return String(content=repr(value))
            else:
                raise NotImplementedError(ERR_3, obj)
        else:
            raise NotImplementedError(ERR_4, obj)


@dataclasses.dataclass(frozen=True, order=True)
class Variable(AtomGR, StarTargetsGR):
    """
        This class has been generated automatically from the bnf rule :
        regex   Variable '[a-zA-Z]\\w*'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Variable:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    def to_str(self) -> str:
        return self.content
    
    @classmethod
    def from_str(cls, obj: typing.Optional[str]) -> typing.Optional[Variable]:
        if obj is None:
            return None
        return cls(content=obj)
    
    def as_call_arg(self, __value: Expression) -> NamedArgument:
        return NamedArgument(name=self, expr=__value)
    
    def as_def_arg(self, default: typing.Optional[Expression] = None, type_: typing.Optional[Expression] = None) -> DefArgumentGR:
        return Argument(name=self, type=type_, default=default)
    
    @classmethod
    def from_ast(cls, obj: ast.expr) -> Variable:
        if isinstance(obj, ast.Name):
            return cls(content=obj.id)
        else:
            raise NotImplementedError(ERR_7, obj)


@dataclasses.dataclass(frozen=True, order=True)
class EllipsisClass(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch EllipsisClass := <DOT_DOT_DOT>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield '...'
    
    @classmethod
    def parse(cls, obj: Element) -> EllipsisClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class FalseClass(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch FalseClass := <KW_FALSE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'False'
    
    @classmethod
    def parse(cls, obj: Element) -> FalseClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class Float(Constant):
    """
        This class has been generated automatically from the bnf rule :
        regex   Float '\\d+\\.\\d*|\\.\\d+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Float:
        assert isinstance(obj, Token)
        return cls(content=obj.content)


@dataclasses.dataclass(frozen=True, order=True)
class Integer(Constant):
    """
        This class has been generated automatically from the bnf rule :
        regex   Integer '\\d+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> Integer:
        assert isinstance(obj, Token)
        return cls(content=obj.content)


@dataclasses.dataclass(frozen=True, order=True)
class NoneClass(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch NoneClass := <KW_NONE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'None'
    
    @classmethod
    def parse(cls, obj: Element) -> NoneClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )


@dataclasses.dataclass(frozen=True, order=True)
class String(Constant):
    """
        This class has been generated automatically from the bnf rule :
        regex   String '\\"(?:\\"|[^\\"])*?(?<!\\\\\\\\)\\"|\\'(?:\\'|[^\\'])*?(?<!\\\\\\\\)\\''
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    @classmethod
    def parse(cls, obj: Element) -> String:
        assert isinstance(obj, Token)
        return cls(content=obj.content)
    
    def to_str(self) -> str:
        return eval(self.content)
    
    @classmethod
    def sl_docstring(cls, __value: str) -> String:
        return cls(content='"""' + __value + '"""')
    
    @classmethod
    def _i_ml_docstring(cls, __value: str, level: int = 0) -> typing.Iterator[str]:
        if not __value.startswith('\n'):
            yield '\n'
        indent = level * '    '
        for index, line in enumerate(__value.split('\n')):
            if index:
                yield '\n'
            yield indent
            if line and not line.startswith('    '):
                yield '    '
            yield line
        if not __value.endswith('\n'):
            yield '\n'
        yield indent
    
    @classmethod
    def ml_docstring(cls, __value: str, level: int = 0) -> String:
        return cls(content='"""' + ''.join(cls._i_ml_docstring(__value, level)) + '"""')


@dataclasses.dataclass(frozen=True, order=True)
class TrueClass(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch TrueClass := <KW_TRUE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'True'
    
    @classmethod
    def parse(cls, obj: Element) -> TrueClass:
        assert isinstance(obj, Lemma)
        return cls(
            
        )

TRUE = TrueClass()

FALSE = FalseClass()

NONE = NoneClass()

CONTINUE = ContinueClass()

BREAK = BreakClass()

ERR_0 = 'ERR_0'

ERR_1 = 'ERR_1'

ERR_2 = 'ERR_2'

ERR_3 = 'ERR_3'

ERR_4 = 'ERR_4'

ERR_5 = 'ERR_5'

ERR_6 = 'ERR_6'

ERR_7 = 'ERR_7'

ERR_8 = 'ERR_8'

ERR_9 = 'ERR_9'

ERR_10 = 'ERR_10'

ERR_11 = 'ERR_11'
