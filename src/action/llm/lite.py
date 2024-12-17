import litellm
import os
action_password = os.environ.get("LOCAL_ACTION_PASSWORD")
action_server = os.environ.get("LOCAL_ACTION_SERVER")
litellm.api_base = f"http://{action_server}:4000"
litellm.api_key = f"sk-{action_password}"