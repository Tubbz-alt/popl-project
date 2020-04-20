#!/usr/bin/env python3

from ply import yacc
import tokenizer

# TOKENIZER
tokens = tokenizer.tokens


# name ::= definition # defines a non-terminal symbol 'name'
# a1 a2    # 'a1' is immediately followed by 'a2'
# a1 | a2  # 'a1' or 'a2'
# [a]    # 'a' or nothing (optional)
# {a}    # zero or more times 'a'
# (a1 | a2) a3  # 'a1' or 'a2' always followed by 'a3'


# program ::= {function_or_variable_definition} return_value DOT


def p_program(p):
    '''program : function_or_variable_definition return_value DOT
               | function_or_variable_definition program'''

# function_or_variable_definition ::= variable_definition | function_definition


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions
                                       | function_definition'''


# function_definition ::= DEFINE funcIDENT LSQUARE [formals] RSQUARE
#                         BEGIN
#                         {variable_definitions}
#                         return_value DOT
#                         END DOT

def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN variable_definitions return_value DOT END DOT
                        | DEFINE funcIDENT LSQUARE RSQUARE BEGIN variable_definitions return_value DOT END DOT
                        | DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN return_value DOT END DOT
                        | DEFINE funcIDENT LSQUARE RSQUARE BEGIN return_value DOT END DOT'''
    print('func_definition( %s )' % p[2])
# formals ::= varIDENT {COMMA varIDENT}


def p_formals(p):
    '''formals : varIDENT
               | varIDENT COMMA varIDENT
               | formals COMMA varIDENT'''

# return_value ::= EQ simple_expression | NOTEQ pipe_expression


def p_return_value(p):
    '''return_value : EQ simple_expression
                    | NOTEQ pipe_expression'''

# variable_definitions ::= varIDENT LARROW simple_expression DOT
#                        | constIDENT LARROW constant_expression DOT
#                        | tupleIDENT LARROW tuple_expression DOT
#                        | pipe_expression RARROW tupleIDENT DOT


def p_variable_definitions(p):
    '''variable_definitions : variable_definition
                            | constant_definition
                            | tuplevariable_definition
                            | variable_definitions variable_definition
                            | variable_definitions constant_definition
                            | variable_definitions tuplevariable_definition'''


def p_variable_definition(p):
    '''variable_definition : varIDENT LARROW simple_expression DOT'''
    print('variable_definition( %s )' % p[1])


def p_constant_definition(p):
    '''constant_definition : constIDENT LARROW constant_expression DOT'''
    print('constant_definition( %s )' % p[1])


def p_tuplevariable_definition(p):
    '''tuplevariable_definition : tupleIDENT LARROW tuple_expression DOT
                                | pipe_expression RARROW tupleIDENT DOT'''
    if p[2] == '<-':
        print('tuplevariable_definition( %s )' % p[1])
    else:
        print('tuplevariable_definition( %s )' % p[3])

# constant_expression ::= constIDENT
#                       | NUMBER_LITERAL


def p_constant_expression(p):
    '''constant_expression : constIDENT
                      | NUMBER_LITERAL'''

# pipe_expression ::= tuple_expression {PIPE pipe_operation}


def p_pipe_expression(p):
    '''pipe_expression : tuple_expression PIPE pipe_operation
                        | tuple_expression
                        | pipe_expression PIPE pipe_operation'''
    print('pipe_expression')

# pipe_operation ::= funcIDENT
#                  | MULT
#                  | PLUS
#                  | each_statement


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT
                 | MULT
                 | PLUS
                 | each_statement'''

# each_statement ::= EACH COLON funcIDENT


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''

# tuple_expression ::= tuple_atom {tuple_operation tuple_atom}


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom tuple_operation tuple_atom
                      | tuple_atom
                      | tuple_expression tuple_operation tuple_atom'''

# tuple_operation ::= DOUBLEPLUS


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''

# tuple_atom ::= tupleIDENT
#      | function_call
#      | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
#      | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
#      | LSQUARE arguments RSQUARE


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
                | function_call
                | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
                | LSQUARE arguments RSQUARE'''

# function_call ::= funcIDENT LSQUARE [arguments] RSQUARE


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE
                    | funcIDENT LSQUARE arguments RSQUARE'''
    print('function_call( %s )' % p[1])


# arguments ::= simple_expression {COMMA simple_expression}


def p_arguments(p):
    '''arguments : simple_expression
                 | simple_expression COMMA simple_expression
                 | arguments COMMA simple_expression'''


# atom ::= function_call | NUMBER_LITERAL | STRING_LITERAL | varIDENT |
#          constIDENT | LPAREN simple_expression RPAREN |
#          SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE

def p_atom(p):
    '''atom : function_call
            | NUMBER_LITERAL 
            | STRING_LITERAL 
            | varIDENT 
            | constIDENT 
            | LPAREN simple_expression RPAREN 
            | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    if len(p) == 2:
        print('atom( %s )' % p[1])
    else:
        print('atom')

# factor ::= [MINUS] atom


def p_factor(p):
    '''factor : MINUS atom
            | atom'''
    print('factor')


# term ::= factor {(MULT | DIV) factor}


def p_term(p):
    '''term : factor
            | factor MULT factor
            | factor DIV factor
            | term MULT factor
            | term DIV factor
            '''
    print('term')

# simple_expression ::= term {(PLUS | MINUS) term}


def p_simple_expression(p):
    '''simple_expression : term
                        | term PLUS term
                        | term MINUS term
                        | simple_expression PLUS term
                        | simple_expression MINUS term'''
    print('simple_expression')


def p_error(token):
    print("{%d}:Syntax Error (token: '%s')" % (token.lineno, token.value))
    raise SystemExit


parser = yacc.yacc()

if __name__ == '__main__':
    import argparse
    import codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print('88888 Ahto Simakuutio')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=tokenizer.lexer, debug=False)
        if result is None:
            print('syntax OK')
