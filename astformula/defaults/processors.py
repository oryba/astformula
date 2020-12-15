import ast
import operator as op
from decimal import Decimal
from typing import TYPE_CHECKING

from astformula.exceptions.calc import UnsupportedOperationError, MissingAttributeError, MissingVariableError

if TYPE_CHECKING:
    from astformula.main import ASTFormula

CALC_NONE = "CalcNone"


def if_error(engine, variables, condition, alternative_result):
    try:
        return engine.evaluate(condition, variables)
    except Exception:
        return engine.evaluate(alternative_result, variables)


def not_in(container, item):
    return not op.contains(container, item)


def ast_compare(engine: 'ASTFormula', node, variables):
    operator = engine.get_operator(node.ops[0])
    if operator in [op.contains, not_in]:
        result = operator(
            engine.evaluate(node.comparators[0], variables),
            engine.evaluate(node.left, variables))
    else:
        result = operator(
            engine.evaluate(node.left, variables), engine.evaluate(node.comparators[0],
                                                                   variables))
    return result


def ast_bool_and(engine: 'ASTFormula', node, variables):
    result = None
    for value in node.values:
        result = engine.evaluate(value, variables)
        if not result:
            return result
    return result


def ast_bool_or(engine: 'ASTFormula', node, variables):
    result = None
    for value in node.values:
        result = engine.evaluate(value, variables)
        if result:
            return result
    return result


def get_keywords(engine: 'ASTFormula', node, variables):
    dict_all = {}
    if node.keywords:
        for elem in node.keywords:
            dict_all[elem.arg] = engine.evaluate(elem.value)
    return dict_all


def num(engine: 'ASTFormula', node, variables):
    result = node.n
    if type(result) == float:
        result = Decimal(f'{result}')
    return result


def constant(engine: 'ASTFormula', node, variables):
    result = node.value
    if type(result) == float:
        result = Decimal(f'{result}')
    return result


def raw_val(engine: 'ASTFormula', node, variables):
    return node


def float_val(engine: 'ASTFormula', node, variables):
    return Decimal(f'{node}')


def string(engine: 'ASTFormula', node, variables):
    return node.s


def raw_list(engine: 'ASTFormula', node, variables):
    result = []
    for el in node:
        if isinstance(el, ast.Starred):
            result += [*engine.evaluate(el.value, variables)]
        else:
            result += [engine.evaluate(el, variables)]
    return result


def raw_tuple(engine: 'ASTFormula', node, variables):
    result = []
    for el in node:
        if isinstance(el, ast.Starred):
            result += [*engine.evaluate(el.value, variables)]
        else:
            result += [engine.evaluate(el, variables)]
    return tuple(result)


def bin_op(engine: 'ASTFormula', node, variables):
    result = engine.get_operator(node.op)(
        engine.evaluate(node.left, variables),
        engine.evaluate(node.right, variables)
    )
    return engine.evaluate(result)


def unary_op(engine: 'ASTFormula', node, variables):
    return engine.get_operator(node.op)(engine.evaluate(node.operand, variables))


def bool_op(engine: 'ASTFormula', node, variables):
    if isinstance(node.op, ast.And):
        result = ast_bool_and(engine, node, variables)
    elif isinstance(node.op, ast.Or):
        result = ast_bool_or(engine, node, variables)
    else:
        result = engine.get_operator(node.op)(engine.evaluate(node.values[0], variables),
                                              engine.evaluate(node.values[1], variables))
    return result


def ast_tuple(engine: 'ASTFormula', node, variables):
    result = []
    for el in node.elts:
        if isinstance(el, ast.Starred):
            result += [*engine.evaluate(el.value, variables)]
        else:
            result += [engine.evaluate(el, variables)]
    return tuple(result)


def ast_list(engine: 'ASTFormula', node, variables):
    result = []
    for el in node.elts:
        if isinstance(el, ast.Starred):
            result += [*engine.evaluate(el.value, variables)]
        else:
            result += [engine.evaluate(el, variables)]
    return result


def ast_dict(engine: 'ASTFormula', node, variables):
    return {engine.evaluate(k, variables): engine.evaluate(v, variables) for k, v in zip(node.keys, node.values)}


def ast_index(engine: 'ASTFormula', node, variables):
    return engine.evaluate(engine.evaluate(node.value, variables)[engine.evaluate(node.slice.value, variables)])


def ast_call(engine: 'ASTFormula', node, variables):
    if not getattr(node.func, 'id', None):
        raise UnsupportedOperationError(f'Function {node.func} is not supported')
    if node.func.id == 'iferror':
        result = if_error(engine, variables, *node.args)
    else:
        result = engine.get_function(node.func.id)(*engine.evaluate(node.args, variables),
                                                   **get_keywords(engine, node, variables))
    return result


def ast_attr(engine: 'ASTFormula', node, variables):
    try:
        attr_val = engine.evaluate(node.value, variables).get(node.attr, CALC_NONE)
    except AttributeError:
        attr_val = getattr(engine.evaluate(node.value, variables), node.attr, CALC_NONE)

    if attr_val is CALC_NONE:
        raise MissingAttributeError(f'Missing attribute {node.attr}')
    return engine.evaluate(attr_val, variables)


def ast_if(engine: 'ASTFormula', node, variables):
    if engine.evaluate(node.test, variables):
        return engine.evaluate(node.body, variables)
    else:
        return engine.evaluate(node.orelse, variables)


def ast_list_comp(engine: 'ASTFormula', node, variables):
    result = []
    if node.generators:
        g = node.generators[0]
        for val in engine.evaluate(g.iter, variables):
            if isinstance(g.target, ast.Name):
                local_vars = {g.target.id: val}
            elif isinstance(g.target, ast.Tuple):
                local_vars = dict(zip(map(lambda elt: elt.id, g.target.elts), val))
            else:
                raise TypeError(f"Unsupported type {type(g.target)} for list comprehensions")

            if not g.ifs or all(bool(engine.evaluate(
                    cond,
                    {**variables, **local_vars}
            )) for cond in g.ifs):
                result.append(engine.evaluate(node.elt, {**variables, **local_vars}))
    return result


def ast_name(engine: 'ASTFormula', node, variables):
    if node.id not in variables:
        raise MissingVariableError(f"Variable {node.id} isn`t set")
    return engine.evaluate(variables.get(node.id))


def ast_name_constant(engine: 'ASTFormula', node, variables):
    return node.value


DEFAULT_PROCESSORS = {
    ast.Num: num,
    ast.Constant: constant,
    float: float_val,
    (int, str, bool, dict, type(None), Decimal): raw_val,
    ast.Str: string,
    list: raw_list,
    tuple: raw_tuple,
    ast.BinOp: bin_op,
    ast.UnaryOp: unary_op,
    ast.BoolOp: bool_op,
    ast.Compare: ast_compare,
    ast.Tuple: ast_tuple,
    ast.List: ast_list,
    ast.Dict: ast_dict,
    ast.Subscript: ast_index,
    ast.Call: ast_call,
    ast.Attribute: ast_attr,
    ast.IfExp: ast_if,
    (ast.GeneratorExp, ast.ListComp): ast_list_comp,
    ast.Name: ast_name,
    ast.NameConstant: ast_name_constant
}
