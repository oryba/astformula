import astformula.exceptions as ex
from utils import executor


def test_exceptions(engine):
    base_const_tests = [
        {"statement": "1 / 0", "variables": {}, "except": ex.CalculationError},
        {"statement": "a.b", "variables": {'a': 1},
         "except": ex.MissingAttributeError},
        {"statement": "2 * c + 1", "variables": {},
         "except": ex.MissingVariableError},
        {"statement": "match(3 + c)", "variables": {'c': 5},
         "except": ex.UnsupportedFunctionError},
        {"statement": "a = 33", "variables": {}, "except": ex.ParsingError},
        {"statement": "a & 33", "variables": {},
         "except": ex.UnsupportedOperationError},
        {"statement": "sum(*a)", "variables": {'a': [1, 2, 3]},
         "except": ex.UnsupportedOperationError}
    ]

    executor(engine, base_const_tests)
