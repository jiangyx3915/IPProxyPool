"""
代理抓取文件
"""
import json
import re
from IPProxyPool.utils import get_page
from IPProxyPool.logger import logger
from pyquery import PyQuery as pq


class ProxyMetaClass(type):
    """
    代理元类，用于收集抓取类中所有定义的站点
    """
    def __new__(cls, name, parent, attr):
        site_count = 0
        attr['__CrawlFunc__'] = []
        for k, v in attr.items():
            if k.startswith('crawl_'):
                attr['__CrawlFunc__'].append(k)
            site_count += 1
        attr['__CrawlFuncCount__'] = site_count
        return type.__new__(cls, name, parent, attr)


class ProxyCrawl(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        """
        通过传进的方法名，动态进行方法调用，获取到抓回来的代理
        :param callback:
        :return:
        """
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            logger.info("成功获取到代理 {}".format(proxy))
            proxies.append(proxy)
        return proxies

    def crawl_66ip(self, page_count=5):
        """
        获取66ip的代理
        :param page_count: 页码
        :return: 代理
        """
        url_format = 'http://www.66ip.cn/{}.html'
        urls = [url_format.format(page) for page in range(1, page_count+1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])


if __name__ == '__main__':
    crawl = ProxyCrawl()
    for proxy in crawl.get_proxies('crawl_66ip'):
        print(proxy)
