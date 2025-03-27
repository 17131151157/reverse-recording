# -*- coding: utf-8 -*-
import re




'''
使用方法一:
r_list = re.findall('正则表达式', html, re.S)

使用方法二:
pattern = re.complie('正则表达式', re.S)
r_list = pattrern.findall(html)

注意①: 使用findall()方法得到的结果一定为列表
注意②: re.S作为使用正则表达式元字符,可匹配\n在内的所有字符串
'''

"""
正则表达式常用元字符
. - 任意一个字符(不包含\n)
\d - 一个数字
\s - 空白字符
\S - 非空白字符
[] - 包含[]内容
* - 出现0次或多次
+ - 出现1次或多次
"""

"""
贪婪匹配和非贪婪匹配
贪婪匹配:
    1. 在整个表达式匹配成功的前提下,尽可能多的匹配: * + ?
    2. 表达方式: .* .+ .?

非贪婪匹配:
    1. 在整个表达式匹配成功的前提下,尽可能少的匹配 * + ?
    2. 表达方式: .*? .+? .??
"""





html = """
<div><p>如果你为门中弟子伤她一分,我便屠你满门!</p></div>
<div><p>如果你为天下人损伤她一毫,我便杀尽天下人!</p></div>
"""

patterns1 = re.findall('<div><p>.*</p></div>', html,re.S)
print(patterns1)


# 贪婪匹配
pattern = re.compile('<div><p>.*</p></div>', re.S)
result = re.findall(pattern, html)
print(result)

# 非贪婪匹配
pattern2 = re.compile('<div><p>.*?</p></div>', re.S)
result1 = re.findall(pattern2, html)
print(result1)