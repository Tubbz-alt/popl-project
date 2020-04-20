### What is syntax analysis and how is it related to other parts in compilation?

It's a crucial part of the compilation process because this phase, a compiler in this phase checks if the program is written in a legitime way and also results in generating the parse tree. The syntax analysis for the porpouses of designing a programming language can be really useful in the sense that we can test if our design is good enougn to dont have ambiguous rules and give the correct boundary for a correct expression or statement in the language. This gives you also the base for designing the capabilities that this one is going to have, like recursion, mutation, operations and multiple other things. Finally checking the syntax of your code will avoid errors in the other stages of compilation and sometimes can also give some structure to the code and how programmers should write it.

### How is the syntactic structure of the language expressed in the PLY tool? I.e., what parts are needed in the code and how are they related to syntactic rules of the language?

Because is this tool can handle with Extended BNF we need to make the conversion, but the PLY tool has his particular way to write the rules that is using a extended comment just below the definition of the rule. And if there is another one we must use a pipeline and a different line so the PLY tool can understand it. Also is required to write every function starting with a p, so the Yacc can identify the fucntions that can use in order to start checking the syntax. So in conlcusion the tool give us the freedom to write down in a comment the syntactic rules like if it was pen and paper BNF. The issue of translating EBNF to notmal BNF is was more related with recursion and it was not complex at all.

### Explain in English what the syntax of the following elements mean (i.e. how would you describe the syntax in textual form):

#### Variable definitions

A variable definition needs to start with the token of type of variable, this can be varIDENT, constIDENT, tupleIDENT or a pipe expression. This should be next to the left arrow that means assigment and a simple expression. Every line must finish with the DOT sign. Is the must complex of the rules and can derivate to so much things because the simple expression an turn in almost everything because of atom. So it should be in this case separated and treat it differently each type.

```python
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

```

#### Function call

A function call must start with the special token funcIDENT and start with a left square bracket and finish with one right square brackets. Between them, can be arguments but is not required to have them. The arguments, their main block is the simple expression so in the language can be almost everything and can have as much as the programmer wants with the only requiremnt of separate them using commas.

```python
# function_call ::= funcIDENT LSQUARE [arguments] RSQUARE


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE
                    | funcIDENT LSQUARE arguments RSQUARE'''
    print('function_call( %s )' % p[1])


```

#### Tuple expressions

A tuple expression starts with a tuple Atom and is required. The tuple atom can be a function call, the name of a function or a value between square brackets. After this required tuple atom we can start using the combination of an the other hand, you can have multiple function calls inside a function definition, but no another function definition.

```python
# tuple_expression ::= tuple_atom {tuple_operation tuple_atom}


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom tuple_operation tuple_atom
                      | tuple_atom
                      | tuple_expression tuple_operation tuple_atom'''


```

#### Is it syntactically possible to perform arithmetic with strings ("Hello"+"world")? Why?

It's possible to perform that kind of operation because the variable definitions derive in having simple expressions and this are made of terms that at the same time are made from factors and there is a rule to have parentesis between simple expressions. This allows to perform the concatanation.

#### Is it possible to initialize a variable from a constant (N<-1. var<-N.)? Why?

Itś possible because the variable definitions in particular the rule using the variables (varIdent) have the freedom to assign a simple expression, beacuse of that and the fact that a term cann be a factor and a factor can be a constIDENT give you the freedom of concretate this kind of operation.

#### Is it possible to initialize a constant from a variable (var<-1. N<-var.)? Why?

This can't be done because for assigning a constant the only think can derive from there is a constant expression and that is limited to a number or another constant identifier (constIDENT).

#### Are the following allowed by the syntax: xx--yy and --xx? Why?

This can be done because of the rule of factor. This rules allow to have after a the factor a minus and because it could be repeated gives the language the freedom to do it recursively.

#### How is it ensured that addition/subtraction are done after multiplication/division?

Because division and substraction are in a higher level than addition, so if there is a sign of addition or substraction the next token must be a term instead of a factor. so if ther is one multiplication or division is always going to be in a lower level of the tree.

### Please mention in the document if you didn't implement functions (i.e. you are ok with passing with the minimum grade).

I didnt implement the extras and I agree to pass with the maximum amount corresponding to the phase without implementing the extra features in my syntax checker.

### What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?

This assigment was quite challenging for me, the conversion between EBNF to BNF give me a little bit of trouble and also I spend some of my time trying to make the syntax checker accept the examples of the first phase because a misreading. By the way, the phase two give me a fair challenge to work with and I enjoyed two work on it.

Learning about how to use BNF rules in code help to realize important and useful is to define good rules for porpouses of syntax checking and not letting some ambigous rules that can cause problems in the next stages of compilation. Also checking if my tokenizer actually works and this task was the best way to test it.
