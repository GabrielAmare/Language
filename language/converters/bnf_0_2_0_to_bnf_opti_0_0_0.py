"""
Converter module that allows to convert any `bnf@0.2.0` object into its corresponding `bnf_opti@0.0.0` object.
"""
import language.base.bnf.v0_2_0 as origin
import language.base.bnf_opti.v0_0_0 as target

__all__ = [
    'convert',
]

from language.base.bnf import BuildToken, BuildLemma, BuildGroup, Engine


class _Converter(origin.AbstractGRVisitor):
    def _engine(self, obj: Engine):
        # WARNING : `obj.entry` is lost during conversion !
        return target.Lexicon(definitions=tuple(
            self(rule)
            for rule in obj.rules
        ))
    
    def _build_group(self, obj: BuildGroup):
        return target.Definition(
            name=obj.type,
            rule=target.parallel(*[
                target.Reference(name=ref)
                for ref in obj.refs
            ])
        )
    
    def _build_lemma(self, obj: BuildLemma):
        return target.Definition(
            name=obj.type,
            rule=target.sequence(*[
                self(obj.rule),
                target.BuildLemma(type=obj.type),
            ])
        )
    
    def _build_token(self, obj: BuildToken):
        return target.Definition(
            name=obj.type,
            rule=target.sequence(*[
                self(obj.rule),
                target.BuildToken(type=obj.type),
            ])
        )
    
    def _parallel(self, obj: origin.Parallel):
        # problem while using the `target.parallel` factory because it uses a set injected into a tuple.
        return target.Parallel(rules=tuple(map(self, obj.rules)))
    
    def _sequence(self, obj: origin.Sequence):
        return target.sequence(*map(self, obj.rules))
    
    def _enum0(self, obj: origin.Enum0):
        separator = self(obj.separator)
        item = self(obj.item)
        return target.sequence(item, target.repeat_0(target.sequence(separator, item)))
    
    def _enum1(self, obj: origin.Enum1):
        separator = self(obj.separator)
        item = self(obj.item)
        return target.sequence(item, target.repeat_1(target.sequence(separator, item)))
    
    def _optional(self, obj: origin.Optional):
        return target.optional(self(obj.rule))
    
    def _repeat0(self, obj: origin.Repeat0):
        rule = self(obj.rule)
        return target.repeat_0(rule)
    
    def _repeat1(self, obj: origin.Repeat1):
        rule = self(obj.rule)
        return target.repeat_1(rule)
    
    def _grouping(self, obj: origin.Grouping):
        return self(obj.rule)
    
    def _canonical(self, obj: origin.Canonical):
        return target.EMPTY
    
    def _literal(self, obj: origin.Literal):
        return target.sequence(*[
            target.IncludeChar(chars=repr(char), inverted=False)
            for char in eval(obj.expr)
        ])
    
    def _literal_if(self, obj: origin.LiteralIf):
        return target.sequence(
            *[target.IncludeChar(chars=repr(char)) for char in eval(obj.expr)],
            target.BuildToken('__bool__'),
            target.Store(obj.key)
        )
    
    def _match(self, obj: origin.Match):
        return target.Match(chars=obj.charset, inverted=obj.inverted)
    
    def _store(self, obj: origin.Store):
        return target.sequence(*[
            target.Reference(name=obj.type),
            target.Store(key=obj.key),
        ])


convert = _Converter()
