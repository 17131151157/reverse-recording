# -*- coding: utf-8 -*-
#!/usr/bin/python3

import ssl
from urllib import request
import random
import time
import re


class MaoyanSpider:
    def __init__(self):
        # 初始化猫眼电影爬虫类
        self.url = 'https://maoyan.com/board/4?offset={}'  # 猫眼电影排行榜的URL模板
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
            'Cookie': '__mta=214675752.1627866406865.1627875459110.1627875460018.12; uuid_n_v=v1; uuid=E85FEA50F32D11EB8C9F5D6CCA53AC9DD7DBAF07A29F40DB93EF3FC782A0F81F; _csrf=38f9740349f3f3b55a88970a5164681765e4611ccbd2fc8ef5f526914970614d; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1627866407; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=17b04661fb4c8-0813968a22224b-d7e1938-e1000-17b04661fb4c8; _lxsdk=E85FEA50F32D11EB8C9F5D6CCA53AC9DD7DBAF07A29F40DB93EF3FC782A0F81F; __mta=214675752.1627866406865.1627866406865.1627866409991.2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1627875460; _lxsdk_s=17b04f00a6e-9d7-717-d8%7C%7C9'
        }
        # 添加计数变量，用于统计抓取到的电影数量
        self.i = 0

    def get_html(self, url):
        """获取HTML内容"""
        # 创建 SSL 上下文并禁用验证，以避免SSL证书验证错误
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        # 创建请求对象，并添加请求头
        req = request.Request(url=url, headers=self.headers)
        # 发送请求并获取响应
        res = request.urlopen(req, context=ssl_context)
        # 读取响应内容并解码为字符串
        html = res.read().decode()
        # 直接调用解析函数，解析HTML内容
        self.parse_html(html)

    def parse_html(self, html):
        """提取HTML内容"""
        # 定义正则表达式，用于匹配电影信息
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?">.*?</a></p>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>'
        # 编译正则表达式
        pattern = re.compile(regex, re.S)
        # 使用正则表达式查找所有匹配的电影信息
        r_list = pattern.findall(html)
        # 调用数据处理函数，保存提取到的电影信息
        self.save_html(r_list)

    def save_html(self, r_list):
        """数据处理函数"""
        item = {}
        # 遍历提取到的电影信息列表
        for r in r_list:
            # 将电影名称、主演和上映时间存入字典
            item['name'] = r[0].strip()
            item['star'] = r[1].strip()
            item['time'] = r[2].strip()
            # 打印电影信息
            print(item)
            # 计数加1
            self.i += 1

    def run(self):
        """程序运行调配"""
        # 遍历页码，每次增加10，从0到90
        for page in range(0, 91, 10):
            # 格式化URL，生成具体的请求URL
            url = self.url.format(page)
            # 调用获取HTML内容的函数
            self.get_html(url)
            # 控制数据抓取频率，随机等待1到2秒
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    # 创建猫眼电影爬虫对象
    spider = MaoyanSpider()
    # 运行爬虫
    spider.run()
    # 打印抓取到的电影数量
    print('电影数量：', spider.i)
