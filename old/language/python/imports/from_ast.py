import ast
import itertools
import typing

from website.language.base.decorators import *
from website.language.python import *

ERR_0 = "ERR_0"
ERR_1 = "ERR_1"
ERR_2 = "ERR_2"
ERR_3 = "ERR_3"
ERR_4 = "ERR_4"
ERR_5 = "ERR_5"
ERR_6 = "ERR_6"
ERR_7 = "ERR_7"
ERR_8 = "ERR_8"
ERR_9 = "ERR_9"
ERR_10 = "ERR_10"
ERR_11 = "ERR_11"


########################################################################################################################
# UTILS
########################################################################################################################

# noinspection PyUnusedLocal
@__class_method__
def from_ast_list(cls: DefArgumentGR.__class__, obj: ast.arguments) -> list[DefArgumentGR]:
    result = []

    for arg, default in reversed(
            list(itertools.zip_longest(reversed(obj.args), reversed(obj.defaults), fillvalue=None))):
        result.append(Argument.from_ast(arg, default))

    if obj.vararg:
        arg = Argument.from_ast(obj.vararg)
        result.append(NonKeywordArgument(name=arg.name, type=arg.type))

    if obj.kwarg:
        arg = Argument.from_ast(obj.kwarg)
        result.append(KeywordArgument(name=arg.name, type=arg.type))

    return result


# noinspection PyUnusedLocal
@__class_method__
def from_ast_slice(cls: ExprEnum.__class__, obj: typing.Union[ast.expr, ast.slice]):
    if isinstance(obj, ast.expr):
        return Expression.__from_ast__(obj)

    elif isinstance(obj, ast.Index):  # TODO : generalize to handle `ast.slice`
        return Returnable.__from_ast__(obj.value)

    else:
        NotImplementedError(obj)


