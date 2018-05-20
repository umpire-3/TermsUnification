import ply.lex as lex
import ply.yacc as yacc
import term
import re

with open('grammar.txt') as file:
    grammar = eval(file.read())

variables = {'var%d' % i: var for i, var in enumerate(grammar['Variables'])}
function_symbols = grammar['FunctionSymbols']

tokens = tuple(variables) + ('Space', 'name', 'newline')

for token, lexeme in variables.items():
    globals()['t_%s' % token] = lexeme

t_Space = r'\s'
t_name = r'[a-zA-Z][a-zA-Z0-9]+'

literals = set(''.join(function_symbols)) - {' '}


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print('An error was occurred')

lex.lex()


def production(rule):
    def decorator(fn):
        fn.__doc__ = rule
        return fn
    return decorator


def p_terms(p):
    ''' terms : term
              | term newline terms '''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = (p[1],) + p[3]


@production('term : ' + '\n| '.join(variables))
def p_var(p):
    p[0] = term.Variable(p[1])


def to_production(symbol):
    rule = 'term : %s' % ' name '.join(
        map(
            lambda s: ' '.join(
                map(
                    lambda c: '\'%s\'' % c if c != ' ' else 'Space',
                    s
                )
            ).replace('\'_\'', 'term'),

            re.split(t_name, symbol)
        )
    )
    print(rule)

    @production(rule)
    def p_term(p):
        p[0] = term.FunctionSymbol(symbol, *filter(lambda t: isinstance(t, term.Term), p))

    return p_term

for i, symbol in enumerate(function_symbols):
    globals()['p_term%d' % i] = to_production(symbol)


def p_error(p):
    print('Syntax error\nProduction -', p)

parser = yacc.yacc()

with open('input.txt') as file:
    data = parser.parse(file.read().strip('\n'))
