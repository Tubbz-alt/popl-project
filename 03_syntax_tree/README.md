### What is an (abstract) syntax tree and how is it related to other parts in compilation?

An AST is just a representation or a way of visualize of the syntactic structure of a program or a expression. In the case of this project is the whole program so the first node is always going to be the program as itself, from there the rules start being leafs in the tree. Is related to the next stages because is a way of seeing how the compiler is going to execute the operations in a hierarchical way. This checks which rules are choosen in the syntax checking for making a valid code and you can see also in this tree if there are some ambiguos rules that can derive in paths that are not supposed to appear or be valid for the syntax.

### How is the syntax tree generated using the PLY tool? I.e., what things are needed in the code and how are they related to syntactic rules of the language and the tree?

Is quite easy, we need to define our structure for the AST node, so it consist in handling with arrays and sub arrays creating a node every subarray (head) and starting from there. For example program is the first one always so it works like this:

```python
def p_program_1(p):
    '''program : function_or_variable_definition return_value DOT'''
    p[0] = ASTnode('program')
    p[0].children_definitions = [p[1]]
    p[0].child_return_value = p[2]
```

In the rule after it matches, we handle every specific derivation. In this case for example, we need to create our node with the ASTnode constructor that we define above. Then for the children we assign the value of the string before the return value and the return value separatly so we can continue the contruction of our tree.

### Explain in English what kind of tree is formed in your code from the following syntactic elements:

#### Variable definitions

The top of the node is labeled as variable_definition and is only showing us the fact thats a definition of a variable is called, the first child of it has the name of the variable. Last, the child of the one that has the name has as first child the expression and that we can say what is assigned to that variable.

#### Pipe expressions

For this i needed to use separate this rule in three main cases, the first one is for a tuple expression and only put as child the tuple expression. The second one, handles the same but with a pipe operation. The last one is for the cases where we have multple pipe expressions recursively and it assigns this also as child of the pipe operation.

#### Function call (if you implemented it)

The fucntion calls as head has the name of the function that is called and then a first child thats is called arguments that is a list of every argument between the parentesis of our funtion call. Also every argument has their type of value, for example string literal, variable, etc.

### Answer the following based on the syntax definition and your implementation:

#### In which cases is it possible in your implementation to end up with a tree with empty child attributes (somewhere in the tree there is a place for a child node (or nodes), but there is none)? I.e., in which situations you end up with tree nodes with child*... attribute being None, or children*... attribute being an empty list?

I do not think that is possible or at least in my implementation because the rules that have final cases we only add the value of the node as an attribute of the ASTnode, we do not define a child tree. To make a tree with child none we must assign or at least declare the children list that in this code is not the case.

#### Are there places in your implementation where you were able to "simplify" the tree by omitting trivial/non-useful nodes or by collecting a recursive repeating structure into a list of child nodes?

I think is a difficult job to try to simply the rules but at least one of them that I identify is the program having useless variable definition because we can definively delete that intermediary rule and make multiple cases of program.

### Please mention in the document if you didn't implement functions (i.e. you are ok with passing with the minimum grade).

I am okay to passing with the minimum grade because in this phase there were not specific requirements of extra work and I do not implemnent something out of the minimal requirements specified for this phase.

### What did you think of this assignment? What was difficult? What was easy? Did you learn anything useful?

It was a little tricky and personally I did not like it as the last one beacuse it was basically trying to debug the las phase for making the representation. I give thanks for the printing code provided because without it the amount of job for this phase would be huge and not affordable for exam weeks.
