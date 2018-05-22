from input import data
from unification import unify, UndefinedSub

if __name__ == '__main__':
    if len(data) >= 2:
        term1, term2 = data[:2]
        print('For terms:')
        print('     1)', term1)
        print('     2)', term2)
        try:
            unifier = unify(term1, term2)
            print('\nUnification is \N{GREEK SMALL LETTER SIGMA} =', unifier, '\n')
            print('     \N{GREEK SMALL LETTER SIGMA}(', term1, ') =', unifier(term1))
            print('     \N{GREEK SMALL LETTER SIGMA}(', term2, ') =', unifier(term2))
        except UndefinedSub:
            print('Unification is not possible')
    else:
        print('Two terms required')
