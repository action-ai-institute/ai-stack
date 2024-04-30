from enum import Enum
from typing import Optional
from kombu import Connection, Exchange, Queue, Consumer, Producer
import asyncio
from asyncio import Task


class CommError(Exception):
    pass


class CommTopic(str, Enum):
    POTENTIAL_ATTACK = "potential_attack"
    LOG = "log"


class Comm:
    def __init__(self, url: str):
        self._url: str = url

        self._connection: Optional[Connection] = None
        self._channel: Optional[any] = None
        self._exchanges: dict[CommTopic, Exchange] = dict()
        self._consumers: list[Consumer] = list()
        self._producers: dict[CommTopic, Producer] = list()
        self._listen_task: Optional[Task] = None

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def _ensure_connected(self):
        if not self._connection:
            raise CommError(
                "Never connected to the message broker. Did you forgot to `connect`?"
            )
        if not self._connection.connected:
            raise CommError("Connection to the message broker was lost.")

    def connect(self):
        if not self._connection or not self._connection.connected:
            self._connection = Connection(self._url)
            self._channel = self._connection.channel()

            async def consume_events():
                while True:
                    self._connection.drain_events()
            
            self._listen_task = asyncio.create_task(consume_events())

    def disconnect(self):
        if self._listen_task:
            self._listen_task.cancel()

        if self._connection and self._connection.connected:
            self._connection.release()
            self._channel = None
            self._exchanges.clear()
            self._consumers.clear()
            self._producers.clear()

    def block_forever(self):
        asyncio.wait_for(self._listen_task, None)

    def _get_exchange(self, topic: CommTopic) -> Exchange:
        exchange = self._exchanges.get(topic)
        if not exchange:
            exchange = Exchange(topic, type="topic", durable=True)
            exchange.declare(self._channel)
            self._exchanges[topic] = exchange
        return exchange
    
    def _get_producer(self, topic: CommTopic) -> Producer:
        producer = self._producers.get(topic)
        if not producer:
            exchange = self._get_exchange(topic)
            producer = Producer(self._channel, exchange=exchange)
            self._producers[topic] = producer
        return producer

    def subscribe(self, topic: CommTopic, routing_key: str, callback: callable):
        self._ensure_connected()

        exchange = self._get_exchange(topic)
        queue = Queue(exchange=exchange, routing_key=routing_key, durable=True)
        queue.declare(self._channel)
        consumer = Consumer(self._channel, queues=[queue], callbacks=[callback])
        self._consumers.append(consumer)

    def publish(self, topic: CommTopic, routing_key: str, data: any):
        self._ensure_connected()

        producer = self._get_producer(topic)
        producer.publish(data, routing_key=routing_key)
