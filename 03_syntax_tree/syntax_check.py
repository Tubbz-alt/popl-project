#!/usr/bin/env python3

from ply import yacc
import tokenizer
import tree_print

# TOKENIZER
tokens = tokenizer.tokens


class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr


# name ::= definition # defines a non-terminal symbol 'name'
# a1 a2    # 'a1' is immediately followed by 'a2'
# a1 | a2  # 'a1' or 'a2'
# [a]    # 'a' or nothing (optional)
# {a}    # zero or more times 'a'
# (a1 | a2) a3  # 'a1' or 'a2' always followed by 'a3'


# program ::= {function_or_variable_definition} return_value DOT


def p_program_1(p):
    '''program : function_or_variable_definition return_value DOT'''
    p[0] = ASTnode('program')
    p[0].children_definitions = [p[1]]
    p[0].child_return_value = p[2]


def p_program_2(p):
    '''program : function_or_variable_definition program'''
    p[0] = p[2]
    p[0].children_definitions.append(p[1])

# function_or_variable_definition ::= variable_definition | function_definition


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions
                                       | function_definition'''
    p[0] = p[1]

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

    p[0] = ASTnode('function_definition')
    p[0].value = str(p[2])

    if len(p) == 11:
        if p[4] == '[':   # Case 4
            p[0].child_formals = p[4]
            p[0].child_return_value = p[7]
        else:             # Case 1
            p[0].children_variable_definitions = [p[6]]
            p[0].child_return_value = p[7]
    elif len(p) == 12:    # Case 2
        p[0].child_formals = p[4]
        p[0].children_variable_definitions = [p[7]]
        p[0].child_return_value = p[8]
    elif len(p) == 10:    # Case 3
        p[0].child_return_value = p[6]


# formals ::= varIDENT {COMMA varIDENT}


def p_formals_1(p):
    '''formals : varIDENT'''

    p[0] = ASTnode('formals')
    p[1] = ASTnode(p[1])
    p[0].children_variable = [p[1]]


def p_formals_2(p):
    '''formals : varIDENT COMMA varIDENT'''

    p[0] = ASTnode('formals')
    p[1] = ASTnode(p[1])
    p[3] = ASTnode(p[3])
    p[0].children_variable = [p[1], p[3]]


def p_formals_3(p):
    '''formals : formals COMMA varIDENT'''

    p[0] = p[1]
    p[0].children_variable.append(p[3])

# return_value ::= EQ simple_expression | NOTEQ pipe_expression


def p_return_value(p):
    '''return_value : EQ simple_expression
                    | NOTEQ pipe_expression'''

    p[0] = ASTnode('simple_return_value')
    p[0].child_retval = p[2]

# variable_definitions ::= varIDENT LARROW simple_expression DOT
#                        | constIDENT LARROW constant_expression DOT
#                        | tupleIDENT LARROW tuple_expression DOT
#                        | pipe_expression RARROW tupleIDENT DOT


def p_variable_definitions(p):
    '''variable_definitions : variable_definition
                            | constant_definition
                            | tuplevariable_definition'''

    p[0] = ASTnode('variables')
    p[0].children_def = [p[1]]


def p_variable_definitions_2(p):
    '''variable_definitions : variable_definitions variable_definition
                            | variable_definitions constant_definition
                            | variable_definitions tuplevariable_definition'''
    p[0] = p[1]
    p[0].children_def.append(p[2])


def p_variable_definition(p):
    '''variable_definition : varIDENT LARROW simple_expression DOT'''
    print('variable_definition( %s )' % p[1])
    p[0] = ASTnode('variable_definition')
    p[0].value = p[1]
    p[0].child_expr = p[3]


def p_constant_definition(p):
    '''constant_definition : constIDENT LARROW constant_expression DOT'''
    print('constant_definition( %s )' % p[1])

    p[0] = ASTnode('constant_definition')
    p[0].value = p[1]
    p[0].child_expression = p[3]


def p_tuplevariable_definition(p):
    '''tuplevariable_definition : tupleIDENT LARROW tuple_expression DOT
                                | pipe_expression RARROW tupleIDENT DOT'''

    p[0] = ASTnode('tuplevariable_definition')

    if p[2] == '<-':
        print('tuplevariable_definition( %s )' % p[1])
        p[0].value = p[1]
        p[0].child_expression = p[3]
    else:
        print('tuplevariable_definition( %s )' % p[3])
        p[0].value = p[3]
        p[0].child_expression = p[1]

# constant_expression ::= constIDENT
#                       | NUMBER_LITERAL


def p_constant_expression_1(p):
    '''constant_expression : constIDENT'''

    p[0] = ASTnode('constant')
    p[0].value = p[1]


def p_constant_expression_2(p):
    '''constant_expression : NUMBER_LITERAL'''

    p[0] = ASTnode('NUMBER_LITERAL')
    p[0].value = p[1]


# pipe_expression ::= tuple_expression {PIPE pipe_operation}


def p_pipe_expression_1(p):
    '''pipe_expression : tuple_expression'''

    print('pipe_expression')

    p[0] = ASTnode('pipe_expression')
    p[0].children_tuple_expression = [p[1]]


def p_pipe_expression_2(p):
    '''pipe_expression : tuple_expression PIPE pipe_operation'''

    print('pipe_expression')

    p[0] = ASTnode('pipe_expression')
    p[0].children_tuple_expression = [p[1]]
    p[0].children_pipe_operation = [p[3]]


def p_pipe_expression_3(p):
    '''pipe_expression : pipe_expression PIPE pipe_operation'''

    print('pipe_expression')

    p[0] = p[1]
    p[0].children_pipe_expression.append(p[3])


# pipe_operation ::= funcIDENT
#                  | MULT
#                  | PLUS
#                  | each_statement


def p_pipe_operation_1(p):
    '''pipe_operation : funcIDENT
                      | MULT
                      | PLUS'''

    p[0] = ASTnode('pipe_operation')
    p[0].value = p[1]


def p_pipe_operation_2(p):
    '''pipe_operation : each_statement'''

    p[0] = ASTnode('pipe_operation')
    p[0].child_statement = p[1]

# each_statement ::= EACH COLON funcIDENT


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''

    p[0] = ASTnode('each')
    p[0].value = p[3]

# tuple_expression ::= tuple_atom {tuple_operation tuple_atom}


def p_tuple_expression_1(p):
    '''tuple_expression : tuple_atom
                        | tuple_atom tuple_operation tuple_atom'''

    p[0] = ASTnode('tuple_expression')

    if len(p) == 2:
        p[0].children_tuple = [p[1]]
    else:
        p[0].children_tuple = [p[1], p[3]]
        p[0].child_operation = p[2]


def p_tuple_expression_2(p):
    '''tuple_expression : tuple_expression tuple_operation tuple_atom'''

    p[0] = p[1]
    p[0].children_tuple.append(p[3])
    p[0].child_operation = p[2]

# tuple_operation ::= DOUBLEPLUS


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''

    p[0] = ASTnode('tuple_operation')
    p[0].value = p[1]

# tuple_atom ::= tupleIDENT
#      | function_call
#      | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
#      | LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE
#      | LSQUARE arguments RSQUARE


def p_tuple_atom_1(p):
    '''tuple_atom : tupleIDENT'''

    p[0] = ASTnode('tuple_ident')
    p[0].value = p[1]


def p_tuple_atom_2(p):
    '''tuple_atom : function_call'''

    p[0] = ASTnode('function')
    p[0].child_funtcion = p[1]


def p_tuple_atom_3(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                  | LSQUARE constant_expression DOUBLEDOT constant_expression RSQUARE'''

    p[0] = ASTnode('tuple')
    p[0].children_constant_expression = [p[2], p[4]]
    p[0].value = p[3]


