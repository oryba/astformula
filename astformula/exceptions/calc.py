class FormulaError(Exception):
    pass


class UnsupportedOperationError(FormulaError):
    pass


class UnsupportedASTNodeError(FormulaError):
    pass


class UnsupportedFunctionError(FormulaError):
    pass


class MissingAttributeError(FormulaError):
    pass


class MissingVariableError(FormulaError):
    pass
