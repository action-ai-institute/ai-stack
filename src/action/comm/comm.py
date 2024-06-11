import os
from threading import Thread

from kombu import Connection, Exchange

from .comm_consumer import CommConsumer
from .comm_error import CommError


class Comm:
    def __init__(self, url: str):
        self._consumers: list[CommConsumer] = list()
        self._connection: Connection = Connection(url)
        self._connection.connect()

    def __enter__(self) -> "Comm":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

        # Let the exception propagate
        return False

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
        producer = self._connection.Producer(exchange=exchange, serializer="json")
        producer.publish(data)


def local_comm():
    comm_password = os.environ.get("GLOBAL_COMM_PASSWORD")
    return Comm(f"amqp://agent:{comm_password}@10.0.8.88:5672")


def global_comm():
    comm_password = os.environ.get("GLOBAL_COMM_PASSWORD")
    comm_ip = os.environ.get("GLOBAL_COMM_IP")
    return Comm(f"amqp://agent:{comm_password}@{comm_ip}:5672")
