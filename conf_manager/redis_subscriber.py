import gevent
import logging
import redis


class RedisSubscriber(object):

    redis_host = None
    redis_port = None
    redis_section = None
    redis_callbacks = []
    redis_logger = logging.getLogger('redis')

    def set_connection(self, *args, **kwargs):
        self.redis = redis.StrictRedis(host=self.redis_host,
                                       port=self.redis_port)

    def subscribe(self):
        channel = {
            '__keyspace@0__:{0}'.format(self.redis_section): self.set_data
        }
        self.redis_pub_sub = self.redis.pubsub(ignore_subscribe_messages=True)
        self.redis_pub_sub.subscribe(**channel)

    def listen(self):
        while True:
            try:
                self.redis_pub_sub.get_message()
                gevent.sleep(0.1)
            except redis.ConnectionError as e:
                self.redis_logger.error(e.message)
                raise

    def set_data(self, event_data=None):
        data = self.redis.hgetall(self.redis_section)
        self.redis_logger.info(
                'Received redis data: {0}'.format(data))
        if data:
            for cb in self.redis_callbacks:
                cb(data)

    def start(self):
        try:
            self.set_connection()
            self.set_data()
            self.subscribe()
            gevent.spawn(self.listen).join()
        except redis.ConnectionError as e:
            self.redis_logger.error(
                    '{0} Will retry in 5 seconds.'.format(e.message))
            gevent.sleep(5)
            gevent.spawn(self.start).join()
