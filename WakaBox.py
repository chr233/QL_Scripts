#!/usr/bin/python3

'''
# @Author       : Chr_
# @Date         : 2022-01-30 18:38:40
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-06 16:55:47
# @Description  : 
'''

import os
import json
import requests

# 环境变量
GIST_ID = os.getenv('GIST_ID')
WAKA_TOKEN = os.getenv('WAKA_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
# 输出设置

NAME_LEN = 11
BAR_LEN = 25
PERCENT_LEN = 5
BAR_STYLE = 1  # 进度条样式

BAR_STYLES = [
    "▁▂▃▄▅▆▇█",
    "⣀⣄⣤⣦⣶⣷⣿",
    "⣀⣄⣆⣇⣧⣷⣿",
    "○◔◐◕⬤",
    "□◱◧▣■",
    "□◱▨▩■",
    "□◱▥▦■",
    "░▒▓█",
    "░█",
    "⬜⬛",
    "⬛⬜",
    "▱▰",
    "▭◼",
    "▯▮",
    "◯⬤",
    "⚪⚫"
]

WAKA_API_URL = 'https://wakatime.com/api/v1'
GIST_API_URL = 'https://api.github.com/gists'


def waka_api_get(path):
    path = WAKA_API_URL + path
    r = requests.get(path, params={'api_key': WAKA_TOKEN})

    return json.loads(r.text)


def get_gist():
    url = f'{GIST_API_URL}/{GIST_ID}'
    r = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
    return json.loads(r.text)


def get_content(stats):
    langs = stats['languages'][:6]
    names = [x['name'] for x in langs]
    names = [
        x.ljust(NAME_LEN) if len(x) < NAME_LEN else x[:NAME_LEN - 1] + '.'
        for x in names
    ]

    texts = [(str(x['hours']), str(x['minutes'])) for x in langs]
    times = [f"{h.rjust(2)} H {m.rjust(2)} M " for h, m in texts]

    percentages = [x['percent'] for x in langs]
    bars = [gen_process_bar(x, BAR_LEN, BAR_LEN) for x in percentages]
    percentages = [f'{x:.1f}'.rjust(PERCENT_LEN) + '%' for x in percentages]

    result = '\n'.join(
        [n + t + b + p for n, t, b, p in zip(names, times, bars, percentages)])
    print(result)
    return result


def gen_process_bar(p,  min_size=24, max_size=24):
    min_delta = 999999
    bar_style = BAR_STYLES[BAR_STYLE]
    full_symbol = bar_style[len(bar_style) - 1]
    n = len(bar_style) - 1
    if (p == 100):
        return full_symbol * max_size
    p = p / 100
    for i in range(max_size, min_size-1, -1):
        x = p * i
        full = int(x)
        rest = x - full
        middle = int(rest * n)
        if (p != 0 and full == 0 and middle == 0):
            middle = 1
        d = abs(p - (full + middle / n) / i) * 100
        if (d < min_delta):
            min_delta = d
            m = bar_style[middle]
            if (full == i):
                m = ""
            r = full_symbol * full + m + bar_style[0] * (i - full - 1)
    return r


def update_gist(content):
    gist = get_gist()
    filename = list(gist['files'].values())[0]['filename']
    update = dict(description='', files={filename: {'content': content}})

    url = f'{GIST_API_URL}/{GIST_ID}'
    requests.patch(url,
                   data=json.dumps(update),
                   headers={'Authorization': f'token {GITHUB_TOKEN}'})


if __name__ == '__main__':
    print('start')
    stats = waka_api_get('/users/current/stats/last_7_days')['data']
    content = get_content(stats)
    update_gist(content)
    print('done')
