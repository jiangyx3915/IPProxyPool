"""
代理池获取器
"""
import sys
from IPProxyPool.logger import logger
from IPProxyPool.store import RedisClient
from IPProxyPool.crawler import ProxyCrawl
from IPProxyPool.settings import POOL_MAX_THRESHOLD


class Getter:
    def __init__(self):
        self.client = RedisClient()
        self.crawler = ProxyCrawl()

    def is_over_threshold(self):
        """判断是否达到了代理池容量的限制"""
        if self.client.count() >= POOL_MAX_THRESHOLD:
            return True
        return False

    def run(self):
        logger.info("代理池获取器开始运行")
        if not self.is_over_threshold():
            for callback in self.crawler.__CrawlFunc__:
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.client.add(proxy)