########################################################################################################################
# GROUPS
########################################################################################################################


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Expression.__class__, obj: ast.expr) -> Expression:
    # IfExp | LambdaDef | Disjunction
    if isinstance(obj, ast.IfExp):
        return IfExp.from_ast(obj)

    elif isinstance(obj, ast.Lambda):
        raise NotImplementedError(ERR_0, obj)

    else:
        return Disjunction.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: SliceGR.__class__, obj: typing.Union[ast.Slice, ast.expr]) -> typing.Union[SliceGR, ExprEnum]:
    if isinstance(obj, ast.Slice):
        if isinstance(obj, ast.Slice):
            return Slice.from_ast(obj)

        elif isinstance(obj, ast.Index):  # deprecated
            if isinstance(obj.value, ast.Tuple):
                return ExprEnum(items=list(map(Expression.__from_ast__, obj.value.elts)))

            else:
                return Expression.__from_ast__(obj.value)

        elif isinstance(obj, ast.ExtSlice):  # deprecated
            raise NotImplementedError(ERR_1, obj)

        else:
            raise NotImplementedError(ERR_2, obj)

    elif isinstance(obj, ast.Tuple):
        return ExprEnum(items=list(map(Expression.__from_ast__, obj.elts)))

    else:
        return Expression.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Disjunction.__class__, obj: ast.expr) -> Disjunction:
    if isinstance(obj, ast.BoolOp):
        if isinstance(obj.op, ast.Or):
            return Or.from_ast(obj)

    return Conjunction.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Conjunction.__class__, obj: ast.expr) -> Conjunction:
    if isinstance(obj, ast.BoolOp):
        if isinstance(obj.op, ast.And):
            return And.from_ast(obj)

    return Inversion.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Inversion.__class__, obj: ast.expr) -> Inversion:
    if isinstance(obj, ast.UnaryOp):
        if isinstance(obj.op, ast.Not):
            return Not.from_ast(obj.operand)

    return Comparison.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Comparison.__class__, obj: ast.expr) -> Comparison:
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

            left = factory(
                left=left,
                right=BitwiseOrGR.__from_ast__(comparator)
            )

        return left

    else:
        return BitwiseOrGR.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: BitwiseOrGR.__class__, obj: ast.expr) -> BitwiseOrGR:
    if isinstance(obj, ast.BinOp):
        if isinstance(obj.op, ast.BitOr):
            return BitwiseOr.from_ast(obj)
    return BitwiseXorGR.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: BitwiseXorGR.__class__, obj: ast.expr) -> BitwiseXorGR:
    if isinstance(obj, ast.BinOp):
        if isinstance(obj.op, ast.BitXor):
            return BitwiseXor.from_ast(obj)
    return BitwiseAndGR.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: BitwiseAndGR.__class__, obj: ast.expr) -> BitwiseAndGR:
    if isinstance(obj, ast.BinOp):
        if isinstance(obj.op, ast.BitAnd):
            return BitwiseAnd.from_ast(obj)
    return ShiftExpr.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: ShiftExpr.__class__, obj: ast.expr) -> ShiftExpr:
    # TODO : handle LShift
    # TODO : handle RShift
    return Sum.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Sum.__class__, obj: ast.expr) -> Sum:
    if isinstance(obj, ast.BinOp):
        if isinstance(obj.op, ast.Add):
            return Add.from_ast(obj)

        elif isinstance(obj.op, ast.Sub):
            return Sub.from_ast(obj)

    return Term.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Term.__class__, obj: ast.expr) -> Term:
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


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Factor.__class__, obj: ast.expr) -> Factor:
    if isinstance(obj, ast.UnaryOp):
        if isinstance(obj.op, ast.UAdd):
            return UAdd.from_ast(obj.operand)

        elif isinstance(obj.op, ast.USub):
            return USub.from_ast(obj.operand)

        elif isinstance(obj.op, ast.Invert):
            return Invert.from_ast(obj.operand)

    return Power.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Power.__class__, obj: ast.expr) -> Factor:
    if isinstance(obj, ast.BinOp):
        if isinstance(obj.op, ast.Pow):
            return Pow.from_ast(obj)

    return Primary.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Primary.__class__, obj: ast.expr) -> Primary:
    if isinstance(obj, ast.Subscript):
        return Subscript.from_ast(obj)

    elif isinstance(obj, ast.Attribute):
        return GetAttr.from_ast(obj)

    elif isinstance(obj, ast.Call):
        return Call.from_ast(obj)

    else:
        return DataGR.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: DataGR.__class__, obj: ast.expr) -> DataGR:
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


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: AtomGR.__class__, obj: ast.expr) -> AtomGR:
    if isinstance(obj, ast.Name):
        return Variable.from_ast(obj)

    else:
        return Constant.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: StarTargetsGR.__class__, obj: ast.expr) -> StarTargetsGR:
    if isinstance(obj, ast.Tuple):
        return StarTargets.from_ast(obj)

    else:
        return Variable.from_ast(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Constant.__class__, obj: ast.expr) -> Constant:
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


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Statement.__class__, obj: ast.stmt) -> Statement:
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
        raise NotImplementedError(ERR_5, obj)  # cls.__name__ + ".from_ast")


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: ElseGR.__class__, statements: list[ast.stmt]) -> ElseGR:
    if len(statements) == 1:
        statement = statements[0]
        if isinstance(statement, ast.If):
            return Elif.from_ast(statement)

    return Else.from_ast(statements)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: Returnable.__class__, obj: ast.expr) -> Returnable:
    if isinstance(obj, ast.Tuple):
        return ExprEnum.from_ast(obj)

    else:
        return Expression.__from_ast__(obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: AugAssign.__class__, obj: ast.AugAssign) -> AugAssign:
    if isinstance(obj.op, ast.Add):
        return IAdd.from_ast(obj)

    elif isinstance(obj.op, ast.Sub):
        return ISub.from_ast(obj)

    else:
        raise NotImplementedError(ERR_6, obj)


# noinspection PyUnusedLocal
@__class_method__
def __from_ast__(cls: CallArgumentGR.__class__, obj: typing.Union[ast.expr, ast.keyword]) -> CallArgumentGR:
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


########################################################################################################################
# FOR CLASSES from_ast
########################################################################################################################

@__class_method__
def from_ast(cls: Block.__class__, statements: list[ast.stmt]) -> Block:
    return Block(
        statements=list(map(Statement.__from_ast__, statements))
    )


@__class_method__
def from_ast(cls: Except.__class__, obj: ast.ExceptHandler) -> Except:
    return cls(
        error=Expression.__from_ast__(obj.type),
        as_=Variable.from_str(obj.name) if obj.name else None,
        block=Block.from_ast(obj.body)
    )


