import pytest

from astformula import ASTFormula


def executor(engine: ASTFormula, tests: list):
    for test in tests:
        exc = test.get('except')
        try:
            expr = engine.get_calc_expression(test['statement'])
        except Exception as e:
            if not exc:
                raise e
            assert isinstance(e, exc)
            return
        expected = test.get('result')
        variables = test['variables']
        if exc:
            with pytest.raises(exc):
                expr(variables)
        else:
            assert expected == expr(variables)
