'''
# @Author       : Chr_
# @Date         : 2022-02-06 16:59:08
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-06 17:54:48
# @Description  : 启动文件
'''

from cddns import ddns
from os import path

import logging

logging.getLogger("requests").setLevel(logging.WARNING)

SCRIPT_PATH = path.split(path.realpath(__file__))[0]
CONFIG_PATH = path.join(SCRIPT_PATH, 'ddns.toml')
CACHE_PATH = '/tmp/ip.txt'


ddns(CONFIG_PATH, CACHE_PATH)
