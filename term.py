from functools import reduce


class Term:

    def __init__(self, symbol, *sub_terms):
        self._symbol = symbol
        if len(sub_terms) != 0:
            self._sub_terms = sub_terms

    def __eq__(self, other):
        return self._symbol == other._symbol

    def __hash__(self):
        return hash(self._symbol)

    def is_variable(self):
        pass

    def variables(self):
        pass

    def __len__(self):
        pass


class Variable(Term):

    def contains(self, variable):
        if not isinstance(variable, Variable):
            raise TypeError('a term.Variable is required')
        return self._symbol == variable._symbol

    def is_variable(self):
        return True

    def variables(self):
        return [self]

    def __len__(self):
        return 1

    def __str__(self):
        return self._symbol

    def __repr__(self):
        return '<Variable: \'%s\'>' % self._symbol


class FunctionSymbol(Term):

    def __init__(self, symbol, *sub_terms):
        self._arity = 0

        def to_braces(c):
            if c == '_':
                self._arity += 1
                return '{}'
            return c

        super().__init__(''.join(map(to_braces, symbol)), *sub_terms)
        self._variables = reduce(
            lambda variables, term: variables + term.variables(),
            self._sub_terms, []
        )

    def contains(self, variable):
        return any(sub_term.contains(variable) for sub_term in self._sub_terms)

    def is_variable(self):
        return False

    def variables(self):
        return self._variables

    def __len__(self):
        return len(self._variables)

    def __iter__(self):
        return iter(self._sub_terms)

    def __str__(self):
        return self._symbol.format(*map(str, self._sub_terms))

    def __repr__(self):
        return '<FunctionSymbol: \'%s\', subterms: %s>' % (self._symbol, str(self._sub_terms))


class Substitution:

    def __init__(self, map=None):
        self._map = map or {}

    def is_identity(self):
        return len(self._map) == 0

    def __call__(self, term):
        if isinstance(term, Variable):
            return self._map.get(term, term)
        return FunctionSymbol(term._symbol, *map(self, term._sub_terms))

    def compose(self, substitution):
        if isinstance(substitution, Substitution):
            map = substitution._map
        elif isinstance(substitution, dict):
            map = substitution
        else:
            raise TypeError('an instance of term.Substitution or dict is required')

        self._map.update(map)

        return self

    def __str__(self):
        return '{%s}' % '; '.join('{} -> {}'.format(str(v), str(t)) for v, t in self._map.items())


def IdentitySub():
    return Substitution()

# if __name__ == '__main__':
#     a = Variable('a')
#     b = Variable('b')
#     c = Variable('c')
#     fab = FunctionSymbol('f(_, _)', a, b)
#     plus0 = FunctionSymbol('_ + _', c, fab)
#     plus1 = FunctionSymbol('_ + _', fab, c)
#
#     print(plus0)
#     print(plus1)
#     print(len(plus0) == len(plus1))
#
#     # sub = Substitution({
#     #     Variable('a'): Variable('x'),
#     #     Variable('b'): Variable('y')
#     # })
#     #
#     # sub.compose({Variable('a'): Variable('1')})
#     #
#     # print(sub.apply(plus))
