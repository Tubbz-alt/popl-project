#!/usr/bin/env python3

import ply.lex

tokens = [
    'COMMENT',
    'LARROW',
    'RARROW',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'COMMA',
    'DOT',
    'PIPE',
    'DOUBLEPLUS',
    'DOUBLEMULT',
    'DOUBLEDOT',
    'COLON',
    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',
    'NUMBER_LITERAL',
    'STRING_LITERAL',
    'constIDENT',
    'varIDENT',
    'tupleIDENT',
    'funcIDENT',
    'NEWLINE',
]


# non-tokens
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT(t):
    r'(?s){.*?}'
    pass


# reserved words (each identified as a token) are:
reserved = {
    'define': 'DEFINE',
    'begin': 'BEGIN',
    'end': 'END',
    'each': 'EACH',
    'select': 'SELECT'
}

tokens += reserved.values()

# one and two letter tokens:
t_LARROW = r'<-'
t_RARROW = r'->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = '\['
t_RSQUARE = '\]'
t_COMMA = r','
t_DOT = r'\.'
t_PIPE = r'\|'
t_DOUBLEPLUS = r'\+\+'
t_DOUBLEMULT = r'\*\*'
t_DOUBLEDOT = r'\.\.'
t_COLON = r':'

t_EQ = r'='
t_NOTEQ = r'!='
t_LT = r'<'
t_LTEQ = r'<='
t_GT = r'>'
t_GTEQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'%'


def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'\".*?\"'
    t.value = t.value[1:len(t.value) - 1]
    return t


def t_varIDENT(t):
    r'[a-z][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


t_constIDENT = r'[A-Z]+'
t_tupleIDENT = r'<[a-z]*>'
t_funcIDENT = r'[A-Z][a-z0-9_]+'

t_ignore = ' \t\r'


def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format(
        t.value[0], t.lexer.lineno))


lexer = ply.lex.lex()

if __name__ == '__main__':
    import argparse
    import codecs

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()

    if ns.who == True:
        print('290957 Guillermo David Aguilar Castilleja')
    elif ns.file is None:
        parser.print_help()
    else:
        with codecs.open(ns.file, 'r', encoding='utf-8') as INFILE:
            data = INFILE.read()
        lexer.input(data)

        while True:
            token = lexer.token()
            if token is None:
                break
            print(token)
