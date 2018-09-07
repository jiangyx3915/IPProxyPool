"""
连接池测试器
"""
import sys
import asyncio
import aiohttp
from IPProxyPool.logger import logger
from IPProxyPool.store import RedisClient


class Tester(object):
    def __init__(self):
        self.client = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:   代理
        :return:        代理是否有效
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                logger.info('正在测试代理: {}'.format(real_proxy))
            except Exception:
                pass
        pass