import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('name', 'John')
print(r['name'], r.get('name'))
