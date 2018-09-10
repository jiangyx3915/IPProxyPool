"""
主入口
"""
from IPProxyPool.scheduler import Scheduler


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()