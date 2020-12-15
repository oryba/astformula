import json
import math
from datetime import datetime, date
from uuid import uuid4

from astformula.defaults.processors import if_error

DEFAULT_FUNCTIONS = {
    'sum': sum,
    'count': len,
    'len': len,
    'max': max,
    'min': min,
    'abs': abs,
    'iferror': if_error,
    'log': math.log,
    'log10': math.log10,
    'round': round,
    'str': str,
    'float': float,
    'int': int,
    'list': list,
    'tuple': tuple,
    'set': set,
    'dict': dict,
    'bool': bool,
    'enumerate': enumerate,
    'reversed': reversed,
    'inf': lambda: 2 ** 53 - 1,
    'pow': pow,
    'date_now': lambda: date.today().isoformat(),
    'datetime_now': lambda: datetime.now(),
    'get_uuid': lambda: str(uuid4()),
    'loads': json.loads,
    'dumps': json.dumps
}
