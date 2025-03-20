import asyncio
import time

import requests, httpx, aiohttp

# requests 只有同步请求
    # 同步请求：requests_http共花费时间： 109.73191237449646（100请求）
# httpx 同时支持同步和异步请求
    # 同步请求：httpx_http共花费时间： 109.73191237449646（100请求）
    # 异步请求：httpx共花费时间： 4.3494954109191895（100请求）
    # 异步请求：httpx共花费时间：（1000请求结果： 连接池耗尽报错）
# aiohttp 仅支持异步请求
    # aiohttp共花费时间： 2.5330536365509033（100请求）
    # 异步请求：aiohttp共花费时间： 33.35934281349182：（1000请求结果）


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
url = 'https://docs.aiohttp.org/en/stable/'


# requests
def requests_http():
    start = time.time()
    for i in range(100):
        r = requests.get(url, headers=headers)
        print(r.status_code)
    end = time.time() - start
    print('requests_http共花费时间：', end)


# httpx
def httpx_http():
    # 同步请求
    start = time.time()
    for i in range(100):
        r = httpx.get(url, headers=headers)
        print(r.status_code)
    end = time.time() - start
    print('httpx共花费时间：', end)


async def spider(i, client):
    html = await client.get(url)
    print('启动{}{}'.format(i, html.status_code))


# httpx 异步请求
async def httpx_async_http():
    start = time.time()
    async with httpx.AsyncClient(headers=headers) as client:
        lists = []
        for i in range(1000):
            lists.append(asyncio.create_task(spider(i, client)))
        await asyncio.gather(*lists)
    end = time.time() - start
    print('httpx共花费时间：', end)


# aiohttp
# async def aiohttp_http():
#     start = time.time()
#     async with aiohttp.ClientSession(headers=headers) as client:
#         lists = []
#     for i in range(100):
#         lists.append(asyncio.create_task(spider(i, client)))
#     await asyncio.gather(*lists)
#     end = time.time() - start
#     print('aiohttp共花费时间：',end)

async def spiders(i, client):
    try:
        async with client.get(url) as response:
            print('启动{}{}'.format(i, response.status))
    except Exception as e:
        print(f'任务 {i} 出错: {e}')


async def aiohttp_http():
    start = time.time()
    async with aiohttp.ClientSession(headers=headers) as client:
        tasks = []
        for i in range(1000):
            tasks.append(asyncio.create_task(spiders(i, client)))
        await asyncio.gather(*tasks)
    end = time.time() - start
    print('aiohttp共花费时间：', end)


if __name__ == '__main__':
    # requests_http()
    # httpx_http()
    # asyncio.run(httpx_async_http())
    asyncio.run(aiohttp_http())
