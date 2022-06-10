"""
    This module has been auto-generated. Do not change manually.
    WARNING : Manual changes to this file are likely to be overwritten.
"""
from __future__ import annotations

import abc
import dataclasses
import typing

from website.langs import javascript as js
from website.language import python as py

__all__ = [
    'Add',
    'Alt',
    'Append',
    'Argument',
    'Assign',
    'Atom',
    'Block',
    'Call',
    'Code',
    'Comparison',
    'Constant',
    'ConstantDef',
    'ControlSTMT',
    'Dict',
    'Div',
    'Docstring',
    'Elif',
    'Else',
    'Enum',
    'Eq',
    'Except',
    'Export',
    'Expression',
    'FALSE',
    'FalseConstant',
    'For',
    'Function',
    'If',
    'In',
    'Integer',
    'KeyPair',
    'Length',
    'List',
    'Module',
    'Mul',
    'NULL',
    'NullConstant',
    'Primary',
    'Raise',
    'Return',
    'Secondary',
    'Statement',
    'StrKeyPair',
    'String',
    'Sub',
    'Sum',
    'TRUE',
    'Term',
    'TrueConstant',
    'Try',
    'UpdateSTMT',
    'VarKeyPair',
    'Variable',
    'VariableDef',
    'While'
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
class Alt(abc.ABC):
    """
        >>> Elif  # concrete
        >>> Else  # concrete
    """
    block: Block
    
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Argument:
    """
        This class has been generated automatically from the bnf rule :
        branch Argument := <Variable as name> ?<COLON> $' ' <Expression as type> ?[$' ' <EQ> $' ' <Expression as value>]
    """
    name: Variable
    type: Expression | None = None
    value: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.name)
        if self.type:
            yield ':'
            yield ' '
            yield str(self.type)
        if self.value:
            yield ' '
            yield '='
            yield ' '
            yield str(self.value)
    
    def to_py(self):
        name = self.name.to_py()
        type_ = self.type.to_py()
        default = self.value.to_py()
        return py.Argument(name=name, type=type_, default=default)
    
    def to_js(self):
        name = self.name.to_js()
        return name


@dataclasses.dataclass(frozen=True, order=True)
class Atom(abc.ABC):
    """
        >>> Variable  # atomic
        >>> Constant  # abstract
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Block:
    """
        This class has been generated automatically from the bnf rule :
        branch Block '    ' := *[<NEWLINE> <Statement in statements>]
    """
    statements: list[Statement] | None = None
    
    @_indented('    ')
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.statements:
            for e in self.statements:
                yield '\n'
                yield str(e)
    
    def to_py(self):
        statements = [statement.to_py() for statement in self.statements]
        return py.Block(statements=statements)
    
    def to_js(self):
        statements = [statement.to_js() for statement in self.statements]
        return js.Block(statements=statements)


@dataclasses.dataclass(frozen=True, order=True)
class Call:
    """
        This class has been generated automatically from the bnf rule :
        branch Call := <Primary as obj> <LEFT_PARENTHESIS> <COMMA> $' '.<Expression in args> <RIGHT_PARENTHESIS>
    """
    obj: Primary
    args: list[Expression]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.obj)
        yield '('
        if self.args:
            for i, e in enumerate(self.args):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield ')'
    
    def to_py(self):
        return py.Call(left=self.obj.to_py(), args=[arg.to_py() for arg in self.args])
    
    def to_js(self):
        args = js.CallArgs(items=[arg.to_js() for arg in self.args])
        return js.Call(left=self.obj.to_js(), args=args)


@dataclasses.dataclass(frozen=True, order=True)
class Code(abc.ABC):
    """
        >>> Module  # concrete
        >>> Statement  # abstract
        >>> Expression  # abstract
    """
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Except:
    """
        This class has been generated automatically from the bnf rule :
        branch Except := <KW_EXCEPT> $' ' <LEFT_PARENTHESIS> <Variable as name> <COLON> $' ' <Expression as type> <RIGH…
    """
    name: Variable
    type: Expression
    block: Block
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'except'
        yield ' '
        yield '('
        yield str(self.name)
        yield ':'
        yield ' '
        yield str(self.type)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    def to_py(self):
        name = self.name.to_py()
        error = self.type.to_py()
        block = self.block.to_py()
        return py.Except(error=error, block=block, as_=name)
    
    def to_js(self):
        name = self.name.to_js()
        error = self.type.to_js()
        right = js.InstanceOf(left=name, right=error)
        block = self.block.to_js()
        return js.Catch(name=name, right=right, block=block)


@dataclasses.dataclass(frozen=True, order=True)
class KeyPair(abc.ABC):
    """
        >>> VarKeyPair  # concrete
        >>> StrKeyPair  # concrete
    """
    value: Expression
    
    @abc.abstractmethod
    def __str__(self) -> typing.Iterator[str]:
        pass
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Elif(Alt):
    """
        This class has been generated automatically from the bnf rule :
        branch Elif := $' ' <KW_ELIF> $' ' <LEFT_PARENTHESIS> <Expression as test> <RIGHT_PARENTHESIS> $' ' <LS> <Block…
    """
    test: Expression
    alt: Alt
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield ' '
        yield 'elif'
        yield ' '
        yield '('
        yield str(self.test)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
        yield str(self.alt)
    
    def to_py(self):
        condition = self.test.to_py()
        block = self.block.to_py()
        alt = self.alt.to_py() if self.alt else None
        return py.Elif(condition=condition, block=block, alt=alt)
    
    def to_js(self):
        condition = self.test.to_js()
        block = self.block.to_js()
        alt = self.alt.to_js() if self.alt else None
        return js.ElseIf(condition=condition, block=block, alt=alt)


@dataclasses.dataclass(frozen=True, order=True)
class Else(Alt):
    """
        This class has been generated automatically from the bnf rule :
        branch Else := $' ' <KW_ELSE> $' ' <LS> <Block as block> <NEWLINE> <RS>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield ' '
        yield 'else'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    def to_py(self):
        return py.Else(block=self.block.to_py())
    
    def to_js(self):
        return js.Else(block=self.block.to_js())