@__class_method__
def from_ast(cls: Try.__class__, obj: ast.Try) -> Try:
    # TODO : handle obj.orelse (Else)
    # TODO : handle obj.finalbody (Finally)
    return cls(
        block=Block.from_ast(obj.body),
        excepts=list(map(Except.from_ast, obj.handlers)) if obj.handlers else None
    )


@__class_method__
def from_ast(cls: Variable.__class__, obj: ast.expr) -> Variable:
    if isinstance(obj, ast.Name):
        return cls(content=obj.id)

    else:
        raise NotImplementedError(ERR_7, obj)


@__class_method__
def from_ast(cls: GetAttr.__class__, obj: ast.Attribute) -> GetAttr:
    return cls(
        left=Primary.__from_ast__(obj.value),
        right=Variable.from_str(obj.attr)
    )


@__class_method__
def from_ast(cls: Slice.__class__, obj: ast.Slice) -> Slice:
    return cls(
        lower=Expression.__from_ast__(obj.lower),
        upper=Expression.__from_ast__(obj.upper) if obj.upper else None,
        step=Expression.__from_ast__(obj.step) if obj.step else None
    )


@__class_method__
def from_ast(cls: Subscript.__class__, obj: ast.Subscript) -> Subscript:
    return cls(
        left=Primary.__from_ast__(obj.value),
        right=SliceGR.__from_ast__(obj.slice)
    )


@__class_method__
def from_ast(cls: SSArgument.__class__, obj: ast.expr) -> SSArgument:
    return cls(expr=Expression.__from_ast__(obj))


@__class_method__
def from_ast(cls: Call.__class__, obj: ast.Call) -> Call:
    args = []
    for arg in obj.args:
        args.append(CallArgumentGR.__from_ast__(arg))

    for keyword in obj.keywords:
        args.append(CallArgumentGR.__from_ast__(keyword))

    return cls(
        left=Primary.__from_ast__(obj.func),
        args=args
    )


@__class_method__
def from_ast(cls: Or.__class__, obj: ast.BoolOp) -> Or:
    values = list(map(Conjunction.__from_ast__, obj.values))

    left = values[0]
    rights = values[1:]
    for right in rights:
        left = cls(left=left, right=right)

    return left


@__class_method__
def from_ast(cls: And.__class__, obj: ast.BoolOp) -> And:
    values = list(map(Inversion.__from_ast__, obj.values))

    left = values[0]
    rights = values[1:]
    for right in rights:
        left = cls(left=left, right=right)

    return left


@__class_method__
def from_ast(cls: Not.__class__, obj: ast.expr) -> Not:
    return cls(
        right=Inversion.__from_ast__(obj)
    )


@__class_method__
def from_ast(cls: BitwiseOr.__class__, obj: ast.BinOp) -> BitwiseOr:
    return cls(
        left=BitwiseOrGR.__from_ast__(obj.left),
        right=BitwiseXorGR.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: BitwiseXor.__class__, obj: ast.BinOp) -> BitwiseXor:
    return cls(
        left=BitwiseXorGR.__from_ast__(obj.left),
        right=BitwiseAndGR.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: BitwiseAnd.__class__, obj: ast.BinOp) -> BitwiseAnd:
    return cls(
        left=BitwiseAndGR.__from_ast__(obj.left),
        right=ShiftExpr.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: Add.__class__, obj: ast.BinOp) -> Add:
    return cls(
        left=Sum.__from_ast__(obj.left),
        right=Term.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: Sub.__class__, obj: ast.BinOp) -> Sub:
    return cls(
        left=Sum.__from_ast__(obj.left),
        right=Term.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: Mul.__class__, obj: ast.BinOp) -> Mul:
    return cls(
        left=Term.__from_ast__(obj.left),
        right=Factor.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: TrueDiv.__class__, obj: ast.BinOp) -> TrueDiv:
    return cls(
        left=Term.__from_ast__(obj.left),
        right=Factor.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: FloorDiv.__class__, obj: ast.BinOp) -> FloorDiv:
    return cls(
        left=Term.__from_ast__(obj.left),
        right=Factor.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: MatMul.__class__, obj: ast.BinOp) -> MatMul:
    return cls(
        left=Term.__from_ast__(obj.left),
        right=Factor.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: Mod.__class__, obj: ast.BinOp) -> Mod:
    return cls(
        left=Term.__from_ast__(obj.left),
        right=Factor.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: UAdd.__class__, obj: ast.expr) -> UAdd:
    return cls(
        factor=Factor.__from_ast__(obj)
    )


