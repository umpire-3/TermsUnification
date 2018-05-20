import term
from functools import reduce


class UndefinedSub(Exception):
    pass


def unify(term1, term2):
    def _simple_unify(x, t):
        if x == t:
            return term.IdentitySub()
        elif t.contains(x):
            raise UndefinedSub()
        else:
            return term.Substitution({x: t})

    if isinstance(term1, term.Variable):
        return _simple_unify(term1, term2)
    elif isinstance(term2, term.Variable):
        return _simple_unify(term2, term1)
    else:
        if term1 != term2:
            raise UndefinedSub()
        try:
            return reduce(
                lambda unifier, terms: unifier.compose(unify(*map(unifier, terms))),
                zip(term1, term2),
                term.IdentitySub()
            )
        except UndefinedSub:
            raise
