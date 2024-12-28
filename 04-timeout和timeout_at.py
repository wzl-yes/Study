import asyncio
from 计算异步执行时间装饰器 import async_timed


async def greet(name, delay):
    await asyncio.sleep(delay)
    return f'hello {name}'


@async_timed
async def main():
    try:
        # asyncio.timeout_at()
        async with asyncio.timeout(2):
            task1 = asyncio.create_task(greet('张三', 1), name='zhangsan')
            task2 = asyncio.create_task(greet('李四', 3), name='lisi')

            result1 = await task1
            print(result1)
            result2 = await task2
            print(result2)
    except asyncio.TimeoutError:
        print('超时了!')
        tasks = asyncio.all_tasks()
        print(tasks)
        print(task1.done())
        print(task2.cancelled())


if __name__ == '__main__':
    asyncio.run(main())
