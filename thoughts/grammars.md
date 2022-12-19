# Types of grammars

## Generalities & Definitions

In this document we talk about some code generation processes. To not get lost in the subject we will define some terms
with a strict meaning :

- `Language` : A set of sentences that can be interpreted.
- `Sentence` : Generally a sequence of symbols that are meaningful in a `Language`.
- `Comprehension` : A structured representation of a `Sentence` in a given `Language`.
    - Abstract Syntax Tree (`AST`) : A tree structure representing a sentence, using the different descriptors of a
      language.
    - Concrete Syntax Tree (`CST`) : Generally and extension of an AST that include some real behaviour (i.e. : If our
      language allow us to define maths formulas, the CST could have methods to evaluate said formulas).
- `Grammar` : A set of rules defining a language, describe each token, lemma, and other objects of the language.
- `Parser` : A process/function that is based on a grammar, it takes a sentence written in its language and transforms
  it
  into a comprehension (AST/CST).
- `Models` : A class hierarchy representing the different structures of a `Language`.
- `<...>Generator` : As we will talk about code generation, it is important to discriminate correctly some objects and
  the processes used to generate this objects. (i.e. : Grammar / GrammarGenerator, Parser ParserGenerator)

## Properties

### Issues with top-bottom approach

- `Left recursion` : the left-recursion in a grammar is when a rule has a reference to itself as a first symbol.
    - `Direct Left Recursion` : a left-recursion where the symbol is explicitly referring to itself.
    - `Indirect Left Recursion` : a left-recursion where the symbol is implicitly referring to itself.

### About ambiguity

- `Formal` : a formal grammar is mostly a grammar that doesn't allow ambiguity.
- `Natural` : a natural grammar is mostly a grammar that allow ambiguity (a same sentence can have multiple AST).

## Parsing

- `Order dependant` : when a `Parser-Generator` can generate a `Parser` that works differently depending on the order of
  the rules in the given `Grammar`.

### Some processes

```
ParserGenerator: Grammar -> Parser
ModelsGenerator: Grammar -> Models
Parser: Sentence -> Comprehension
```