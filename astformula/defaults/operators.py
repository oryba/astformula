import ast
import operator as op

from astformula.defaults.processors import not_in

DEFAULT_OPERATORS = {
    ast.Add: op.add,  # +
    ast.Sub: op.sub,  # -
    ast.Mult: op.mul,  # *
    ast.Div: op.truediv,  # /
    ast.Pow: op.pow,  # **
    ast.BitXor: op.xor,  # ^ (bitwise XOR)
    ast.And: lambda x, y: x and y,  # and
    ast.Or: lambda x, y: x or y,  # or
    ast.Gt: op.gt,  # >
    ast.GtE: op.ge,  # >=
    ast.Lt: op.lt,  # <
    ast.LtE: op.le,  # <=
    ast.USub: op.neg,  # !
    ast.In: op.contains,  # in
    ast.NotIn: not_in,  # not in
    ast.Eq: op.eq,  # ==
    ast.NotEq: op.ne,  # !=
    ast.Not: op.not_  # not
}
