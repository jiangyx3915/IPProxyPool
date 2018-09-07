"""
代理存储器
"""
import redis
import re
from IPProxyPool.logger import logger
from IPProxyPool.errors import PoolEmptyError
from IPProxyPool.settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_KEY
from IPProxyPool.settings import INITIAL_SCORE, MIN_SCORE, MAX_SCORE
from random import choice


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host:  Redis地址
        :param port:  Redis端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，并设置分数
        :param proxy:   代理
        :param score:   分数
        :return:        添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+:\d+', proxy):
            logger.error('代理 {} 不符合规范, 丢弃'.format(proxy))
            return None
        if not self.db.zscore(REDIS_KEY, proxy):
            # 判断该代理不存在代理池中, 则将代理添加
            self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取代理，优先获取分数最高
        如果不存在则按照分数排名获取
        再不存在则抛出代理池为空异常

        zrangebyscore: 返回指定分数区间内的数据
        zrevrange: 返回指定区间内的数据，递减排序
        :return:
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理分数减一，小于最小值则删除该代理
        :param proxy:   代理
        :return:        修改后代理的分数

        zscore  返回有序集合key中指定成员的分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            logger.info('代理 {}, 当前分数 {}, 减一'.format(proxy, score))
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            logger.info('代理 {} 移除'.format(proxy))
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """判断代理是否存在"""
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理值设置为最大值
        :param proxy:   代理
        :return:        设置的结果
        """
        logger.info('代理 {} 设置为 {}'.format(proxy, MAX_SCORE))
        self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取代理数量
        :return:    代理数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return:    代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, end):
        """
        批量获取代理
        :param start:   开始索引
        :param end:     结束索引
        :return:        代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, end-1)


if __name__ == '__main__':
    client = RedisClient()
    print(client.batch(100, 200))