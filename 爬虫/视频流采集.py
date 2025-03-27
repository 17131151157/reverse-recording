# -*- coding: utf-8 -*-
import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Cookie': 'PHPSESSID=c2id44e383fqjculohlkacrs2k; clothes=white; _ga_SPVSSSRFTT=GS1.1.1743040550.1.1.1743040741.0.0.0; _ga=GA1.1.1901660229.1743040551; closeclick=closeclick; mac_history_dianying=%5B%7B%22vod_name%22%3A%22%E5%94%90%E6%8E%A21900%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.xiuer.pro%2Fplay%2Fm7G82228-1-1%2F%22%2C%22vod_part%22%3A%22TC%E4%B8%AD%E5%AD%97%22%7D%5D; https://v.cdnlz3.com/20250130/32952_451ad4b5/index.m3u8=0'
}


session = requests.session()
# session 对象添加 headers
session.headers.update(headers)

home_html = session.get(url='https://www.xiuer.pro/',verify=False)
'''
<div class="module-item-titlebox">
<a href="/detail/6Na82228/" target="_blank" class="module-item-title" title="黄雀">黄雀</a>
'''
# 视频详情链接格式： view-source:https://www.xiuer.pro/detail/K9a82228/
# 请求视频详情链接拿到视频数据请求的字符串

# 获取视频名称及
video_name = re.findall(r'<a href="/detail/(.*?)" target="_blank" class="module-item-title" title="(.*?)">', home_html.text)
print(video_name)


headers1 = {
    'Host': 'svip.high21-playback.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br, zstd',
'Origin': 'https://www.xiuer.pro',
'Connection': 'keep-alive',
'Referer': 'https://www.xiuer.pro/',
                 'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site',
'TE': 'trailers'
}



video_name_1 = '封神第二部：战火西岐'
video_url_list = []
for i in video_name:
    if video_name_1 in i[1]:
        video_url = 'https://www.xiuer.pro/detail/' + i[0]
        video_url_list.append(video_url)  # 添加视频链接到列表

print(video_url_list)

# 视频链接格式： view-source:https://www.xiuer.pro/detail/K9a82228/
# 请求视频链接拿到视频数据请求的字符串
# 没有做循环所有视频请求， 只爬取一部电影
video_html = session.get(url=video_url_list[0],verify=False)
# print(video_html.text)
# 获取视频数据请求的字符串
# <a href="/play/p7G82228-1-1/"
video_data = re.findall(r'<a href="/play/(.*?)/" title="(.*?)">', video_html.text)
'''
[
('p7G82228-1-1', '立刻播放封神第二部：战火西岐'), ('p7G82228-2-1', '播放封神第二部：战火西岐TC'), 
('p7G82228-2-1', '播放封神第二部：战火西岐TC'), ('p7G82228-4-1', '播放封神第二部：战火西岐TC国语'), 
('p7G82228-4-1', '播放封神第二部：战火西岐TC国语'), ('p7G82228-1-1', '播放封神第二部：战火西岐TS国语'), 
('p7G82228-1-1', '播放封神第二部：战火西岐TS国语'), ('p7G82228-3-1', '播放封神第二部：战火西岐TC中字'),
 ('p7G82228-3-1', '播放封神第二部：战火西岐TC中字')]

可能会像这样拿到多条数据，这是因为有不同线路
'''
print(video_data)
# 视频播放页格式： https://www.xiuer.pro/play/m7G82228-1-1/
# 请求视频播放页拿到视频播放链接
video_play_url = 'https://www.xiuer.pro/play/' + video_data[0][0] + '/'
print(video_play_url)
video_play_data = session.get(url=video_play_url,verify=False)
print(video_play_data.text)  # 视频播放页源码
# 获取视频播放链接
url_pattern = r'"url":"(.*?)svip.high21-playback.com([^"]+)"'
video_play_data_url = re.search(url_pattern, video_play_data.text)
video_urls = video_play_data_url.group()  # 视频播放链接
# 先去掉转义符后在操作按照英文引号分割
cleaned_url = video_urls.replace("\\/", "/").split('"')
# 视频播放链接格式： "url":"https://svip.high21-playback.com/20250130/41323_559eaec3/index.m3u8"
#  分割后数据：['', 'url', ':', 'https://svip.high21-playback.com/20250130/41323_559eaec3/index.m3u8', '']
source_data_url = session.get(url=cleaned_url[3],verify=False)
print(source_data_url.text)
'''
返回数据： 
#EXTM3U
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=1080x608
2000k/hls/mixed.m3u8
思路： 返回数据按照换行符分割，然后使用时 for 循环遍历拿到不带#号的数据
'''
a = None
source_data_url_list = source_data_url.text.split('\n')
print(source_data_url_list)  # 视频播放链接列表
for i in source_data_url_list:
    if '#' not in i:
       a=i  # 视频播放链接列表
    else:
        pass

print(a)

# 视频流资源地址： https://svip.high21-playback.com/20250130/41323_559eaec3/2000k/hls/mixed.m3u8

"""
https://svip.high21-playback.com/20250130/41323_559eaec3/2000k/hls/mixed.m3u8
这串数据不知道来的/20250130/41323_559eaec3/但是翻看前面的数据发现是固定的
视频播放链接格式： "url":"https://svip.high21-playback.com/20250130/41323_559eaec3/index.m3u8"
发现取自这条数据，那么我们将这条数据按照/分割然后再进行组装
已知2000k/hls/mixed.m3u8取自source_data_url_list

"""

b = cleaned_url[3].split('/')
print(b)
# 链接组装

c= 'https://svip.high21-playback.com/'+b[3]+"/"+b[4]+"/"

d = c + a
print("33333333333",a)
e = session.get(url=d,verify=False)
# 所有视频数据，因为网站把一整个视频分成很多小片段
print("222222222222",e.text)
f = []
for i in e.text.split('\n'):
    if '#' not in i:
        print(i)
        f.append(i)
    else:
        pass
session.headers.update(headers1)
# '975ff4c31ba000000.ts', '975ff4c31ba000001.ts',
with open('test.mp4','ab+') as file :
    for num,i in enumerate(f):
        print("1111111111111", c+i)
        file.write(session.get(url=c+'2000k/hls/'+i,verify=False).content)
        print("总数据数：{}, 已写入视频数：{}, 进度条：{}".format(len(f),num, num/len(f)*100))







import subprocess

def convert_ts_to_mp4(input_file, output_file):
    """
    将 TS 文件转换为 MP4 文件
    :param input_file: 输入的 TS 文件路径
    :param output_file: 输出的 MP4 文件路径
    """
    try:
        # 使用 ffmpeg 命令进行转换
        command = [
            'ffmpeg',          # 调用 ffmpeg
            '-i', input_file,  # 输入文件
            '-c:v', 'copy',    # 视频编码器直接复制（不重新编码）
            '-c:a', 'aac',     # 音频编码器使用 AAC
            output_file        # 输出文件
        ]

        # 执行命令
        subprocess.run(command, check=True)
        print(f"转换成功！文件已保存为: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
    except FileNotFoundError:
        print("未找到 ffmpeg，请确保已安装 ffmpeg 并添加到系统环境变量中。")

# 示例用法
if __name__ == '__main__':

    input_ts = "test.ts"  # 输入的 TS 文件路径
    output_mp4 = "output.mp4"  # 输出的 MP4 文件路径
    convert_ts_to_mp4(input_ts, output_mp4)
