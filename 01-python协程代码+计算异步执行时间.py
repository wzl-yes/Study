import asyncio
from 计算异步执行时间装饰器 import async_timed


# import time
# time.sleep(1)
@async_timed
async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')


if __name__ == '__main__':
    # main()：创建一个协程，并不是直接运行main函数，并且这个协程是不会自己运行的
    asyncio.run(main())

# 以下是注释，不是代码，方便理解事件循环
# 有一个协程队列，存储所有需要执行的协程
'''
queue = [cor1, cor2, ...]
while True:
	cor = queue.pop()
	result = await cor
'''
# 其他代码
