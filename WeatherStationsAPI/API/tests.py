import redis
r = redis.Redis(host='localhost', port=6380, db=0)
for key in r.keys():
    print(key,r.get(key))
