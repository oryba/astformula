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
        {"statement": "a[:(1 + 2)]", "variables": {"a": [1, 2, 3, 4, 5]}, "result": [1, 2, 3]},
        {"statement": "a[1:3]", "variables": {"a": [1, 2, 3, 4, 5]}, "result": [2, 3]},
        {"statement": "a[(1 + 2):]", "variables": {"a": [1, 2, 3, 4, 5]}, "result": [4, 5]},
        {"statement": "a[::(1 + 1)]", "variables": {"a": [1, 2, 3, 4, 5]}, "result": [1, 3, 5]},
        {"statement": "[b ** 2 for b in a]", "variables": {"a": [1, 2, 3, 4, 5]}, "result": [1, 4, 9, 16, 25]},
        {"statement": "[i for i, b in enumerate(a) if b >= 4]", "variables": {"a": [1, 2, 3, 4, 5]}, "result": [3, 4]},
        {
            "statement": "{i + 1: b ** 2 for i, b in enumerate(a) if i < 3}",
            "variables": {"a": [1, 2, 3, 4, 5]},
            "result": {1: 1, 2: 4, 3: 9}
        },
        {
            "statement": "{i + 1: b ** 2 for i, b in enumerate(a) if i < 3 and b ** 0.5 > 1.5}",
            "variables": {"a": [1, 2, 3, 4, 5]},
            "result": {3: 9}
        },
    ]

    executor(engine, base_const_tests)
