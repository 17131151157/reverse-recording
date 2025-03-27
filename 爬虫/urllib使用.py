# -*- coding: utf-8 -*-
import urllib
from urllib import parse
from urllib import request


# 1、定义常用变量
url = 'http://httpbin.org/get'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
# 2、包装请求
req = request.Request(url=url, headers=headers)
# 3、发送请求
res = request.urlopen(req)
# 4、获取响应内容
html = res.read().decode()
print(html)


# todo urllib.parse编码模块

# 作用: 给URL地址中的查询参数进行编码
#
# 导入方式:
# -- import urllib.parse
# -- from urllib import parse
# urlencode()方法
# -- 给URL地址中查询参数进行编码,参数类型为字典

# URL地址中多个查询参数
# -- 编码前: params = {'wd': '美女', 'pn': '50'}
# -- 编码中: params = urllib.parse.urlencode(params)
# -- 编码后: params结果: 'wd=%E7%BE%8E%E5%A5%B3&pn=50'


# urllib.parse.quote('参数为字符串')编码
# 作用:
# -- 对URL地址中的中文进行编码,类似于urlencode()方法
# 示例:
word = '美女'
result = urllib.parse.quote(word)
print("result 的值：{}".format(result))
# result结果: '%E7%BE%8E%E5%A5%B3'


# unquote()方法
# 作用
# -- 将编码后的字符串转换为普通的Unicode字符串

results = urllib.parse.unquote(result)
print("results 的值：{}".format(results))
# 结果： results 的值：美女







