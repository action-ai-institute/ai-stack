"""
Inter-agent event system

Example usage:

```
from action.comm import Comm

def my_callback(body, message):
    print(f"Received message: {body['message']}")
    message.ack()

# Change the URL to match the intranet or global instance 
with Comm("amqp://guest:guest@localhost:5672//") as comm:
    comm.publish(
        topic="auditd",                 # One "topic" (category) per agent
        data="/etc/passwd changed :O",  # Can be str, JSON, or pickle
    )
    comm.subscribe(
        topic="auditd",
        callback=my_callback,
    )
    comm.block_indefinitely()  # Optional; removes the need for a `while True: sleep()`
```
"""

from .comm import Comm
from .comm_error import CommError