def p_tuple_atom_4(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''

    p[0] = p[2]


# function_call ::= funcIDENT LSQUARE [arguments] RSQUARE


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE
                    | funcIDENT LSQUARE arguments RSQUARE'''

    print('function_call( %s )' % p[1])

    p[0] = ASTnode('function_call')
    p[0].value = p[1]

    if len(p) == 5:
        p[0].child_arguments = p[3]


# arguments ::= simple_expression {COMMA simple_expression}


def p_arguments_1(p):
    '''arguments : simple_expression'''

    p[0] = ASTnode('arguments')
    p[0].children_argument = [p[1]]


def p_arguments_2(p):
    '''arguments : simple_expression COMMA simple_expression'''

    p[0] = ASTnode('arguments')
    p[0].children_argument = [p[1], p[3]]


def p_arguments_3(p):
    '''arguments : arguments COMMA simple_expression'''

    p[0] = p[1]
    p[0].children_argument.append(p[3])


# atom ::= function_call | NUMBER_LITERAL | STRING_LITERAL | varIDENT |
#          constIDENT | LPAREN simple_expression RPAREN |
#          SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE


def p_atom_1(p):
    '''atom : function_call'''

    print('atom')

    p[0] = ASTnode('function_call')
    p[0].value = p[1]


def p_atom_2(p):
    '''atom : NUMBER_LITERAL'''

    print('atom')

    p[0] = ASTnode('NUMBER_LITERAL')
    p[0].value = p[1]


def p_atom_3(p):
    '''atom : STRING_LITERAL'''

    print('atom')

    p[0] = ASTnode('STRING_LITERAL')
    p[0].value = p[1]


def p_atom_4(p):
    '''atom : varIDENT'''

    print('atom')

    p[0] = ASTnode('var')
    p[0].value = p[1]


def p_atom_5(p):
    '''atom : constIDENT'''

    print('atom')

    p[0] = ASTnode('const')
    p[0].value = p[1]


def p_atom_6(p):
    '''atom : LPAREN simple_expression RPAREN'''

    print('atom')

    p[0] = ASTnode('atom')
    p[0].child_constant_expression = p[2]


def p_atom_7(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''

    print('atom')

    p[0] = ASTnode('select')
    p[0].child_constant_expression = p[3]
    p[0].child_tuple_expression = p[5]


# factor ::= [MINUS] atom


def p_factor(p):
    '''factor : MINUS atom
            | atom'''

    print('factor')

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = -p[2]


# term ::= factor {(MULT | DIV) factor}


def p_term_1(p):
    '''term : factor'''

    print('term')

    p[0] = p[1]


def p_term_2(p):
    '''term : factor MULT factor
            | factor DIV factor'''

    print('term')

    p[0] = ASTnode('term')
    p[0].children_factor = [p[1], p[3]]
    p[0].value = p[2]


def p_term_3(p):
    '''term : term MULT factor
            | term DIV factor'''

    print('term')

    p[0] = p[1]
    p[0].children_factor.append(p[3])
    p[0].value = p[2]

# simple_expression ::= term {(PLUS | MINUS) term}


def p_simple_expression_1(p):
    '''simple_expression : term'''

    print('simple_expression')

    p[0] = p[1]


def p_simple_expression_2(p):
    '''simple_expression : term PLUS term
                         | term MINUS term'''

    print('simple_expression')

    p[0] = ASTnode('simple_expression')
    p[0].children_term = [p[1], p[3]]
    p[0].value = p[2]


def p_simple_expression_3(p):
    '''simple_expression : simple_expression PLUS term
                         | simple_expression MINUS term'''

    print('simple_expression')

    p[0] = p[1]
    p[0].children_term.append(p[3])
    p[0].value = p[2]


def p_error(token):

    print("{%d}:Syntax Error (token: '%s')" % (token.lineno, token.value))
    raise SystemExit


parser = yacc.yacc()

if __name__ == '__main__':
    import argparse
    import codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat = "unicode"
    if ns.treetype:
        outformat = ns.treetype

    if ns.who == True:
        # Identify who wrote this
        print("290957 - Guillermo David Aguilar Castilleja")
    elif ns.file is None:
        # User didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=tokenizer.lexer, debug=False)

        # We separate the syntax checker output and the tree output
        print("Syntax OK!")
        print('\n The Tree Print: \n')
        tree_print.treeprint(result, outformat)
