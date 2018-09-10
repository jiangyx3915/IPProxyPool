"""
代理池调度器
"""
import time
from multiprocessing import Process
from IPProxyPool.settings import TESTER_CYCLE, GETTER_CYCLE, ENABLE_TESTER, ENABLE_GETTER, ENABLE_API
from IPProxyPool.settings import API_HOST, API_PORT
from IPProxyPool.tester import Tester
from IPProxyPool.getter import Getter
from IPProxyPool.api import app
from IPProxyPool.logger import logger


class Scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """定时测试代理"""
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """定时获取代理"""
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """开启API支持"""
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        logger.info("代理池开始运行")
        if ENABLE_TESTER:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if ENABLE_GETTER:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if ENABLE_API:
            api_process = Process(target=self.schedule_api)
            api_process.start()
