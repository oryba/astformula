class ParsingError(Exception):
    def __init__(self, message: str, node: str):
        super().__init__(message)
        self.message = message
        self.node = node

    def __str__(self):
        return f"{self.message} at {self.node}"


class CalculationError(Exception):
    def __init__(self, message: str, node: str = None):
        super().__init__(message)
        self.message = message
        self.node = node

    def __str__(self):
        if self.node:
            return f"{self.message} in {self.node}"
        return self.message


class UnsupportedOperationError(CalculationError):
    pass


class UnsupportedASTNodeError(CalculationError):
    pass


class UnsupportedFunctionError(CalculationError):
    pass


class MissingAttributeError(CalculationError):
    pass


class MissingVariableError(CalculationError):
    pass
