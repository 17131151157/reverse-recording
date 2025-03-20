# 安装 aiohttp 库，使用清华大学的镜像源以加快下载速度
# pip install aiohttp -i https://pypi.tuna.tsinghua.edu.cn/simple

import aiohttp  # 导入 aiohttp 库，用于执行异步 HTTP 请求
import asyncio  # 导入 asyncio 库，用于编写异步代码

# 定义请求头，模拟浏览器访问以获取更准确的网页内容
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

proxy = {'http': '172.16.17.32:80'}
# 定义异步主函数
async def main():
    # 创建一个 aiohttp 客户端会话，并传入自定义的请求头
    async with aiohttp.ClientSession(headers=headers) as session:
        # 使用会话对象发起 GET 请求到指定 URL
        html = await session.get('https://docs.aiohttp.org/en/stable/', proxy=proxy)
        # 打印响应内容的文本内容
        print(await html.text())
        # 关闭响应对象，释放资源
        html.close()

# 设置 asyncio 事件循环策略，以便在 Windows 上使用 SelectorEventLoop
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# 运行异步主函数
asyncio.run(main())