@__class_method__
def from_ast(cls: USub.__class__, obj: ast.expr) -> USub:
    return cls(
        factor=Factor.__from_ast__(obj)
    )


@__class_method__
def from_ast(cls: Invert.__class__, obj: ast.expr) -> Invert:
    return cls(
        factor=Factor.__from_ast__(obj)
    )


@__class_method__
def from_ast(cls: Pow.__class__, obj: ast.BinOp) -> Pow:
    return cls(
        left=Primary.__from_ast__(obj.left),
        right=Factor.__from_ast__(obj.right)
    )


@__class_method__
def from_ast(cls: List.__class__, obj: ast.List) -> List:
    return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@__class_method__
def from_ast(cls: Tuple.__class__, obj: ast.Tuple) -> Tuple:
    return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@__class_method__
def from_ast(cls: Set.__class__, obj: ast.Set) -> Set:
    return cls(items=list(map(Expression.__from_ast__, obj.elts)))


@__class_method__
def from_ast(cls: DictItem.__class__, key: ast.expr, value: ast.expr) -> DictItem:
    return cls(
        key=Expression.__from_ast__(key),
        value=Expression.__from_ast__(value)
    )


@__class_method__
def from_ast(cls: Dict.__class__, obj: ast.Dict) -> Dict:
    return cls(items=[DictItem.from_ast(key, value) for key, value in zip(obj.keys, obj.values)])


@__class_method__
def from_ast(cls: StarTargets.__class__, obj: ast.Tuple) -> StarTargets:
    return cls(elts=list(map(Variable.from_ast, obj.elts)))


@__class_method__
def from_ast(cls: ForIfClause.__class__, obj: ast.comprehension) -> ForIfClause:
    return cls(
        target=StarTargetsGR.__from_ast__(obj.target),
        iter=Disjunction.__from_ast__(obj.iter),
        ifs=list(map(Disjunction.__from_ast__, obj.ifs)) if obj.ifs else None
    )


@__class_method__
def from_ast(cls: ListComp.__class__, obj: ast.ListComp) -> ListComp:
    return cls(
        elt=Expression.__from_ast__(obj.elt),
        generators=list(map(ForIfClause.from_ast, obj.generators))
    )


@__class_method__
def from_ast(cls: SetComp.__class__, obj: ast.SetComp) -> SetComp:
    return cls(
        elt=Expression.__from_ast__(obj.elt),
        generators=list(map(ForIfClause.from_ast, obj.generators))
    )


@__class_method__
def from_ast(cls: GenExp.__class__, obj: ast.GeneratorExp) -> GenExp:
    return cls(
        elt=Expression.__from_ast__(obj.elt),
        generators=list(map(ForIfClause.from_ast, obj.generators))
    )


@__class_method__
def from_ast(cls: DictComp.__class__, obj: ast.DictComp) -> DictComp:
    return cls(
        elt=DictItem.from_ast(obj.key, obj.value),
        generators=list(map(ForIfClause.from_ast, obj.generators))
    )


@__class_method__
def from_ast(cls: IfExp.__class__, obj: ast.IfExp) -> IfExp:
    return cls(
        body=Disjunction.__from_ast__(obj.body),
        test=Disjunction.__from_ast__(obj.test),
        or_else=Disjunction.__from_ast__(obj.orelse)
    )


# TODO : expression

@__class_method__
def from_ast(cls: If.__class__, obj: ast.If) -> If:
    return cls(
        condition=Expression.__from_ast__(obj.test),
        block=Block.from_ast(obj.body),
        alt=ElseGR.__from_ast__(obj.orelse) if obj.orelse else None
    )


@__class_method__
def from_ast(cls: Elif.__class__, obj: ast.If) -> Elif:
    return cls(
        condition=Expression.__from_ast__(obj.test),
        block=Block.from_ast(obj.body),
        alt=ElseGR.__from_ast__(obj.orelse) if obj.orelse else None
    )


@__class_method__
def from_ast(cls: Else.__class__, statements: list[ast.stmt]) -> Else:
    return cls(
        block=Block.from_ast(statements)
    )


