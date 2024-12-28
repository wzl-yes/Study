import asyncio
import time
from functools import wraps


def async_timed(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        print(f'开始执行{func}，参数为：{args}, {kwargs}')
        start = time.time()
        try:
            return await func(*args, **kwargs)
        finally:
            end = time.time()
            total = end - start
            print(f'结束执行{func}，耗时：{total:.4f}秒')

    return wrapped
