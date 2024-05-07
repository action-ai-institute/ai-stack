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

# Use local or global instance url
comm = Comm("amqp://localhost:5672")

comm.subscribe("agent_a", lambda msg: print(msg))
comm.subscribe("agent_b", lambda msg: print(msg["foo"]))
comm.publish("agent_a", "bar")
comm.publish("agent_b", {"foo": "bar"})

comm.disconnect()
```