@dataclasses.dataclass(frozen=True, order=True)
class Expression(Code, abc.ABC):
    """
        >>> Comparison  # abstract
    """


@dataclasses.dataclass(frozen=True, order=True)
class Module(Code):
    """
        This class has been generated automatically from the bnf rule :
        branch Module := <NEWLINE>.<Statement in statements>
    """
    statements: list[Statement]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        if self.statements:
            for i, e in enumerate(self.statements):
                if i:
                    yield '\n'
                yield str(e)
    
    def to_py(self):
        statements = [statement.to_py() for statement in self.statements]
        return py.Module(statements=statements)
    
    def to_js(self):
        statements = [statement.to_js() for statement in self.statements]
        return js.Module(statements=statements)


@dataclasses.dataclass(frozen=True, order=True)
class Statement(Code, abc.ABC):
    """
        >>> Docstring  # concrete
        >>> Return  # concrete
        >>> Raise  # concrete
        >>> Export  # concrete
        >>> UpdateSTMT  # abstract
    """
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class StrKeyPair(KeyPair):
    """
        This class has been generated automatically from the bnf rule :
        branch StrKeyPair := <String as key> <COLON> $' ' <Expression as value>
    """
    key: String
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.key)
        yield ':'
        yield ' '
        yield str(self.value)
    
    def to_py(self):
        key = self.key.to_py()
        value = self.value.to_py()
        return py.DictItem(key=key, value=value)
    
    def to_js(self):
        key = self.key.to_js()
        value = self.value.to_js()
        return js.DictItem(key=key, right=value)


@dataclasses.dataclass(frozen=True, order=True)
class VarKeyPair(KeyPair):
    """
        This class has been generated automatically from the bnf rule :
        branch VarKeyPair := <Variable as key> <COLON> $' ' <Expression as value>
    """
    key: Variable
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.key)
        yield ':'
        yield ' '
        yield str(self.value)
    
    def to_py(self):
        key = py.String(content=repr(self.key.content))
        value = self.value.to_py()
        return py.DictItem(key=key, value=value)
    
    def to_js(self):
        key = self.key.to_js()
        value = self.value.to_js()
        return js.DictItem(key=key, right=value)


@dataclasses.dataclass(frozen=True, order=True)
class Variable(Atom):
    """
        This class has been generated automatically from the bnf rule :
        regex   Variable '[a-zA-Z_]\\w*'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    def to_py(self):
        return py.Variable(content=self.content)
    
    def to_js(self):
        return js.Variable(content=self.content)


@dataclasses.dataclass(frozen=True, order=True)
class Comparison(Expression, abc.ABC):
    """
        >>> Eq  # concrete
        >>> In  # concrete
        >>> Sum  # abstract
    """


@dataclasses.dataclass(frozen=True, order=True)
class Docstring(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Docstring := <KW_DOC> <String as value>
    """
    value: String
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'doc'
        yield str(self.value)
    
    def to_py(self):
        return py.StatementExpr(expr=py.String.ml_docstring(eval(self.value.content)))
    
    def to_js(self):
        return js.String(content='/* ' + eval(self.value.content) + ' */')


