import pytest

from astformula import ASTFormula


def executor(engine: ASTFormula, tests: list):
    for test in tests:
        expr = engine.get_calc_expression(test['statement'])
        expected = test['result']
        variables = test['variables']
        if isinstance(expected, Exception):
            with pytest.raises(Exception):
                expr(variables)
        else:
            assert expected == expr(variables)