@__class_method__
def from_ast(cls: Args.__class__, obj: ast.expr) -> Args:
    if isinstance(obj, ast.Tuple):
        return cls(variables=list(map(Variable.from_ast, obj.elts)))

    elif isinstance(obj, ast.Name):
        return cls(variables=[Variable.from_ast(obj)])

    else:
        raise NotImplementedError(ERR_8, obj)


@__class_method__
def from_ast(cls: For.__class__, obj: ast.For) -> For:
    return cls(
        target=StarTargetsGR.__from_ast__(obj.target),
        iterator=Expression.__from_ast__(obj.iter),
        block=Block.from_ast(obj.body),
        alt=Else.from_ast(obj.orelse) if obj.orelse else None
    )


@__class_method__
def from_ast(cls: While.__class__, obj: ast.While) -> While:
    return cls(
        condition=Expression.__from_ast__(obj.test),
        block=Block.from_ast(obj.body),
        alt=Else.from_ast(obj.orelse) if obj.orelse else None
    )


@__class_method__
def from_ast(cls: WithItem.__class__, obj: ast.withitem) -> WithItem:
    return cls(
        context_expr=Expression.__from_ast__(obj.context_expr),
        optional_vars=Expression.__from_ast__(obj.optional_vars)
    )


@__class_method__
def from_ast(cls: With.__class__, obj: ast.With) -> With:
    return cls(
        items=list(map(WithItem.from_ast, obj.items)),
        block=Block.from_ast(obj.body),
        type_comment=Comment.from_str(obj.type_comment)
    )


@__class_method__
def from_ast(cls: StatementExpr.__class__, obj: ast.Expr) -> typing.Union[StatementExpr, Yield, YieldFrom]:
    """expression as statement"""
    # TODO : this is irregular, Yield & YieldFrom should be considered StatementExpr
    if isinstance(obj.value, ast.Yield):
        return Yield.from_ast(obj.value)

    elif isinstance(obj.value, ast.YieldFrom):
        return YieldFrom.from_ast(obj.value)

    else:
        return cls(
            expr=Expression.__from_ast__(obj.value)
        )


@__class_method__
def from_ast(cls: Yield.__class__, obj: ast.Yield) -> Yield:
    return cls(
        expr=Returnable.__from_ast__(obj.value) if obj.value else None
    )


@__class_method__
def from_ast(cls: YieldFrom.__class__, obj: ast.YieldFrom) -> YieldFrom:
    return cls(
        expr=Returnable.__from_ast__(obj.value) if obj.value else None
    )


@__class_method__
def from_ast(cls: DottedAsName.__class__, obj: ast.alias) -> DottedAsName:
    return DottedAsName(
        names=list(map(Variable, obj.name.split('.'))),
        as_name=obj.asname
    )


@__class_method__
def from_ast(cls: Import.__class__, obj: ast.Import) -> Import:
    return cls(targets=list(map(DottedAsName.from_ast, obj.names)))


@__class_method__
def from_ast(cls: AnnAssign.__class__, obj: typing.Union[ast.Assign, ast.AnnAssign]) -> AnnAssign:
    if isinstance(obj, ast.Assign):
        if len(obj.targets) == 1:
            return cls(
                target=Returnable.__from_ast__(obj.targets[0]),
                annotation=None,
                value=Expression.__from_ast__(obj.value)
            )
        else:
            raise NotImplementedError(ERR_9, obj)

    elif isinstance(obj, ast.AnnAssign):
        return cls(
            target=Primary.__from_ast__(obj.target),
            annotation=Expression.__from_ast__(obj.annotation),
            value=Expression.__from_ast__(obj.value) if obj.value else None
        )

    else:
        raise NotImplementedError(ERR_10, obj)


@__class_method__
def from_ast(cls: IAdd.__class__, obj: ast.AugAssign) -> IAdd:
    return cls(
        obj=Primary.__from_ast__(obj.target),
        expr=Expression.__from_ast__(obj.value)
    )


@__class_method__
def from_ast(cls: ISub.__class__, obj: ast.AugAssign) -> ISub:
    return cls(
        obj=Primary.__from_ast__(obj.target),
        expr=Expression.__from_ast__(obj.value)
    )


