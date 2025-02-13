import requests
import os

action_password = os.environ.get("LOCAL_ACTION_PASSWORD")
action_server = os.environ.get("LOCAL_ACTION_SERVER")
aptEndpoint = f"http://{action_server}:4000"
masterKey = f"sk-{action_password}"


def getKeyWithBudget(budget):
    response = requests.post(
        f"{aptEndpoint}/key/generate",
        headers={
            "Authorization": f"Bearer {masterKey}",
            "Content-Type": "application/json",
        },
        json={
            "max_budget": budget,
        },
    )
    if response.ok:
        return response.json()
    else:
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None
