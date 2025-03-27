# -*- coding: utf-8 -*-
import requests
import re
import os
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

# 请求头，模拟浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Cookie': 'PHPSESSID=c2id44e383fqjculohlkacrs2k; clothes=white; _ga_SPVSSSRFTT=GS1.1.1743040550.1.1.1743040741.0.0.0; _ga=GA1.1.1901660229.1743040551; closeclick=closeclick; mac_history_dianying=%5B%7B%22vod_name%22%3A%22%E5%94%90%E6%8E%A21900%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.xiuer.pro%2Fplay%2Fm7G82228-1-1%2F%22%2C%22vod_part%22%3A%22TC%E4%B8%AD%E5%AD%97%22%7D%5D; https://v.cdnlz3.com/20250130/32952_451ad4b5/index.m3u8=0'
}

# 创建会话对象并更新请求头
session = requests.session()
session.headers.update(headers)

# 获取视频流地址
home_html = session.get(url='https://www.xiuer.pro/', verify=False) # 禁用 SSL 验证
video_name = re.findall(r'<a href="/detail/(.*?)" target="_blank" class="module-item-title" title="(.*?)">', home_html.text)

print(video_name)

# 指定要下载的视频名称
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

# 提取视频播放地址
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

# 提取所有 .ts 文件的名称
ts_files = [line.strip() for line in e.text.split('\n') if line.strip() and '#' not in line]

# 消息队列
download_queue = Queue()  # 下载任务队列
write_queue = Queue()     # 写入任务队列

# 下载 .ts 文件的函数
def download_ts_file(base_url):
    while not download_queue.empty():
        ts_url = download_queue.get()
        try:
            ts_response = session.get(base_url + ts_url, verify=False)
            if ts_response.status_code == 200 and ts_response.content:
                write_queue.put((ts_url, ts_response.content))  # 将结果放入写入队列
                print(f"Downloaded: {ts_url}")
            else:
                raise Exception(f"Failed to download {ts_url}")
        except Exception as e:
            print(f"Error downloading {ts_url}: {e}")
            write_queue.put((ts_url, None))  # 放入空内容表示下载失败
        finally:
            download_queue.task_done()

# 写入文件的函数
def write_ts_files(output_file):
    sorted_results = {}
    while True:
        ts_url, content = write_queue.get()
        if ts_url is None:  # 停止信号
            break
        sorted_results[ts_url] = content
        print(f"Queued for writing: {ts_url}")
        write_queue.task_done()

        # 按顺序写入文件
        while sorted_results:
            next_key = min(sorted_results.keys())  # 找到最小的键（即最早的 .ts 文件）
            if next_key in sorted_results:
                content = sorted_results.pop(next_key)
                if content:
                    with open(output_file, 'ab+') as file:
                        file.write(content)
                        print(f"Written: {next_key}")
                else:
                    print(f"Skipped empty content for: {next_key}")

# 主程序
if __name__ == "__main__":
    import time
    # 获取当前时间
    start_time = time.time()

    base_url = c + "2000k/hls/"
    output_file = "output1.ts"

    # 如果文件已存在，删除旧文件
    if os.path.exists(output_file):
        os.remove(output_file)

    # 将所有 .ts 文件放入下载队列
    for ts_file in ts_files:
        download_queue.put(ts_file)

    # 创建下载线程池
    num_download_workers = 10
    download_threads = []
    for _ in range(num_download_workers):
        thread = threading.Thread(target=download_ts_file, args=(base_url,))
        thread.start()
        download_threads.append(thread)

    # 创建写入线程
    write_thread = threading.Thread(target=write_ts_files, args=(output_file,))
    write_thread.start()

    # 等待下载队列完成
    download_queue.join()

    # 停止写入线程
    write_queue.put((None, None))  # 发送停止信号
    write_thread.join()

    # 等待所有下载线程完成
    for thread in download_threads:
        thread.join()

    print("Download and merge completed!")
    # 获取结束时间
    end_time = time.time()
    print(f"Total time: {end_time - start_time}")
