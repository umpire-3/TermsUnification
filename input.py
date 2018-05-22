import string
import ply.lex as lex
import ply.yacc as yacc
import term
import re

with open('grammar.txt') as file:
    grammar = eval(file.read())

variables = grammar['Variables']
function_symbols = {symbol: re.findall(r'[a-zA-Z][a-zA-Z0-9]*', symbol) for symbol in grammar['FunctionSymbols']}
symbols = []
for names in function_symbols.values():
    symbols.extend(names)

tokens = tuple(symbols) + (
    'Variable',
    'Space',
    'Newline'
)

literals = set(''.join(function_symbols)) - set(string.ascii_letters) - {' ', '_'}
print('Lexis:', tokens + tuple(literals), sep='\n')

t_Space = r'\s'


def t_Symbol(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in variables:
        t.type = 'Variable'
    elif t.value in symbols:
        t.type = t.value
    return t


def t_Newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print('An error was occurred')

lex.lex()


def p_terms(p):
    """ terms : term
              | term Newline terms """
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = (p[1],) + p[3]


def p_var(p):
    """term : Variable"""
    p[0] = term.Variable(p[1])
print('Grammar:', p_var.__doc__, sep='\n')


def to_production(symbol, tokens):
    def to_rule(it, symbol):
        try:
            token = next(it)
            return (' %s ' % token).join(map(lambda s: to_rule(it, s), symbol.split(token)))
        except StopIteration:
            return ' '.join(
                map(
                    lambda c: '\'%s\'' % c if c != ' ' else 'Space',
                    symbol
                )
            ).replace('\'_\'', 'term')

    def p_term(p):
        p[0] = term.FunctionSymbol(symbol, *filter(lambda t: isinstance(t, term.Term), p))
    p_term.__doc__ = 'term : %s' % to_rule(iter(tokens), symbol)
    print(p_term.__doc__)

    return p_term

for i, (symbol, names) in enumerate(function_symbols.items()):
    globals()['p_term%d' % i] = to_production(symbol, names)


def p_error(p):
    print('Syntax error\nProduction -', p)

parser = yacc.yacc()

with open('input.txt') as file:
    data = parser.parse(file.read().strip('\n'))
