# ai-stack

| Submodule            | Description              |
| -------------------- | ------------------------ |
| `comm`               | Inter-agent event system |
| `knowledge_base`     |                          |
| `learning_reasoning` |                          |
| `strategy_planning`  |                          |
| `agent_agent`        |                          |
| `human_agent`        |                          |

## comm

Local RabbitMQ instance:

```shell
docker run -p 5672:5672 -d --hostname action-rabbit --name action-rabbit rabbitmq:3
```

Example usage:

```python
from action.comm import Comm

comm = Comm("amqp://localhost:5672")       # Use local or global instance url
comm.subscribe(
    topic="auditd",                        # One topic (category) per agent
    callback=lambda msg: print(msg.body),  # Data can be str, JSON, or pickle
)
comm.publish(
    topic="auditd",                 
    data="/etc/passwd changed :O",
)
# Do your thing...
comm.disconnect()
```
