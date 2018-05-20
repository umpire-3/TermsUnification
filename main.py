import term
from input import data
from unification import unify, UndefinedSub

if __name__ == '__main__':
    # print(*map(str, data), sep='\n')
    #
    # for t0, t1 in zip(data[0], data[1]):
    #     print(t0, ', ', t1, sep='')

    if len(data) >= 2:
        term1, term2 = data[:2]
        print('For terms:')
        print('     1)', term1)
        print('     2)', term2)
        try:
            print('Unification is',unify(*data[:2]))
        except UndefinedSub:
            print('Unification is not possible')
    else:
        print('Two terms required')