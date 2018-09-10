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
POOL_MAX_THRESHOLD = 5000   # 代理池容量限制

BATCH_TEST_SIZE = 10        # 批量测试数量

# 检查周期配置
TESTER_CYCLE = 20           # 测试器运行周期
GETTER_CYCLE = 300          # 获取器运行周期

# 模块加载配置
ENABLE_TESTER = True        # 是否开启测试器
ENABLE_GETTER = True        # 是否开启获取器
ENABLE_API = True           # 是否开启API的支持

# api配置
API_HOST = '0.0.0.0'        # API 服务器地址
API_PORT = 5000             # API 服务器端口
