"""
自定义异常
"""


class PoolEmptyError(Exception):
    """代理池为空异常"""
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("代理数量为空")