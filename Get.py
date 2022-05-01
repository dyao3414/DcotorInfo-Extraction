from ctypes.wintypes import tagSIZE
import email
from gettext import find
import re
from ssl import CertificateError
from sys import prefix
from tkinter import N
from tkinter.messagebox import YES
from turtle import title
import requests
from pyquery import PyQuery as pq

requests.packages.urllib3.disable_warnings()
import time
import lxml
import pandas as pd


def get(url, params=None, headers=None, proxies=None, verify=True, timeout=30, allow_redirects=True, sleep=0,
        try_num=0):
    try_index = 0
    while True:
        try_index += 1
        # print(try_index,try_num)
        if try_num != 0 and try_index >= try_num:
            return
        try:
            response = requests.get(url=url, params=params, headers=headers, proxies=proxies, verify=verify,
                                    timeout=timeout, allow_redirects=allow_redirects)
            response.encoding = response.apparent_encoding
            break
        except requests.exceptions.ProxyError:
            print('get——ProxyError')
            time.sleep(sleep)
            continue
        except requests.exceptions.ConnectTimeout:
            print('get——ConnectTimeout')
            time.sleep(sleep)
            continue
        except requests.exceptions.ReadTimeout:
            print('get——ReadTimeout')
            time.sleep(sleep)
            continue
        except requests.exceptions.ConnectionError:
            print('get——ConnectionError')
            time.sleep(sleep)
            continue
        except requests.exceptions.ChunkedEncodingError:
            print('get——ChunkedEncodingError')
            time.sleep(sleep)
            continue
        except ConnectionResetError:
            print('get——ConnectionResetError')
            time.sleep(sleep)
            continue
    return response