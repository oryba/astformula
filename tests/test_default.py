from decimal import Decimal

from utils import executor


def test_operators(engine):
    base_const_tests = [
        {"statement": "1 + 2", "variables": {}, "result": 3},
        {"statement": "1 - 2", "variables": {}, "result": -1},
        {"statement": "1 / 2", "variables": {}, "result": Decimal('0.5')},
        {"statement": "2 * 3", "variables": {}, "result": 6},
        {"statement": "0 * 2", "variables": {}, "result": 0},
        {"statement": "0 / 2", "variables": {}, "result": 0},
        {"statement": "-1 - 2", "variables": {}, "result": -3},
        {"statement": "-3 + 3", "variables": {}, "result": 0},
        {"statement": "-1 / -5", "variables": {}, "result": Decimal('0.2')},
        {"statement": "1 / -1", "variables": {}, "result": -1},
        {"statement": "0 + -0", "variables": {}, "result": 0},
    ]

    executor(engine, base_const_tests)
