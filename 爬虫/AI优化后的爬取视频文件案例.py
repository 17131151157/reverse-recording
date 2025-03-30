# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Cookie': 'PHPSESSID=c2id44e383fqjculohlkacrs2k; clothes=white; _ga_SPVSSSRFTT=GS1.1.1743040550.1.1.1743040741.0.0.0; _ga=GA1.1.1901660229.1743040551; closeclick=closeclick; mac_history_dianying=%5B%7B%22vod_name%22%3A%22%E5%94%90%E6%8E%A21900%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.xiuer.pro%2Fplay%2Fm7G82228-1-1%2F%22%2C%22vod_part%22%3A%22TC%E4%B8%AD%E5%AD%97%22%7D%5D; https://v.cdnlz3.com/20250130/32952_451ad4b5/index.m3u8=0'
}

session = requests.session()
session.headers.update(headers)

# 获取视频流地址
home_html = session.get(url='https://www.xiuer.pro/', verify=False)
video_name = re.findall(r'<a href="/detail/(.*?)" target="_blank" class="module-item-title" title="(.*?)">', home_html.text)
print(video_name)

video_name_1 = '封神第二部：战火西岐'
video_url_list = []
for i in video_name:
    if video_name_1 in i[1]:
        video_url = 'https://www.xiuer.pro/detail/' + i[0]
        video_url_list.append(video_url)

print(video_url_list)

# 请求视频播放页获取视频数据
video_html = session.get(url=video_url_list[0], verify=False)
video_data = re.findall(r'<a href="/play/(.*?)/" title="(.*?)">', video_html.text)
video_play_url = 'https://www.xiuer.pro/play/' + video_data[0][0] + '/'
video_play_data = session.get(url=video_play_url, verify=False)

url_pattern = r'"url":"(.*?)svip.high21-playback.com([^"]+)"'
video_play_data_url = re.search(url_pattern, video_play_data.text)
video_urls = video_play_data_url.group().replace("\\/", "/").split('"')
source_data_url = session.get(url=video_urls[3], verify=False)

# 获取所有 .ts 文件的 URL
a = None
source_data_url_list = source_data_url.text.split('\n')
for i in source_data_url_list:
    if '#' not in i and i.strip():
        a = i
        break

b = video_urls[3].split('/')
c = 'https://svip.high21-playback.com/' + b[3] + "/" + b[4] + "/"
d = c + a
e = session.get(url=d, verify=False)

ts_files = [line.strip() for line in e.text.split('\n') if line.strip() and '#' not in line]

# 下载 .ts 文件的函数
def download_ts_file(ts_url, base_url):
    ts_response = session.get(base_url + ts_url, verify=False)
    return ts_url, ts_response.content

# 多线程下载
def download_all_ts_files(ts_files, base_url, max_workers=10):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_ts_file, ts, base_url): ts for ts in ts_files}
        for future in as_completed(future_to_url):
            ts_url, content = future.result()
            results[ts_url] = content
            print(f"Downloaded: {ts_url}")
    return results

# 确保按顺序写入文件
def write_sorted_ts_files(results, output_file):
    sorted_ts_files = sorted(results.keys())
    with open(output_file, 'ab+') as file:
        for ts_url in sorted_ts_files:
            file.write(results[ts_url])
            print(f"Written: {ts_url}")

# 主程序
if __name__ == "__main__":
    base_url = c + "2000k/hls/"
    output_file = "output.ts"

    # 如果文件已存在，删除旧文件
    if os.path.exists(output_file):
        os.remove(output_file)

    # 下载所有 .ts 文件
    results = download_all_ts_files(ts_files, base_url)

    # 按顺序写入文件
    write_sorted_ts_files(results, output_file)

    print("Download and merge completed!")