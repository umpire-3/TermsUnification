import ply.lex as lex
import ply.yacc as yacc
import term
import re

with open('grammar.txt') as file:
    grammar = eval(file.read())

variables = grammar['Variables']
function_symbols = grammar['FunctionSymbols']

tokens = (
    'Variable',
    'Space',
    'Symbol',
    'newline'
)

literals = set(''.join(function_symbols)) - {' '}

t_Space = r'\s'


def t_Symbol(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in variables:
        t.type = 'Variable'
    else:
        t.type = 'Symbol'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print('An error was occurred')

lex.lex()


def p_terms(p):
    """ terms : term
              | term newline terms """
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = (p[1],) + p[3]


def p_var(p):
    """term : Variable"""
    p[0] = term.Variable(p[1])
print(p_var.__doc__)


def to_production(symbol):
    def p_term(p):
        p[0] = term.FunctionSymbol(symbol, *filter(lambda t: isinstance(t, term.Term), p))

    p_term.__doc__ = 'term : %s' % ' Symbol '.join(
        map(
            lambda s: ' '.join(
                map(
                    lambda c: '\'%s\'' % c if c != ' ' else 'Space',
                    s
                )
            ).replace('\'_\'', 'term'),

            re.split(t_Symbol.__doc__, symbol)
        )
    )
    print(p_term.__doc__)

    return p_term

for i, symbol in enumerate(function_symbols):
    globals()['p_term%d' % i] = to_production(symbol)


def p_error(p):
    print('Syntax error\nProduction -', p)

parser = yacc.yacc()

with open('input.txt') as file:
    data = parser.parse(file.read().strip('\n'))
