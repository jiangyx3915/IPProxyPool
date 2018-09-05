"""
工具文件：封装常用的方法
"""
import requests
from IPProxyPool.logger import logger
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options=None):
    """
    抓取代理页面
    :param url: 代理url
    :param options:  自定义header选项
    :return:
    """
    headers = dict(base_headers, **options) if options is not None else base_headers
    logger.info("正在抓取 {}".format(url))
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        logger.error("抓取连接 {} 失败".format(url))
        return None
