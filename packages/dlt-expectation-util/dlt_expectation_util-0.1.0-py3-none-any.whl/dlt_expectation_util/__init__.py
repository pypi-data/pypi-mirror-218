import functools

import dlt
import pyspark.sql.functions as f


def is_not_null(colname):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return dlt.expect(f"{colname} is an integer column", f.col(colname).isNotNull())(func)(*args, **kwargs)
        return wrapper
    return decorator