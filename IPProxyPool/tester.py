"""
连接池测试器
"""
import time
import asyncio
import aiohttp
from IPProxyPool.logger import logger
from IPProxyPool.store import RedisClient
from IPProxyPool.settings import BATCH_TEST_SIZE


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
                self.client.decrease(proxy)
                logger.info('代理[{}]请求失败'.format(proxy))

    def run(self):
        """测试器主函数"""
        logger.info("开始运行测试器")
        try:
            count = self.client.count()
            logger.info("当前剩余 {} 个代理".format(count))
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                end = min(i + BATCH_TEST_SIZE, count)
                logger.info("正在测试第 {}-{} 个代理".format(start+1, end))
                test_proxies = self.client.batch(start, end)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            logger.error("测试器发生错误 {}".format(e.args))
