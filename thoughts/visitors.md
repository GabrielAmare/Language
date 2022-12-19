# Types of visitors

## Definition

    The visitor pattern is a way to separate an operation that you want to perform on the elements of an object
    structure from the structure itself. It allows you to add new operations to existing objects without changing their
    classes.
    
    In the visitor pattern, you define a separate visitor class that implements the operation you want to perform.
    Then, you define an accept method in each element of the object structure that takes a visitor as an argument. The
    accept method calls the appropriate method on the visitor, passing itself as an argument. The visitor then performs
    the operation on the element.
    
    By using the visitor pattern, you can add new operations to the object structure without changing the classes of the
    elements themselves. This makes it easier to add new features and maintain the codebase over time.

## Different implementations, pros and cons

    In the following section we'll be using the set of classes below as an example.

```
class Term(abc.ABC):
    pass


@dataclasses.dataclass
class Mul(Term):
    left: Term
    right: Atom


@dataclasses.dataclass
class Div(Term):
    left: Term
    right: Atom


class Atom(Term, abc.ABC):
    pass


@dataclasses.dataclass
class Variable(Atom, abc.ABC):
    name: str


@dataclasses.dataclass
class Integer(Atom, abc.ABC):
    value: int
```

### Abstract Method Visitor

```
class Term(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, context: dict) -> object:
        pass


@dataclasses.dataclass
class Mul(Term):
    left: Term
    right: Atom
    
    def evaluate(self, context: dict) -> object:
        return self.left.evaluate(context) * self.right.evaluate(context)


@dataclasses.dataclass
class Div(Term):
    left: Term
    right: Atom
    
    def evaluate(self, context: dict) -> object:
        return self.left.evaluate(context) / self.right.evaluate(context)


class Atom(Term, abc.ABC):
    pass


@dataclasses.dataclass
class Variable(Atom, abc.ABC):
    name: str
    
    def evaluate(self, context: dict) -> object:
        return context[self.name]


@dataclasses.dataclass
class Integer(Atom, abc.ABC):
    value: int
    
    def evaluate(self, context: dict) -> object:
        return self.value
```

<TABLE>
<TR>
<TD>PROS</TD>
<TD>CONS</TD>
</TR>
<TR>
<TD>
- By looking at a class definition we can see how a certain process should apply on it.
</TD>
<TD>
- When there are a lot of classes it's hard to overview a specific process behaviour over the full class set.
</TD>
</TR>
</TABLE>

### Simple Function Visitor

```
def evaluate(self: Term, context: dict) -> object:
    if isinstance(self, Mul):
        return self.left.evaluate(context) * self.right.evaluate(context)
    elif isinstance(self, Div):
        return self.left.evaluate(context) / self.right.evaluate(context)
    elif isinstance(self, Variable):
        return context[self.name]
    elif isinstance(self, Integer):
        return self.value
    else:
        raise NotImplementedError

```

<TABLE>
<TR>
<TD>PROS</TD>
<TD>CONS</TD>
</TR>
<TR>
<TD>
- Decouple the process from the class set.<BR>
- It's easy to have an overview of what the process is doing for each class of the set.
</TD>
<TD>
- To use the process you'd have to import the process separately from the class set.<BR>
- This process has a default non-implemented case.<BR>
- Process return type hint cannot be specified by the `self` argument type.<BR>
- It's not possible to specify the process (use the base implementation but modify its behaviour in some cases).
</TD>
</TR>
</TABLE>

### Abstract Class Visitor

```

class AbstractVisitor(abc.ABC):
    def __call__(self, obj: Term)
        if isinstance(obj, Mul):
            return self._on_mul(obj)
        elif isinstance(obj, Div):
            return self._on_div(obj)
        elif isinstance(obj, Variable):
            return self._on_variable(obj)
        elif isinstance(obj, Integer):
            return self._on_integer(obj)
        else:
            raise NotImplementedError
    
    @abc.abstractmethod
    def _on_mul(self, obj: Mul):
        pass
    
    @abc.abstractmethod
    def _on_div(self, obj: Div):
        pass
    
    @abc.abstractmethod
    def _on_variable(self, obj: Variable):
        pass
    
    @abc.abstractmethod
    def _on_integer(self, obj: Integer):
        pass
    
@dataclasses.dataclass
class Evaluate(AbstractVisitor):
    context: dict
    
    @abc.abstractmethod
    def _on_mul(self, obj: Mul) -> object:
        return obj.left.evaluate(context) * obj.right.evaluate(context)
    
    @abc.abstractmethod
    def _on_div(self, obj: Div) -> object:
        return obj.left.evaluate(context) / obj.right.evaluate(context)
    
    @abc.abstractmethod
    def _on_variable(self, obj: Variable) -> object:
        return context[obj.name]
    
    @abc.abstractmethod
    def _on_integer(self, obj: Integer) -> int:
        return obj.value

def evaluate(self: Term, context: dict) -> object:
    return Evaluate(context)(self)

```

<TABLE>
<TR>
<TD>PROS</TD>
<TD>CONS</TD>
</TR>
<TR>
<TD>
- Once the abstract visitor is created, multiple other visitors can be implemented easily.<BR>
- All the visitors inheriting from the abstract one share the same interface, which is useful in some cases.<BR>
- When the class set is updated, we only have to update the visitor abstract class, and it will prevent other visitors
to run if they don't get updated accordingly. This can be useful when the class set changes frequently and there are
multiple visitors for which it is important to handle all the classes of the class set.
- You can easily pass global params to the visitor (i.e. `context`) instead of passing them recursively to each call.
</TD>
<TD>
- Requires to create an abstract visitor class before creating the real visitor.<BR>
- It is more complex to call a visitor as it requires to create an instance of the class before using it.
</TD>
</TR>
</TABLE>

### Other ideas of implementation

- Using the `functools.singledispatch` or `functools.singledispatchmethod` to discriminate the classes instead of an
  if/elif/else structure.