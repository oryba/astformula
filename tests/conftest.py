import pytest

from astformula import ASTFormula


@pytest.fixture(scope="session")
def engine() -> ASTFormula:
    yield ASTFormula()