@dataclasses.dataclass(frozen=True, order=True)
class Export(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Export := <KW_EXPORT> $' ' <COMMA> $' '.<Variable in names>
    """
    names: list[Variable]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'export'
        yield ' '
        if self.names:
            for i, e in enumerate(self.names):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
    
    def to_py(self):
        target = py.Variable('__all__')
        value = py.List([py.String(content=repr(name.content)) for name in self.names])
        return py.AnnAssign(target=target, annotation=None, value=value)
    
    def to_js(self):
        items = [name.to_js() for name in self.names]
        return js.Export(items=items)


@dataclasses.dataclass(frozen=True, order=True)
class Raise(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Raise := <KW_RAISE> $' ' <Expression as value>
    """
    value: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'raise'
        yield ' '
        yield str(self.value)
    
    def to_py(self):
        expr = self.value.to_py()
        return py.Raise(expr=expr, cause=None)
    
    def to_js(self):
        expr = self.value.to_js()
        return js.Throw(right=expr)


@dataclasses.dataclass(frozen=True, order=True)
class Return(Statement):
    """
        This class has been generated automatically from the bnf rule :
        branch Return := <KW_RETURN> ?[$' ' <COMMA> $' '.<Expression in values>]
    """
    values: list[Expression] | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'return'
        if self.values:
            yield ' '
            if self.values:
                for i, e in enumerate(self.values):
                    if i:
                        yield ','
                        yield ' '
                    yield str(e)
    
    def to_py(self):
        values = [value.to_py() for value in self.values]
        if len(values) == 0:
            expr = None
        elif len(values) == 1:
            expr = values[0]
        else:
            expr = py.ExprEnum(items=values)
        return py.Return(expr=expr)
    
    def to_js(self):
        values = [value.to_js() for value in self.values]
        if len(values) == 0:
            expr = None
        elif len(values) == 1:
            expr = values[0]
        else:
            expr = js.List(items=values)
        return js.Return(right=expr)


@dataclasses.dataclass(frozen=True, order=True)
class UpdateSTMT(Statement, abc.ABC):
    """
        >>> Function  # concrete
        >>> VariableDef  # concrete
        >>> ConstantDef  # concrete
        >>> Assign  # concrete
        >>> ControlSTMT  # abstract
    """
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Assign(UpdateSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch Assign := <KW_SET> <COMMA> $' '.<Primary in targets> $' ' <EQ> $' ' <Expression as value>
    """
    targets: list[Primary]
    value: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'set'
        if self.targets:
            for i, e in enumerate(self.targets):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield ' '
        yield '='
        yield ' '
        yield str(self.value)
    
    def to_py(self):
        targets = [target.to_py() for target in self.targets]
        value = self.value.to_py()
        if len(targets) == 1:
            return py.AnnAssign(target=targets[0], annotation=None, value=value)
        else:
            return py.AssignTuple(args=targets, value=value)
    
    def to_js(self):
        targets = [target.to_js() for target in self.targets]
        value = self.value.to_js()
        if len(targets) == 1:
            obj = targets[0]
        else:
            obj = js.VariableList(variables=targets)
        return js.Assign(obj=obj, right=value)


@dataclasses.dataclass(frozen=True, order=True)
class ConstantDef(UpdateSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch ConstantDef := <KW_CON> $' ' <Variable as target> ?<COLON> $' ' <Expression as type> $' ' <EQ> $' ' <Exp…
    """
    target: Variable
    value: Expression
    type: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'con'
        yield ' '
        yield str(self.target)
        if self.type:
            yield ':'
            yield ' '
            yield str(self.type)
        yield ' '
        yield '='
        yield ' '
        yield str(self.value)
    
    def to_py(self):
        target = self.target.to_py()
        annotation = self.type.to_py() if self.type else None
        value = self.value.to_py()
        return py.AnnAssign(target=target, annotation=annotation, value=value)
    
    def to_js(self):
        target = self.target.to_js()
        value = self.value.to_js()
        return js.Assign(obj=js.Const(model=target), right=value)


@dataclasses.dataclass(frozen=True, order=True)
class ControlSTMT(UpdateSTMT, abc.ABC):
    """
        >>> If  # concrete
        >>> For  # concrete
        >>> Enum  # concrete
        >>> While  # concrete
        >>> Try  # concrete
    """
    block: Block
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Eq(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch Eq := <Sum as left> $' ' <EQ_EQ> $' ' <Sum as right>
    """
    left: Sum
    right: Sum
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '=='
        yield ' '
        yield str(self.right)
    
    def to_py(self):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Eq(left=left, right=right)
    
    def to_js(self):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Eq(left=left, right=right)


@dataclasses.dataclass(frozen=True, order=True)
class Function(UpdateSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch Function := <KW_FUN> $' ' <Variable as name> <LEFT_PARENTHESIS> <COMMA> $' '.<Argument in args> <RIGHT_P…
    """
    name: Variable
    args: list[Argument]
    block: Block
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'fun'
        yield ' '
        yield str(self.name)
        yield '('
        if self.args:
            for i, e in enumerate(self.args):
                if i:
                    yield ','
                    yield ' '
                yield str(e)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    def to_py(self):
        name = self.name.to_py()
        args = [arg.to_py() for arg in self.args]
        block = self.block.to_py()
        return py.Def(decorators=[], name=name, args=args, rtype=None, block=block)
    
    def to_js(self):
        name = self.name.to_js()
        args = js.DefArgs(items=[arg.to_js() for arg in self.args])
        block = self.block.to_js()
        return js.Function(name=name, args=args, block=block)


@dataclasses.dataclass(frozen=True, order=True)
class In(Comparison):
    """
        This class has been generated automatically from the bnf rule :
        branch In := <Sum as left> $' ' <KW_IN> $' ' <Sum as right>
    """
    left: Sum
    right: Sum
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.right)
    
    def to_py(self):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.In(left=left, right=right)
    
    def to_js(self):
        left = js.GetAttr(left=self.right.to_js(), right=js.Variable('includes'))
        args = js.CallArgs([self.left.to_js()])
        return js.Call(left=left, args=args)


@dataclasses.dataclass(frozen=True, order=True)
class Sum(Comparison, abc.ABC):
    """
        >>> Add  # concrete
        >>> Sub  # concrete
        >>> Term  # abstract
    """
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class VariableDef(UpdateSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch VariableDef := <KW_VAR> $' ' <Variable as target> ?<COLON> $' ' <Expression as type> $' ' <EQ> $' ' <Exp…
    """
    target: Variable
    value: Expression
    type: Expression | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'var'
        yield ' '
        yield str(self.target)
        if self.type:
            yield ':'
            yield ' '
            yield str(self.type)
        yield ' '
        yield '='
        yield ' '
        yield str(self.value)
    
    def to_py(self):
        target = self.target.to_py()
        annotation = self.type.to_py() if self.type else None
        value = self.value.to_py()
        return py.AnnAssign(target=target, annotation=annotation, value=value)
    
    def to_js(self):
        target = self.target.to_js()
        value = self.value.to_js()
        return js.Assign(obj=js.Var(model=target), right=value)


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
    
    def to_py(self):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Add(left=left, right=right)
    
    def to_js(self):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Add(left=left, right=right)


@dataclasses.dataclass(frozen=True, order=True)
class Enum(ControlSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch Enum := <KW_ENUM> $' ' <LEFT_PARENTHESIS> <Variable as item> ?[<COMMA> $' ' <Variable as index>] $' ' <K…
    """
    item: Variable
    iterable: Expression
    index: Variable | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'enum'
        yield ' '
        yield '('
        yield str(self.item)
        if self.index:
            yield ','
            yield ' '
            yield str(self.index)
        yield ' '
        yield 'in'
        yield ' '
        yield str(self.iterable)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    def to_py(self):
        if self.index:
            target = py.ExprEnum(items=[self.index.to_py(), self.item.to_py()])
            iterator = py.Call(left=py.Variable('enumerate'), args=self.iterable.to_py())
        else:
            target = self.item.to_py()
            iterator = self.iterable.to_py()
        block = self.block.to_py()
        return py.For(target=target, iterator=iterator, block=block, alt=None)
    
    def to_js(self):
        if self.index:
            raise NotImplementedError
        else:
            target = self.item.to_js()
            iterator = self.iterable.to_js()
            block = self.block.to_js()
            key = js.Let(model=target)
            return js.ForOf(key=key, right=iterator, block=block)


@dataclasses.dataclass(frozen=True, order=True)
class For(ControlSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch For := <KW_FOR> $' ' <LEFT_PARENTHESIS> <Variable as index> ?$' ' <KW_FROM> $' ' <Integer as start> $' '…
    """
    index: Variable
    end: Integer
    start: Integer | None = None
    step: Integer | None = None
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'for'
        yield ' '
        yield '('
        yield str(self.index)
        if self.start:
            yield ' '
            yield 'from'
            yield ' '
            yield str(self.start)
        yield ' '
        yield 'to'
        yield ' '
        yield str(self.end)
        if self.step:
            yield ' '
            yield 'by'
            yield ' '
            yield str(self.step)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    def to_py(self):
        args = []
        if self.start:
            args.append(self.start.to_py())
        args.append(self.end.to_py())
        if self.step:
            args.append(self.step.to_py())
        target = self.index.to_py()
        iterator = py.Call(left=py.Variable('range'), args=args)
        block = self.block.to_py()
        return py.For(target=target, iterator=iterator, block=block, alt=None)
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class If(ControlSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch If := <KW_IF> $' ' <LEFT_PARENTHESIS> <Expression as test> <RIGHT_PARENTHESIS> $' ' <LS> <Block as block…
    """
    test: Expression
    alt: Alt
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'if'
        yield ' '
        yield '('
        yield str(self.test)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
        yield str(self.alt)
    
    def to_py(self):
        condition = self.test.to_py()
        block = self.block.to_py()
        alt = self.alt.to_py() if self.alt else None
        return py.If(condition=condition, block=block, alt=alt)
    
    def to_js(self):
        condition = self.test.to_js()
        block = self.block.to_js()
        alt = self.alt.to_js() if self.alt else None
        return js.If(condition=condition, block=block, alt=alt)


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
    
    def to_py(self):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Sub(left=left, right=right)
    
    def to_js(self):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Sub(left=left, right=right)


@dataclasses.dataclass(frozen=True, order=True)
class Term(Sum, abc.ABC):
    """
        >>> Mul  # concrete
        >>> Div  # concrete
        >>> Secondary  # abstract
    """


@dataclasses.dataclass(frozen=True, order=True)
class Try(ControlSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch Try := <KW_TRY> $' ' <LS> <Block as block> <NEWLINE> <RS> +<Except in excepts>
    """
    excepts: list[Except]
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'try'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
        for e in self.excepts:
            yield str(e)
    
    def to_py(self):
        block = self.block.to_py()
        excepts = [except_.to_py() for except_ in self.excepts]
        return py.Try(block=block, excepts=excepts)
    
    def to_js(self):
        block = self.block.to_js()
        excepts = [except_.to_js() for except_ in self.excepts]
        return js.Try(block=block, catches=excepts)


@dataclasses.dataclass(frozen=True, order=True)
class While(ControlSTMT):
    """
        This class has been generated automatically from the bnf rule :
        branch While := <KW_WHILE> $' ' <LEFT_PARENTHESIS> <Expression as test> <RIGHT_PARENTHESIS> $' ' <LS> <Block as…
    """
    test: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'while'
        yield ' '
        yield '('
        yield str(self.test)
        yield ')'
        yield ' '
        yield '{'
        yield str(self.block)
        yield '\n'
        yield '}'
    
    def to_py(self):
        condition = self.test.to_py()
        block = self.block.to_py()
        return py.While(condition=condition, block=block, alt=None)
    
    def to_js(self):
        condition = self.test.to_js()
        block = self.block.to_js()
        return js.While(condition=condition, block=block)


@dataclasses.dataclass(frozen=True, order=True)
class Div(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch Div := <Term as left> $' ' <SLASH> $' ' <Secondary as right>
    """
    left: Term
    right: Secondary
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '/'
        yield ' '
        yield str(self.right)
    
    def to_py(self):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.TrueDiv(left=left, right=right)
    
    def to_js(self):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Div(left=left, right=right)


@dataclasses.dataclass(frozen=True, order=True)
class Mul(Term):
    """
        This class has been generated automatically from the bnf rule :
        branch Mul := <Term as left> $' ' <ASTERISK> $' ' <Secondary as right>
    """
    left: Term
    right: Secondary
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.left)
        yield ' '
        yield '*'
        yield ' '
        yield str(self.right)
    
    def to_py(self):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Mul(left=left, right=right)
    
    def to_js(self):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Mul(left=left, right=right)


@dataclasses.dataclass(frozen=True, order=True)
class Secondary(Term, abc.ABC):
    """
        >>> Append  # concrete
        >>> Length  # concrete
        >>> Primary  # abstract
    """
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Append(Secondary):
    """
        This class has been generated automatically from the bnf rule :
        branch Append := <Primary as obj> <DOT> <KW_APPEND> <LEFT_PARENTHESIS> <Expression as item> <RIGHT_PARENTHESIS>
    """
    obj: Primary
    item: Expression
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.obj)
        yield '.'
        yield 'append'
        yield '('
        yield str(self.item)
        yield ')'
    
    def to_py(self):
        obj = self.obj.to_py()
        item = self.item.to_py()
        return py.Call(left=py.GetAttr(obj, py.Variable('append')), args=[item])
    
    def to_js(self):
        obj = self.obj.to_js()
        item = self.item.to_js()
        left = js.GetAttr(obj, js.Variable('append'))
        args = js.CallArgs(items=[item])
        return js.Call(left=left, args=args)


@dataclasses.dataclass(frozen=True, order=True)
class Length(Secondary):
    """
        This class has been generated automatically from the bnf rule :
        branch Length := <Primary as obj> <DOT> <KW_LENGTH> <LEFT_PARENTHESIS> <RIGHT_PARENTHESIS>
    """
    obj: Primary
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield str(self.obj)
        yield '.'
        yield 'length'
        yield '('
        yield ')'
    
    def to_py(self):
        obj = self.obj.to_py()
        return py.Call(left=py.Variable('len'), args=[obj])
    
    def to_js(self):
        obj = self.obj.to_js()
        args = js.CallArgs(items=[obj])
        return js.Call(left=js.Variable('len'), args=args)


@dataclasses.dataclass(frozen=True, order=True)
class Primary(Secondary, abc.ABC):
    """
        >>> List  # concrete
        >>> Dict  # concrete
        >>> Constant  # abstract
    """
    
    @abc.abstractmethod
    def to_py(self):
        pass
    
    @abc.abstractmethod
    def to_js(self):
        pass


@dataclasses.dataclass(frozen=True, order=True)
class Constant(Atom, Primary, abc.ABC):
    """
        >>> Integer  # atomic
        >>> String  # atomic
        >>> TrueConstant  # concrete
        >>> FalseConstant  # concrete
        >>> NullConstant  # concrete
    """


@dataclasses.dataclass(frozen=True, order=True)
class Dict(Primary):
    """
        This class has been generated automatically from the bnf rule :
        branch Dict := <LS> <COMMA> $' '.<KeyPair in items> <RS>
    """
    items: list[KeyPair]
    
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
    
    def to_py(self):
        return py.Dict(items=[item.to_py() for item in self.items])
    
    def to_js(self):
        return js.Dict(items=[item.to_js() for item in self.items])


@dataclasses.dataclass(frozen=True, order=True)
class List(Primary):
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
    
    def to_py(self):
        return py.List(items=[item.to_py() for item in self.items])
    
    def to_js(self):
        return js.List(items=[item.to_js() for item in self.items])


@dataclasses.dataclass(frozen=True, order=True)
class FalseConstant(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch FalseConstant := <KW_FALSE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'false'
    
    def to_py(self):
        return py.FalseClass()
    
    def to_js(self):
        return js.FalseClass()


@dataclasses.dataclass(frozen=True, order=True)
class Integer(Constant):
    """
        This class has been generated automatically from the bnf rule :
        regex   Integer '\\-?\\d+'
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    def to_py(self):
        return py.Integer(content=self.content)
    
    def to_js(self):
        return js.Integer(content=self.content)


@dataclasses.dataclass(frozen=True, order=True)
class NullConstant(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch NullConstant := <KW_NULL>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'null'
    
    def to_py(self):
        return py.NoneClass()
    
    def to_js(self):
        return js.NullClass()


@dataclasses.dataclass(frozen=True, order=True)
class String(Constant):
    """
        This class has been generated automatically from the bnf rule :
        regex   String '\\".*?\\"|\\'.*?\\''
    """
    content: str
    
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield self.content
    
    def to_py(self):
        return py.String(content=self.content)
    
    def to_js(self):
        return js.String(content=self.content)


@dataclasses.dataclass(frozen=True, order=True)
class TrueConstant(Constant):
    """
        This class has been generated automatically from the bnf rule :
        branch TrueConstant := <KW_TRUE>
    """
    @_flat_str
    def __str__(self) -> typing.Iterator[str]:
        yield 'true'
    
    def to_py(self):
        return py.TrueClass()
    
    def to_js(self):
        return js.TrueClass()

TRUE = TrueConstant()

FALSE = FalseConstant()

NULL = NullConstant()
