import os
import time
import logging

# 创建logger实例，如果参数为空则返回root logger
logger = logging.getLogger('letter')
# 设置总日志级别
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(filename)s[line:%(lineno)d] - <%(threadName)s %(thread)d>' +
    '- <Process %(process)d> - %(levelname)s: %(message)s'
)
basedir = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(basedir, 'logs')
if not os.path.isdir(log_path):
    os.mkdir(log_path)

# 创建日志文件fileHandler
# 日志文件名，以当前时间命名
filename = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
file_handler = logging.FileHandler(os.path.join(log_path, filename))
# 设置日志格式
file_handler.setFormatter(formatter)
# 单独为fileHandler设置日志级别，如果不设置则默认为总日志级别
file_handler.setLevel(logging.INFO)

# 创建控制台日志StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# 将handler添加到logger中
logger.addHandler(file_handler)
logger.addHandler(stream_handler)