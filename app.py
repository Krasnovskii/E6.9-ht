from flask import Flask
from pymemcache.client.base import Client


app = Flask(__name__)
client = Client(('memcached', 11211))

def calc_fibo(n: int, cache_hits: list):
    if n in [0, 1]:
        return n
    c = client.get(str(n))
    if c:
        cache_hits.append(f'Hit cache on {n}')
        return int(c)
    else:
        f = calc_fibo(n-2, cache_hits) + calc_fibo(n-1, cache_hits)
        client.set(str(n), str(f))
        return f

@app.route('/<int:n>')
def fibo(n: int):
    if n < 0:
        return 'Wrong number'
    try:
        cache_hits = []
        res = f'Fibonacci number {n} is {calc_fibo(n, cache_hits)}<br><br><br>' + '<br>'.join(cache_hits)
    except RecursionError:
        res = 'Number is to large. Please try a smaller number to build up the cache. Thank you.'
    return res

@app.route('/')
def hello():
    return 'Hello, this is the Fibonacci number calculator with cache. Enter /n in address bar to get nth Fibo number (n should be positive int)'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')