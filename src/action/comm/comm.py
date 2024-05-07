from threading import Thread

from kombu import Connection, Exchange

from .comm_consumer import CommConsumer
from .comm_error import CommError


class Comm:
    _consumers: list[CommConsumer] = list()

    def __init__(self, url: str):
        self._connection = Connection(url)
        self._connection.connect()

        self._connection: Optional[Connection] = None
        self._channel: Optional[any] = None
        self._exchanges: dict[CommTopic, Exchange] = dict()
        self._consumers: list[Consumer] = list()
        self._producers: dict[CommTopic, Producer] = list()
        self._listen_task: Optional[Task] = None

    def __enter__(self) -> "Comm":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

        # Let the exception propagate
        return False

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

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        for consumer in self._consumers:
            consumer.should_stop = True
        if self._connection and self._connection.connected:
            self._connection.release()

    def _check_connected(self):
        if not self._connection or not self._connection.connected:
            raise CommError("Not connected to the message broker")

    def subscribe(self, topic: str, callback: callable):
        self._check_connected()
        consumer = CommConsumer(self._connection, topic, callback)
        self._consumers.append(consumer)
        Thread(target=consumer.run).start()

    def publish(self, topic: str, data: any):
        self._check_connected()
        exchange = Exchange(name=topic, type="topic")
        producer = self._connection.Producer(exchange=exchange, serializer='json')
        producer.publish(data)
