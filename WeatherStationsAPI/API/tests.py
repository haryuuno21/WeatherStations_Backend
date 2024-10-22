import redis
r = redis.Redis(host='localhost', port=6380, db=0)
r.set('somekey', '1000-7') # сохраняем ключ 'somekey' с значением '1000-7!'
value = r.get('somekey') # получаем значение по ключу
print(value)
