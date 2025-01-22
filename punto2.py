import redis
import time

class DistributedCache:
    def _init_(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value, ttl=None):
        self.client.set(name=key, value=value, ex=ttl)

    def get(self, key):
        return self.client.get(name=key)

    def invalidate(self, key):
        self.client.delete(key)

    def expire(self, key, ttl):
        self.client.expire(name=key, time=ttl)

# Uso del sistema de caché distribuido
cache = DistributedCache()

# Guardar un valor con una caducidad de 10 segundos
cache.set('mi_clave', 'mi_valor', ttl=10)
print(cache.get('mi_clave'))

# Esperar 11 segundos para que el valor caduque
time.sleep(11)
print(cache.get('mi_clave'))  # Debería ser None

# Invalidate cache entry
cache.set('mi_clave', 'nuevo_valor')
cache.invalidate('mi_clave')
print(cache.get('mi_clave'))  # Debería ser None