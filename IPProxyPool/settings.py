"""配置文件"""

# Redis 配置
REDIS_HOST = '127.0.0.1'    # Redis数据库地址
REDIS_PORT = 6379           # Redis端口
REDIS_PASSWORD = None       # Redis密码，如无填None
REDIS_KEY = 'proxies'       # 代理池redis键值

# 代理分数
INITIAL_SCORE = 10          # 初始化分数
MIN_SCORE = 0               # 最低分
MAX_SCORE = 100             # 最高分
