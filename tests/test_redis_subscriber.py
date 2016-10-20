import unittest

import mock
import redis

from conf_manager import redis_subscriber as redis_subscriber_lib


class RedisSubscriberTest(unittest.TestCase):

    def setUp(self):
        self.redis_subscriber = redis_subscriber_lib.RedisSubscriber()
        self.redis_subscriber.redis_host = 'myhost'
        self.redis_subscriber.redis_port = 8888
        self.redis_subscriber.redis_section = 'section'
        self.my_cb = mock.Mock()
        self.redis_subscriber.redis_callbacks = [self.my_cb]

    @mock.patch('conf_manager.redis_subscriber.redis', autospec=True)
    def test_set_connection(self, redis_mock):
        self.redis_subscriber.set_connection()

        redis_mock.StrictRedis.assert_called_with(
                host='myhost',
                port=8888)

    def test_subscribe(self):
        self.redis_subscriber.redis = mock.Mock(spec=redis.StrictRedis)
        pubsub_mock = mock.Mock(spec=redis.client.PubSub)
        self.redis_subscriber.redis.pubsub.return_value = pubsub_mock

        self.redis_subscriber.subscribe()

        self.redis_subscriber.redis.pubsub.assert_called_with(
                ignore_subscribe_messages=True)
        pubsub_mock.subscribe.assert_called_with(
                **{'__keyspace@0__:section': self.redis_subscriber.set_data})

    @mock.patch('conf_manager.redis_subscriber.logging', autospec=True)
    @mock.patch('conf_manager.redis_subscriber.gevent', autospec=True)
    def test_listen(self, gevent_mock, logging_mock):
        self.redis_subscriber.redis_pub_sub = mock.Mock(
                spec=redis.client.PubSub, autospec=True)
        gevent_mock.sleep.side_effect = redis.ConnectionError('error')

        self.assertRaises(redis.ConnectionError, self.redis_subscriber.listen)

        self.redis_subscriber.redis_pub_sub.get_message.assert_called()
        gevent_mock.sleep.assert_called_with(0.1)
        logging_mock.error.assert_called_with('error')

    def test_set_data(self):
        self.redis_subscriber.redis = mock.Mock(spec=redis.StrictRedis)
        self.redis_subscriber.redis.hgetall.return_value = 'test'

        self.redis_subscriber.set_data()

        self.redis_subscriber.redis.hgetall.assert_called_with('section')
        self.my_cb.assert_called_with('test')

    @mock.patch('conf_manager.redis_subscriber.redis', autospec=True)
    @mock.patch('conf_manager.redis_subscriber.logging', autospec=True)
    @mock.patch('conf_manager.redis_subscriber.gevent', autospec=True)
    def test_start(self, gevent_mock, logging_mock, redis_mock):
        self.redis_subscriber.start()

        gevent_mock.spawn.assert_called_with(self.redis_subscriber.listen)
        gevent_mock.spawn.return_value.join.assert_called()

    @mock.patch('conf_manager.redis_subscriber.logging', autospec=True)
    @mock.patch('conf_manager.redis_subscriber.gevent', autospec=True)
    def test_start_connection_error(
            self, gevent_mock, logging_mock):

        self.redis_subscriber.set_connection = mock.Mock(
                side_effect=redis.ConnectionError('error'))
        self.redis_subscriber.start()

        logging_mock.error.assert_called_with('error')
        gevent_mock.sleep.assert_called_with(5)
        gevent_mock.spawn.assert_called_with(self.redis_subscriber.start)
        gevent_mock.spawn.return_value.join.assert_called()
