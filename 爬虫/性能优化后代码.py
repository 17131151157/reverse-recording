# -*- coding: utf-8 -*-
import asyncio
import ssl
import certifi
import aiohttp
from aiohttp import TCPConnector

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
url = 'https://docs.aiohttp.org/en/stable/'

# 性能优化参数
MAX_CONCURRENCY = 200  # 最大并发数（根据网络环境调整）
REQUEST_TIMEOUT = 15    # 请求超时时间（秒）
MAX_CONNECTIONS = 100   # 连接池大小
DNS_CACHE_TTL = 300     # DNS缓存时间（秒）

ssl_context = ssl.create_default_context(cafile=certifi.where())

async def spider(i, session, semaphore):
    async with semaphore:  # 控制并发量
        try:
            async with session.get(
                    url,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT,
                    ssl=ssl_context
            ) as response:
                print(f'任务{i} 状态码: {response.status}')
                return await response.text()  # 实际使用时可处理响应内容
        except Exception as e:
            print(f'任务{i} 出错: {e}')
            return None

async def aiohttp_http():
    # 优化连接池配置
    conn = TCPConnector(
        ssl=ssl_context,
        limit=MAX_CONNECTIONS,
        ttl_dns_cache=DNS_CACHE_TTL,
        use_dns_cache=True,
        force_close=True  # 强制关闭连接防止堆积
    )

    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async with aiohttp.ClientSession(
            connector=conn,
            headers=headers,
            trust_env=True  # 支持系统代理配置
    ) as session:
        start = asyncio.get_event_loop().time()

        # 创建任务列表（分批次提交防止事件循环过载）
        tasks = []
        for i in range(1000):
            task = asyncio.create_task(spider(i, session, semaphore))
            tasks.append(task)

            # 每100个任务分批提交（平衡内存和吞吐量）
            if len(tasks) % 100 == 0:
                await asyncio.sleep(0.1)

        # 使用gather的return_exceptions=True防止个别任务崩溃
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end = asyncio.get_event_loop().time() - start

        print(f'aiohttp 总耗时: {end:.2f}秒')
        # 过滤有效结果（可根据需要处理）
        # valid_results = [r for r in results if r is not None]

if __name__ == '__main__':
    asyncio.run(aiohttp_http())