import pandas as pd
import requests
import re
import html


header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.12022 SLBChan/105 '
    }
detiais = re.compile(r'<a href="(.*?)(?=" class="">)')  # 网址
content = re.compile(r'<span class="title">(.*?)</span>')  # 电影中英文标题
dirs = re.compile(r'导演:(.*?)(?=<br>)')  # 导演
details = re.compile(r'(?<=<br>)(.*?)(?=</p>)', re.DOTALL)  # 时间、国家和类型

names = []
top_names = []
top_directors = []
top_websites = []
top_details =[]
top_times = []
top_countries = []
top_types = []

for i in range(10):
    url = f'https://movie.douban.com/top250?start={i * 25}&filter='
    response = requests.get(url=url, headers=header)
    if response.status_code != 200:
        print(f"{url}请求失败，状态码: {response.status_code}")
    web = html.unescape(response.text)

    names.extend(content.findall(web))
    top_websites.extend(detiais.findall(web))
    top_directors.extend(dirs.findall(web))
    top_details.extend(details.findall(web))

for name in range(len(names)):

    if names[name][1] != '/':
        top_names.append(names[name])

    elif names[name][1] == '/':
        top_names[-1] = top_names[-1] + names[name]

for detail in top_details:

    detail = detail.strip().split('/')

    top_times.append(detail[0])
    top_countries.append(detail[1])
    top_types.append(detail[-1])

for i in range(len(top_names)):
    print(f"第{i+1}", top_names[i], top_websites[i], top_directors[i])
    print()
    print('                                 ', top_times[i], top_countries[i], top_types[i])
    print()

data = {
    '名称': top_names,
    '网址': top_websites,
    '导演和主演': top_directors,
    '时间': top_times,
    '国家': top_countries,
    '类型': top_types
}
top_250 = pd.DataFrame(data)
top_250.index = list(range(1, len(top_names)+1))
print(top_250)
