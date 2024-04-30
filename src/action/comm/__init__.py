"""
Inter-agent event system

Example usage:

```
from action.comm import Comm

def my_callback(body, message):
    print(f"Received message: {body['message']}")
    message.ack()

with Comm("amqp://guest:guest@localhost:5672//") as comm:
    comm.publish(
        topic=CommTopic.LOG,           # General category
        routing_key="auditd",          # Agent-specific queue
        data="/etc/passwd changed :O", # Can be str, JSON, or pickle
    )
    comm.subscribe(
        topic=CommTopic.LOG,
        routing_key="auditd.#",  # Wildcards are supported ('*' for single words separated by '.', or rest of key with '#')
        callback=my_callback,
    )
    comm.block_indefinitely()  # Optional; removes the need for a `while True: sleep()`
```
"""

from .comm import Comm
from .comm_error import CommError
from .comm_topic import CommTopic