@__class_method__
def from_ast(cls: ImportFrom.__class__, obj: ast.ImportFrom) -> ImportFrom:
    if obj.module.startswith('.'):
        raise NotImplementedError(ERR_11, obj)

    variables = []
    for name in obj.module.split('.'):
        variables.append(Variable(content=name))

    if len(obj.names) == 1 and obj.names[0].name == '*' and obj.names[0].asname is None:
        targets = ImportAll()
    else:
        targets = ImportAliases(names=list(map(Alias.from_ast, obj.names)))

    return cls(
        path=AbsoluteImportPath(variables=variables),
        targets=targets
    )


@__class_method__
def from_ast(cls: Return.__class__, obj: ast.Return) -> Return:
    return cls(
        expr=Returnable.__from_ast__(obj.value)
    )


@__class_method__
def from_ast(cls: Raise.__class__, obj: ast.Raise) -> Raise:
    return cls(
        expr=Expression.__from_ast__(obj.exc),
        cause=Expression.__from_ast__(obj.cause) if obj.cause else None
    )


@__class_method__
def from_ast(cls: Assert.__class__, obj: ast.Assert) -> Assert:
    return cls(
        test=Expression.__from_ast__(obj.test),
        msg=Expression.__from_ast__(obj.msg) if obj.msg else None
    )


@__class_method__
def from_ast(cls: PassClass.__class__, _: ast.Pass) -> PassClass:
    return cls()


@__class_method__
def from_ast(cls: ContinueClass.__class__, _: ast.Continue) -> ContinueClass:
    return cls()


@__class_method__
def from_ast(cls: BreakClass.__class__, _: ast.Break) -> BreakClass:
    return cls()


@__class_method__
def from_ast(cls: Module.__class__, obj: ast.Module) -> Module:
    return cls(
        statements=list(map(Statement.__from_ast__, obj.body))
    )


@__class_method__
def from_ast(cls: Alias.__class__, obj: ast.alias) -> Alias:
    return cls(
        name=Variable.from_str(obj.name),
        as_name=Variable.from_str(obj.asname) if obj.asname else None
    )


@__class_method__
def from_ast(cls: Argument.__class__, obj: ast.arg, default=None) -> Argument:
    return cls(
        name=Variable.from_str(obj.arg),
        type=Expression.__from_ast__(obj.annotation) if obj.annotation else None,
        default=None if default is None else Expression.__from_ast__(default)
    )


@__class_method__
def from_ast(cls: NamedArgument.__class__, obj: ast.keyword) -> NamedArgument:
    return cls(
        name=Variable.from_str(obj.arg),
        expr=Expression.__from_ast__(obj.value)
    )


@__class_method__
def from_ast(cls: Decorator.__class__, obj: ast.expr) -> Decorator:
    return cls(
        expr=Expression.__from_ast__(obj)
    )


@__class_method__
def from_ast(cls: Def.__class__, obj: ast.FunctionDef) -> Def:
    return cls(
        decorators=list(map(Decorator.from_ast, obj.decorator_list)) if obj.decorator_list else None,
        name=Variable(obj.name),
        args=DefArgumentGR.from_ast_list(obj.args),
        block=Block(statements=list(map(Statement.__from_ast__, obj.body))),
        rtype=Expression.__from_ast__(obj.returns) if obj.returns else None
    )


@__class_method__
def from_ast(cls: Class.__class__, obj: ast.ClassDef) -> Class:
    bases = Args(variables=list(map(Variable.from_ast, obj.bases))) if obj.bases else None
    return cls(
        decorators=list(map(Decorator.from_ast, obj.decorator_list)) if obj.decorator_list else None,
        name=Variable(obj.name),
        mro=bases,
        block=Block(statements=list(map(Statement.__from_ast__, obj.body)))
    )


@__class_method__
def from_ast(cls: ExprEnum.__class__, obj: ast.Tuple) -> ExprEnum:
    return cls(
        items=list(map(Expression.__from_ast__, obj.elts))
    )


@__class_method__
def from_text(cls: Module.__class__, src: str) -> Module:
    """Parse the `src` text to the corresponding `Module` object."""
    obj = ast.parse(source=src)
    return cls.from_ast(obj)


@__class_method__
def from_file(cls: Module.__class__, __fp: str) -> Module:
    """Parse the `__fp` source module to the corresponding `Module` object."""
    with open(__fp, mode="r", encoding="utf-8") as file:
        src = file.read()

    return cls.from_text(src)
