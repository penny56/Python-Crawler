# bilibili@轻松学Python > Python爬虫实战项目教程 > 案例二、网易云
# 打开网易云应以音乐，进入一个榜单，把榜单上所有音乐download到一个music目录下。
# YJ 20230112

import requests     # 数据请求模块
import re
import os

filename = 'music'
if not os.path.exists(filename):
    os.mkdir(filename)


# 在浏览器上打开网易云应音乐，榜单页面，复制url
# 也可以：inspect > filter: type=doc > 应该是第一条 > header中 Request Method = Get
url = "https://music.163.com/discover/toplist?id=3778678"

# 把inspect中，request headers里的 user-agent 拷贝过来
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

response = requests.get(url=url, headers=headers)
#print(response.text)

# 从返回内容里，用正则表达式去过滤出来榜单中的歌曲，以（id, 歌名）为一个元组。
html_data = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a>', response.text)
for num_id, title in html_data:
    print (num_id, title)
    # 这里是网易云音乐提供的一个API
    music_url = f'http://music.163.com/song/media/outer/url?id={num_id}.mp3'
    music_content = requests.get(url=music_url, headers=headers).content

    with open(filename + '/' + title + '.mp3', mode='wb') as f:
        f.write(music_content)
