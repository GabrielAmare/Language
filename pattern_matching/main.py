from pattern_matching import *


def main():
    def match(__type: str) -> AtomPattern:
        return AtomPattern(
            function=Element.is_typed_as(__type),
        )

    def match_as(__type: str, __key: str) -> AtomPattern:
        return AtomPattern(
            function=Element.is_typed_as(__type),
            action=Context.set_as_for(__key)
        )

    def match_in(__type: str, __key: str) -> AtomPattern:
        return AtomPattern(
            function=Element.is_typed_as(__type),
            action=Context.add_in_for(__key)
        )

    # for example the pattern X *Y Z will be represented by :
    pattern = sequence([match('X'), repeat(match_in('Y', 'ys')), match_as('Z', 'z'), optional(match_as('T', 't'))])

    tokens = [
        Token(type='X', content='1'),
        Token(type='Y', content='2'),
        Token(type='Y', content='3'),
        Token(type='Y', content='4'),
        Token(type='Z', content='5'),
        # Token(type='T', content='6'),
    ]

    index, res = pattern.match(0, tokens)

    context = Context()

    res.apply(context)

    print(context.data)


if __name__ == '__main__':
    main()
