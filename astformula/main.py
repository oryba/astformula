import ast
from typing import Union

import astunparse

from astformula.defaults.functions import DEFAULT_FUNCTIONS
from astformula.defaults.operators import DEFAULT_OPERATORS
from astformula.defaults.processors import DEFAULT_PROCESSORS
from astformula.exceptions import UnsupportedASTNodeError, \
    UnsupportedOperationError, UnsupportedFunctionError, \
    CalculationError, ParsingError


class ASTFormula:

    def __init__(self, functions: dict = None, operators: dict = None,
                 node_processors: dict = None,
                 use_default: bool = True, mode: str = 'eval'):
        self.mode = mode
        self.functions = {**(DEFAULT_FUNCTIONS if use_default else {}),
                          **(functions or {})}
        self.operators = {**(DEFAULT_OPERATORS if use_default else {}),
                          **(operators or {})}
        self.node_processors = {}
        for node_types, processor in {
            **(DEFAULT_PROCESSORS if use_default else {}),
            **(node_processors or {})
        }.items():
            if isinstance(node_types, (list, tuple)):
                for node_type in node_types:
                    self.node_processors[node_type] = processor
            else:
                self.node_processors[node_types] = processor

    def get_operator(self, ast_op):
        if type(ast_op) in self.operators:
            return self.operators[type(ast_op)]
        raise UnsupportedOperationError(
            message=f'Operation {ast_op} is not supported'
        )

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        raise UnsupportedFunctionError(
            f'Function {name} is not implemented')

    def ast_parser(self, statement):
        try:
            return ast.parse(statement.replace('\n', ' '), mode=self.mode).body
        except SyntaxError as e:
            raise ParsingError(message=e.msg, node=e.text) from e

    @staticmethod
    def _unparse(node):
        try:
            return astunparse.unparse(node)
        except Exception:  # pylint: disable=W0703
            return type(node)

    def evaluate(self, node, tree_vars: Union[dict, None] = None):
        try:
            return self.process_eval(node, tree_vars)
        except CalculationError as e:
            raise e
        except Exception as e:
            node_fail = ASTFormula._unparse(node)
            raise CalculationError(
                message=str(e),
                node=node_fail
            ) from e

    def process_eval(self, node, variables: Union[dict, None] = None):
        processor = self.node_processors.get(type(node))
        
        # if no processor defined directly checking for subclasses
        # TODO: cover with tests
        if not processor:
            for typ, proc in self.node_processors.items():
                if isinstance(node, typ):
                    processor = proc
                    break
        
        if not processor:
            raise UnsupportedASTNodeError(
                message=f'No processor defined for node {type(node)}',
                node=ASTFormula._unparse(node)
            )
        return processor(self, node, variables)

    def get_calc_expression(self, statement: str) -> callable:
        parsed = self.ast_parser(statement)

        def calculator(variables: dict):
            return self.evaluate(parsed, variables)

        return calculator
