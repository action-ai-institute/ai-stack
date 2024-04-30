from kombu import Consumer, Exchange, Queue
from kombu.mixins import ConsumerMixin


class CommConsumer(ConsumerMixin):
    def __init__(self, connection, topic, callback):
        self.connection = connection
        self._topic = topic
        self._callback = callback

    def get_consumers(self, _, channel):
        exchange = Exchange(name=self._topic, type="topic", channel=channel)
        queue = Queue(exchange=exchange)
        consumer = Consumer(channel=channel, queues=[queue], on_message=self._callback)
        return [consumer]
