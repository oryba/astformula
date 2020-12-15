# ASTFormula – simple and safe formula engine

## Description

This package is simple and extensible formula engine with python-like 
syntax. **No eval usages under the hood** – it's a safe way to work
with formulas and variables from untrusted sources like user input.  

## Usage

### Quick start

```python
from astformula import ASTFormula

engine = ASTFormula()
executable = engine.get_calc_expression('a + b * 2')
executable({'a': 2, 'b': 3})  # returns 8
```

### Custom functions

List of available functions can be supplemented by passing dict of 
function names as keys and executables as values.

```python
from astformula import ASTFormula

def exp3(value):
    return pow(value, 3)

engine = ASTFormula(functions={'exp3': exp3})
executable = engine.get_calc_expression('a + exp3(b * 2)')
executable({'a': 2, 'b': 3})  # returns 218
```

### Custom node processors

Any AST node processor can be overridden by passing `node_type: callback`
dict to node_processors argument. Callback must take the following arguments:
 - engine: ASTFormula - engine instance
 - node: ast.AST or core types – current node of type `node_type`
 - variables: dict – all variables passed to the executable

In particular, passed `engine` instance can be used to:
 - get operator by name: `engine.get_operator(name)`
 - get function by name: `engine.get_function(name)`
 - evaluate node: `engine.evaluate(node, variables)`

```python
import ast
from astformula import ASTFormula

def bin_op(engine: 'ASTFormula', node, variables):
    # AST node structure: <node.left=left> <node.op=operator> <node.right=right>
    result = engine.get_operator(node.op)(
        engine.evaluate(node.left, variables),
        engine.evaluate(node.right, variables)
    )
    return engine.evaluate(result)

engine = ASTFormula(node_processors={ast.BinOp: bin_op})
executable = engine.get_calc_expression('a + b')
executable({'a': 2, 'b': 3})  # returns 5
```

### Custom constants
To be implemented

### Custom operators processing
Operators processing can be overridden and implemented by passing
`ast_operator_node: callback` dict to operators argument.

```python
import ast
import operator as op
from astformula import ASTFormula

custom_operators_proc = {ast.Pow: op.pow}  # **

engine = ASTFormula(operators=custom_operators_proc)
executable = engine.get_calc_expression('a ** b')
executable({'a': 2, 'b': 3})  # returns 8
```

### Handling exceptions
To simulate try..except statement a special function is provided out of
the box - `iferror(statement, fallback)`. Fallback executes only
if the main statement fails.

```python
from astformula import ASTFormula

engine = ASTFormula()
executable = engine.get_calc_expression('iferror(a ** b / 0, None)')
executable({'a': 2, 'b': 3})  # returns None
```
