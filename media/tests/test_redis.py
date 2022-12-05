from django.test import TestCase
from redis import Redis


class TestRedis(TestCase):

    def test_redis_connection(self):

        redis_host = '127.0.0.1'
        r = Redis(redis_host, socket_connect_timeout=1, password='134tGfhdX')
        try:
            r.ping()
            print("redis connection is valid")
        except:
            self.assertFalse()
