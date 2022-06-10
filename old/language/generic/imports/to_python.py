from website.language import python as py
from website.language.base.decorators import *
from website.language.generic.lang.models import *


@__method__
def to_py(self: Atom):
    if isinstance(self, Variable):
        return py.Variable(content=self.content)
    elif isinstance(self, Integer):
        return py.Integer(content=self.content)
    elif isinstance(self, String):
        return py.String(content=self.content)
    elif isinstance(self, TrueConstant):
        return py.TrueClass()
    elif isinstance(self, FalseConstant):
        return py.FalseClass()
    elif isinstance(self, NullConstant):
        return py.NoneClass()
    else:
        raise NotImplementedError


@__method__
def to_py(self: Primary):
    if isinstance(self, List):
        return py.List(items=[item.to_py() for item in self.items])
    elif isinstance(self, Dict):
        return py.Dict(items=[item.to_py() for item in self.items])
    elif isinstance(self, Call):
        return py.Call(left=self.obj.to_py(), args=[arg.to_py() for arg in self.args])
    else:
        raise NotImplementedError


@__method__
def to_py(self: Secondary):
    if isinstance(self, Append):
        obj = self.obj.to_py()
        item = self.item.to_py()
        return py.Call(left=py.GetAttr(obj, py.Variable('append')), args=[item])
    elif isinstance(self, Length):
        obj = self.obj.to_py()
        return py.Call(left=py.Variable('len'), args=[obj])
    else:
        raise NotImplementedError


@__method__
def to_py(self: Sum):
    if isinstance(self, Mul):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Mul(left=left, right=right)

    elif isinstance(self, Div):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.TrueDiv(left=left, right=right)

    elif isinstance(self, Add):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Add(left=left, right=right)

    elif isinstance(self, Sub):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Sub(left=left, right=right)

    elif isinstance(self, Eq):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.Eq(left=left, right=right)

    elif isinstance(self, In):
        left = self.left.to_py()
        right = self.right.to_py()
        return py.In(left=left, right=right)

    else:
        raise NotImplementedError


@__method__
def to_py(self: Statement):
    if isinstance(self, Docstring):
        return py.StatementExpr(expr=py.String.ml_docstring(eval(self.value.content)))

    elif isinstance(self, Return):
        values = [value.to_py() for value in self.values]
        if len(values) == 0:
            expr = None
        elif len(values) == 1:
            expr = values[0]
        else:
            expr = py.ExprEnum(items=values)
        return py.Return(expr=expr)

    elif isinstance(self, Raise):
        expr = self.value.to_py()
        return py.Raise(expr=expr, cause=None)

    elif isinstance(self, Export):
        target = py.Variable('__all__')
        value = py.List([py.String(content=repr(name.content)) for name in self.names])
        return py.AnnAssign(target=target, annotation=None, value=value)

    else:
        raise NotImplementedError


@__method__
def to_py(self: Argument):
    name = self.name.to_py()
    type_ = self.type.to_py()
    default = self.value.to_py()
    return py.Argument(name=name, type=type_, default=default)


@__method__
def to_py(self: UpdateSTMT):
    if isinstance(self, Function):
        name = self.name.to_py()
        args = [arg.to_py() for arg in self.args]
        block = self.block.to_py()
        return py.Def(decorators=[], name=name, args=args, rtype=None, block=block)

    elif isinstance(self, (VariableDef, ConstantDef)):
        target = self.target.to_py()
        annotation = self.type.to_py() if self.type else None
        value = self.value.to_py()
        return py.AnnAssign(target=target, annotation=annotation, value=value)

    elif isinstance(self, Assign):
        targets = [target.to_py() for target in self.targets]
        value = self.value.to_py()
        if len(targets) == 1:
            return py.AnnAssign(target=targets[0], annotation=None, value=value)
        else:
            return py.AssignTuple(args=targets, value=value)

    else:
        raise NotImplementedError


@__method__
def to_py(self: Alt):
    if isinstance(self, Elif):
        condition = self.test.to_py()
        block = self.block.to_py()
        alt = self.alt.to_py() if self.alt else None
        return py.Elif(condition=condition, block=block, alt=alt)

    elif isinstance(self, Else):
        return py.Else(block=self.block.to_py())

    else:
        raise NotImplementedError


@__method__
def to_py(self: Block):
    statements = [statement.to_py() for statement in self.statements]
    return py.Block(statements=statements)


@__method__
def to_py(self: Except):
    name = self.name.to_py()
    error = self.type.to_py()
    block = self.block.to_py()
    return py.Except(error=error, block=block, as_=name)


@__method__
def to_py(self: ControlSTMT):
    if isinstance(self, If):
        condition = self.test.to_py()
        block = self.block.to_py()
        alt = self.alt.to_py() if self.alt else None
        return py.If(condition=condition, block=block, alt=alt)

    elif isinstance(self, For):
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

    elif isinstance(self, Enum):
        if self.index:
            target = py.ExprEnum(items=[self.index.to_py(), self.item.to_py()])
            iterator = py.Call(left=py.Variable('enumerate'), args=self.iterable.to_py())
        else:
            target = self.item.to_py()
            iterator = self.iterable.to_py()

        block = self.block.to_py()
        return py.For(target=target, iterator=iterator, block=block, alt=None)

    elif isinstance(self, While):
        condition = self.test.to_py()
        block = self.block.to_py()
        return py.While(condition=condition, block=block, alt=None)

    elif isinstance(self, Try):
        block = self.block.to_py()
        excepts = [except_.to_py() for except_ in self.excepts]
        return py.Try(block=block, excepts=excepts)

    else:
        raise NotImplementedError


@__method__
def to_py(self: KeyPair):
    if isinstance(self, StrKeyPair):
        key = self.key.to_py()
        value = self.value.to_py()
        return py.DictItem(key=key, value=value)

    elif isinstance(self, VarKeyPair):
        key = py.String(content=repr(self.key.content))
        value = self.value.to_py()
        return py.DictItem(key=key, value=value)

    else:
        raise NotImplementedError


@__method__
def to_py(self: Module):
    statements = [statement.to_py() for statement in self.statements]
    return py.Module(statements=statements)


# noinspection PyUnusedLocal
@__method__
def to_py(self: Code):
    raise NotImplementedError
