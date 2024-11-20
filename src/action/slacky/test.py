from mattermost import *
import os
import json

# os.environ["LOCAL_ACTION_PASSWORD"] = ""
# os.environ["LOCAL_ACTION_SERVER"] = "127.0.0.1"

client = Mattermost()

client.enable_bot()

org = client.get_organization("Test1")
bot = org.get_bot("bot1")

chan = bot.get_channels()

bot.send_in_channel(chan[0]["id"], "Hello World")


def test_wrapper(a):
    msg = json.loads(a)
    print(msg)
    if msg["type"] == "posted":
        bot.send_in_channel(chan[0]["id"], msg["data"]["post"]["message"])


async def test(a):
    msg = json.loads(a)
    if "event" not in msg:
        return
    if msg["event"] == "posted":
        post = msg["data"]["post"]
        post_obj = json.loads(post)
        # print(msg)
        # print(post_obj["message"])
        if post_obj["user_id"] != bot.id:
            bot.send_in_channel(chan[0]["id"], "You said: " + post_obj["message"])
        # bot.send_in_channel(chan[0]["id"], post_obj["message"])


bot.on_message(test)

print(chan)
