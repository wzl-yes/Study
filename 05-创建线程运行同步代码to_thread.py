import asyncio
import time
from 计算异步执行时间装饰器 import async_timed


def get_url(url):
    print(f'开始获取{url}')
    # 同步阻塞2s
    time.sleep(2)
    print(f'结束获取{url}')
    return 'success'


async def greet(name, delay):
    await asyncio.sleep(delay)
    return f'hello {name}'

@async_timed
async def main():
    results = await asyncio.gather(
        asyncio.to_thread(get_url, url='https://www.baidu.com'),
        greet('张三', 2)
    )
    print(results)


if __name__ == '__main__':
    asyncio.run(main())