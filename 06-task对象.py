import asyncio
from 计算异步执行时间装饰器 import async_timed
from functools import partial


# 1. exception方法：
async def task_will_fail():
    await asyncio.sleep(1)
    raise ValueError('发生异常啦！')


async def main1():
    # create_task创建完任务后，这个任务会立马被加入到事件循环中进行调度了
    task = asyncio.create_task(task_will_fail())
    # 如果任务中没有出现异常，那么调用exception()方法就会出现异常
    # print(task.exception())
    await asyncio.sleep(2)
    print(task.exception())


# 2. add_done_callback
async def greet(name, delay):
    await asyncio.sleep(delay)
    return f'hello {name}'


def my_callback(tag, future):
    print('=' * 20)
    print(type(future))
    # 获取任务的返回值
    print(future.result())
    print('tag:', tag)
    print('=' * 20)


async def main2():
    task = asyncio.create_task(greet('张三', 2))
    # partial：偏函数。作用是可以将这个函数提前准好一些参数
    # task.add_done_callback(partial(my_callback, tag='zhangsan'))
    task.add_done_callback(partial(my_callback, '张三'))
    await task


# 3. cancel：取消任务
async def something():
    print('something start')
    await asyncio.sleep(20)


async def main():
    task = asyncio.create_task(something(), name='AA')
    print('任务名称：', task.get_name())
    task.set_name('BB')
    print('新任务名称：', task.get_name())
    await asyncio.sleep(1)
    task.cancel()
    # 等待一个已经被取消了的任务，是会抛出CancelledError的
    try:
        await task
    except asyncio.CancelledError as e:
        print(e)
        # cancelled：返回任务是否被取消
        print('是否被取消：', task.cancelled())


if __name__ == '__main__':
    asyncio.run(main())
