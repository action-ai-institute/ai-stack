import openai
import os
    
def local_openai():
    action_password = os.environ.get("LOCAL_ACTION_PASSWORD")
    action_server = os.environ.get("LOCAL_ACTION_SERVER")
    return openai.OpenAI(api_key=f"sk-{action_password}",base_url=f"http://{action_server}:4000")
