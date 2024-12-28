import asyncio
from 计算异步执行时间装饰器 import async_timed


async def greet(name, delay):
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


# 这是同步运行
@async_timed
async def main1():
    # 执行两个协程
    result1 = await greet('xx', 2)
    print(result1)
    result2 = await greet('yy', 3)
    print(result2)


# 1. 用创建任务的方式并发运行
@async_timed
async def main2():
    # 以下是正确写法
    # 并发运行，必须要将协程包装成Task对象，才能够并发执行
    task1 = asyncio.create_task(greet('xx', 2))
    task2 = asyncio.create_task(greet('yy', 3))

    # 对创建好的任务进行await
    result1 = await task1
    print(result1)

    result2 = await task2
    print(result2)

    # 以下是错误写法
    # 注意：必须要把所有任务都创建好，再分别await，才能并发运行
    # 不能够创建完任务后就立即await，这样会导致程序同步执行了
    # result1 = await asyncio.create_task(greet('xx', 2))
    # print(result1)
    # result2 = await asyncio.create_task(greet('yy', 3))
    # print(result2)


# 2. 用TaskGroup方式并发运行协程
async def greet_group(name, delay):
    await asyncio.sleep(delay)
    if name == 'xx':
        raise ValueError("执行错误！")
    return f'hello {name}'


@async_timed
async def main3():
    try:
        async with asyncio.TaskGroup() as group:
            # 在这个里面，创建任务，就不再使用asyncio.create_task
            # 而是用group.create_task来创建任务
            task1 = group.create_task(greet_group('xx', 1))
            task2 = group.create_task(greet_group('yy', 2))
            task3 = group.create_task(greet_group('zz', 3))
    except Exception as e:
        print(e)
    # 上面代码执行完后，有可能是两种情况
    # 1. 所有任务都正常运行完了
    # print(task1.result())
    # print(task2.result())
    # print(task3.result())

    # 2. 其中有任务出现异常了，导致后面的任务被取消了，从而提前退出协程的并发运行
    # * done：返回该协程是否完成（被取消，也算完成）
    # * cancelled：返回该协程是否被取消了
    print(task1.cancelled())
    print(task1.done())
    print(task2.cancelled())
    print(task2.done())
    print(task3.done())


# 3. 用gather实现协程的并发
@async_timed
async def main4():
    # gather在将所有协程全部都执行完后，会按照协程入队的顺序，将协程的返回值存放在results中
    try:
        results = await asyncio.gather(
            greet_group('xx', 1),
            greet('李四', 3),
            greet('王五', 2),
            # 把异常作为返回值，而不会抛出异常
            # return_exceptions=True
        )

        print(results)
    except Exception as e:
        pass
    # 获取所有正在运行的任务
    tasks = asyncio.all_tasks()
    for task in tasks:
        # 这里说明：gather中有的任务发生异常了，剩余还没执行完的任务也不会被取消
        # print(task.get_name(), task.cancelled())

        # 继续等待还未执行完的任务
        # Task-1：代表的是main这个协程
        # 不能在协程中await自身，比如在main协程中，不能await main这样
        if task.get_name() == 'Task-1':
            continue
        result = await task
        print(result)


# 4. 使用as_completed
@async_timed
async def main5():
    aws = [
        greet_group('xxx', 1),
        greet('李四', 3)
    ]
    # 可以指定超时时间,timeout=2
    # 如果超过指定的超时时间，还有任务没有完成，那么会抛出TimeoutError异常
    # 剩余的任务不会被取消
    try:
        for coro in asyncio.as_completed(aws):
            result = await coro
            print(result)
    except Exception as e:
        pass
    tasks = asyncio.all_tasks()
    for task in tasks:
        print(task.get_name(), task.cancelled())
        # 如果没有继续等待task执行，那么这个task就不会执行了，而是出于pending状态
        if task.get_name() != 'Task-1':
            result = await task
            print(result)


if __name__ == "__main__":
    asyncio.run(main5())
