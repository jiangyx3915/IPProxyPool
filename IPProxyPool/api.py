from flask import Flask, g, jsonify
from IPProxyPool.store import RedisClient

app = Flask(__name__)


def get_client():
    if not hasattr(g, 'client'):
        g.client = RedisClient()
    return g.client


def success_response(data):
    return {
        'code': 200,
        'message': '成功返回',
        'data': data
    }


@app.route('/')
def index():
    return '<h1 style="text-align: center">Welcome to IP Proxy Pool System</h1>'


@app.route('/random')
def get_random_proxy():
    """随机获取一个代理"""
    client = get_client()
    return jsonify(success_response(client.random()))


@app.route('/count')
def get_proxy_count():
    """获取代理池总量"""
    client = get_client()
    return jsonify(success_response(client.count()))


if __name__ == '__main__':
    app.run()
