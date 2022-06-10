from website.langs import javascript as js
from website.language.base.decorators import *
from website.language.generic.lang.models import *


@__method__
def to_js(self: Atom):
    if isinstance(self, Variable):
        return js.Variable(content=self.content)
    elif isinstance(self, Integer):
        return js.Integer(content=self.content)
    elif isinstance(self, String):
        return js.String(content=self.content)
    elif isinstance(self, TrueConstant):
        return js.TrueClass()
    elif isinstance(self, FalseConstant):
        return js.FalseClass()
    elif isinstance(self, NullConstant):
        return js.NullClass()
    else:
        raise NotImplementedError


@__method__
def to_js(self: Primary):
    if isinstance(self, List):
        return js.List(items=[item.to_js() for item in self.items])
    elif isinstance(self, Dict):
        return js.Dict(items=[item.to_js() for item in self.items])
    elif isinstance(self, Call):
        args = js.CallArgs(items=[arg.to_js() for arg in self.args])
        return js.Call(left=self.obj.to_js(), args=args)
    else:
        raise NotImplementedError


@__method__
def to_js(self: Secondary):
    if isinstance(self, Append):
        obj = self.obj.to_js()
        item = self.item.to_js()
        left = js.GetAttr(obj, js.Variable('append'))
        args = js.CallArgs(items=[item])
        return js.Call(left=left, args=args)
    elif isinstance(self, Length):
        obj = self.obj.to_js()
        args = js.CallArgs(items=[obj])
        return js.Call(left=js.Variable('len'), args=args)
    else:
        raise NotImplementedError


@__method__
def to_js(self: Sum):
    if isinstance(self, Mul):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Mul(left=left, right=right)

    elif isinstance(self, Div):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Div(left=left, right=right)

    elif isinstance(self, Add):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Add(left=left, right=right)

    elif isinstance(self, Sub):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Sub(left=left, right=right)

    elif isinstance(self, Eq):
        left = self.left.to_js()
        right = self.right.to_js()
        return js.Eq(left=left, right=right)

    elif isinstance(self, In):
        left = js.GetAttr(left=self.right.to_js(), right=js.Variable("includes"))
        args = js.CallArgs([self.left.to_js()])
        return js.Call(left=left, args=args)

    else:
        raise NotImplementedError


@__method__
def to_js(self: Statement):
    if isinstance(self, Docstring):
        return js.String(content="/* " + eval(self.value.content) + " */")

    elif isinstance(self, Return):
        values = [value.to_js() for value in self.values]
        if len(values) == 0:
            expr = None
        elif len(values) == 1:
            expr = values[0]
        else:
            expr = js.List(items=values)
        return js.Return(right=expr)

    elif isinstance(self, Raise):
        expr = self.value.to_js()
        return js.Throw(right=expr)

    elif isinstance(self, Export):
        items = [name.to_js() for name in self.names]
        return js.Export(items=items)

    else:
        raise NotImplementedError


@__method__
def to_js(self: Argument):
    name = self.name.to_js()
    # type_ = self.type.to_js()
    # default = self.value.to_js()
    return name


@__method__
def to_js(self: UpdateSTMT):
    if isinstance(self, Function):
        name = self.name.to_js()
        args = js.DefArgs(items=[arg.to_js() for arg in self.args])
        block = self.block.to_js()
        return js.Function(name=name, args=args, block=block)

    elif isinstance(self, VariableDef):
        target = self.target.to_js()
        value = self.value.to_js()
        return js.Assign(
            obj=js.Var(model=target),
            right=value
        )

    elif isinstance(self, ConstantDef):
        target = self.target.to_js()
        value = self.value.to_js()
        return js.Assign(
            obj=js.Const(model=target),
            right=value
        )

    elif isinstance(self, Assign):
        targets = [target.to_js() for target in self.targets]
        value = self.value.to_js()
        if len(targets) == 1:
            obj = targets[0]
        else:
            obj = js.VariableList(variables=targets)
        return js.Assign(obj=obj, right=value)

    else:
        raise NotImplementedError


@__method__
def to_js(self: Alt):
    if isinstance(self, Elif):
        condition = self.test.to_js()
        block = self.block.to_js()
        alt = self.alt.to_js() if self.alt else None
        return js.ElseIf(condition=condition, block=block, alt=alt)

    elif isinstance(self, Else):
        return js.Else(block=self.block.to_js())

    else:
        raise NotImplementedError


@__method__
def to_js(self: Block):
    statements = [statement.to_js() for statement in self.statements]
    return js.Block(statements=statements)


@__method__
def to_js(self: Except):
    name = self.name.to_js()
    error = self.type.to_js()
    right = js.InstanceOf(left=name, right=error)
    block = self.block.to_js()
    return js.Catch(name=name, right=right, block=block)


@__method__
def to_js(self: ControlSTMT):
    if isinstance(self, If):
        condition = self.test.to_js()
        block = self.block.to_js()
        alt = self.alt.to_js() if self.alt else None
        return js.If(condition=condition, block=block, alt=alt)

    elif isinstance(self, For):
        raise NotImplementedError  # TODO

    elif isinstance(self, Enum):
        if self.index:
            raise NotImplementedError  # TODO
        else:
            target = self.item.to_js()
            iterator = self.iterable.to_js()
            block = self.block.to_js()
            key = js.Let(model=target)
            return js.ForOf(key=key, right=iterator, block=block)

    elif isinstance(self, While):
        condition = self.test.to_js()
        block = self.block.to_js()
        return js.While(condition=condition, block=block)

    elif isinstance(self, Try):
        block = self.block.to_js()
        excepts = [except_.to_js() for except_ in self.excepts]
        return js.Try(block=block, catches=excepts)

    else:
        raise NotImplementedError


@__method__
def to_js(self: KeyPair):
    if isinstance(self, (VarKeyPair, StrKeyPair)):
        key = self.key.to_js()
        value = self.value.to_js()
        return js.DictItem(key=key, right=value)

    else:
        raise NotImplementedError


@__method__
def to_js(self: Module):
    statements = [statement.to_js() for statement in self.statements]
    return js.Module(statements=statements)


# noinspection PyUnusedLocal
@__method__
def to_js(self: Code):
    raise NotImplementedError
