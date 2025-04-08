# beautifulsoup4
# 安装：pip install beautifulsoup4 -i https://pypi.tuna.tsinghua.edu.cn/simple
# lxml
# 安装：pip install lxml -i https://pypi.tuna.tsinghua.edu.cn/simple
# html5lib
# 安装：pip install html5lib -i https://pypi.tuna.tsinghua.edu.cn/simple
#
# 1. 导入 bs4 库


import bs4
# 导入lmxl库
import lxml
import requests
from lxml import etree

url = 'https://www.baidu.com/s?wd=python'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'cookie': 'BAIDUID=D4818D945BDEB541EDD4C5359BCE5C1C:FG=1; BIDUPSID=D4818D945BDEB541EDD4C5359BCE5C1C; PSTM=1740023672; ZFY=p10spoZt6jbpD1FRRMyjf:B4uv2WjHWZSlgf7WeStHwU:C; BAIDUID_BFESS=D4818D945BDEB541EDD4C5359BCE5C1C:FG=1; BDUSS=J2dGNJb1A4S1l-Y2FZQTNENE04YXcybnF2MXROanZKeEFNeWFzeTZFa3BodjluSVFBQUFBJCQAAAAAAAAAAAEAAAAc7RO6bnhueGtreGtjbmZubmYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACn512cp-ddnbm; BDUSS_BFESS=J2dGNJb1A4S1l-Y2FZQTNENE04YXcybnF2MXROanZKeEFNeWFzeTZFa3BodjluSVFBQUFBJCQAAAAAAAAAAAEAAAAc7RO6bnhueGtreGtjbmZubmYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACn512cp-ddnbm; H_PS_PSSID=60271_61027_62340_62347_62368_62370_62422_62473_62485_62522_62457_62455_62453_62450_62327_62639_62644_62674; BD_UPN=12314753; BA_HECTOR=8k00ak01a5042gaka4agak85a4i2dn1jtoebt23; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; PSINO=3; delPer=0; H_PS_645EC=2d88UJo6x%2Fd2qXroulCmH71NJy2tq2CTBmIbSkFpLcw2S4aTOTTpuahsyQ1m5DJc6V2%2B; BDSVRTM=273; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; baikeVisitId=f0d89a26-2bf2-469d-a0fa-8d624033174f; COOKIE_SESSION=2462239_0_0_1_1_1_1_0_0_1_20_0_0_0_0_0_1740023683_0_1742485917%7C2%230_0_1742485917%7C1; WWW_ST=1742485961282'
}


# 2. 发起请求
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
# 3. 解析响应内容
# 3.1 创建 bs4.BeautifulSoup 对象
soup = bs4.BeautifulSoup(response.text, 'lxml')
soups = etree.HTML(response.text)

"""
CSS选择器  class == .  id == #  
父标签在前  子/后代标签在后
"""

"""
Xpath解析器
// 从当前节点开始查找或者当前节点的子节点开始查找
/  从当前节点开始查找
//div[@class="result c-container xpath-log new-pmd"]//h3/a   严格匹配必须从头到尾一样
@可以是任意属性
//div[contains@class,"result c-container xpath-log new-pmd"]  属性包含就可以
//div[starts-with@class,"result c-container xpath-log new-pmd"]  属性以什么开头
"""
# 使用BeautifulSoup的select方法选择具有特定CSS类的元素
# 这里选择的是div标签，类名为c-container xpath-log new-pmd，其中包含h3标签，类名为tts-title，以及a标签
results = soup.select('div.c-container.xpath-log.new-pmd h3.tts-title a')
# 使用xpath
results1=soups.xpath('//div[@class="result c-container xpath-log new-pmd"]//h3/a')
# /text()  获取文本只获取当前节点的文本内容
# //text()  获取文本获取当前节点以及所有子节点的文本内容
# /string()  获取文本获取当前节点以及所有子节点的文本内容
# # 遍历查询结果，这些结果很可能是搜索结果或者是页面上的链接列表
# # 目的是过滤掉百度广告，只打印出非广告的内容
for result in results:
    # 打印出链接的文本内容，先去除空格和换行符，然后打印出链接的href属性值
    # 这样做可以使得输出的内容更加整洁，便于阅读和分析
   print(result.text.replace(' ','').replace('\n',''),result.get('href'))
   # 第一个replace()是去掉文本中的空格，第二个replace()是去掉文本中的换行符

for result in results1:
    print(result.xpath('string()'))
    # 在这里使用string()方法，可以获取到当前节点以及所有子节点的文本内容
