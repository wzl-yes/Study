import asyncio
from 计算异步执行时间装饰器 import async_timed


async def greet(name, delay):
    await asyncio.sleep(delay)
    return f'hello {name}'


# 1. wait_for
@async_timed
async def main1():
    try:
        # 如果这个协程超时了，那么就没法继续运行了
        result = await asyncio.wait_for(greet('张三', 2), timeout=1)
        print(result)
    except asyncio.TimeoutError:
        print('超时了！')
        tasks = asyncio.all_tasks()
        print(tasks)


async def greet_group(name, delay):
    await asyncio.sleep(delay)
    if name == 'xx':
        raise ValueError("执行错误！")
    return f'hello {name}'

# 2. wait
@async_timed
async def main():
    aws = [
        # asyncio.create_task(greet_group('xx', 1)),
        asyncio.create_task(greet('xx', 1)),
        asyncio.create_task(greet('李四', 3)),
    ]
    # wait函数返回的结果是一个元组(执行完成的任务，执行超时的任务)
    # 如果没有指定timeout，那么永远不会超时
    done_tasks, pending_tasks = await asyncio.wait(aws, timeout=2, return_when=asyncio.FIRST_COMPLETED)
    print(done_tasks)
    print(pending_tasks)
    # for task in pending_tasks:
    #     result = await task
    #     print(result)




if __name__ == '__main__':
    asyncio.run(main())