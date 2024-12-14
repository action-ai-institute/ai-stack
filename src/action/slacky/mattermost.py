from mattermostdriver import Driver
import os

def local_mattermost():
    return Mattermost(
        server=os.environ.get("LOCAL_ACTION_SERVER"),
        password=os.environ.get("LOCAL_ACTION_PASSWORD"),
    )

def global_mattermost():
    return Mattermost(
        server=os.environ.get("GLOBAL_ACTION_SERVER"),
        password=os.environ.get("GLOBAL_ACTION_PASSWORD"),
    )

class Mattermost:
    def __init__(self, server=None, password=None):
        self.password = password
        self.server = server
        self.driver = None
        self.login()

    def login(self):
        self.driver = Driver(
            {
                "url": self.server,
                "login_id": "admin",
                "password": self.password,
                "scheme": "http",
                "port": 8065,
                "basepath": "/api/v4",
                "verify": False,  # Or /path/to/file.pem
                "timeout": 30,
                "debug": False,
            }
        )
        self.driver.login()
        return self.driver

    def create_organization(self, organization):
        print("Creating organization")
        org = self.driver.teams.create_team(
            {"name": organization.lower(), "display_name": organization, "type": "I"}
        )
        # Now add admin to the organization
        user = self.driver.users.get_user_by_username("admin")
        self.driver.teams.add_user_to_team(
            org["id"], {"user_id": user["id"], "team_id": org["id"]}
        )
        self.driver.teams.update_team_member_roles(
            org["id"], user["id"], {"roles": "team_user team_admin"}
        )

    def get_organization(self, organization):
        team = None
        try:
            team = self.driver.teams.get_team_by_name(organization)
        except:
            self.create_organization(organization)
            team = self.driver.teams.get_team_by_name(organization)
        return Organization(team["id"], self)

    def enable_bot(self):
        config = self._get_current_config()
        config["ServiceSettings"]["EnableBotAccountCreation"] = True
        self._update_config(config)

    def _get_current_config(self):
        response = self.driver.client.make_request(
            method="get",
            endpoint="/config",
        )
        return response.json()

    def _update_config(self, new_config):
        response = self.driver.client.make_request(
            method="put",
            endpoint="/config",
            options=new_config,
        )
        return response.json()


class Organization:
    def __init__(self, id, parent):
        self.id = id
        self._parent: Mattermost = parent
        self.bots = {}

    def create_bot(self, name):
        bot = self._parent.driver.client.make_request(
            method="post",
            endpoint="/bots",
            options={
                "username": name.lower(),
                "display_name": name,
                "description": name + " bot",
            },
        ).json()
        return bot

    def add_bot_to_team(self, bot_id):
        self._parent.driver.teams.add_user_to_team(
            self.id, {"user_id": bot_id, "team_id": self.id}
        )

    def is_bot_in_team(self, bot_id):
        response = self._parent.driver.client.make_request(
            method="get", endpoint=f"/teams/{self.id}/members"
        )
        members = response.json()
        for member in members:
            if member["user_id"] == bot_id:
                return True
        return False

    def _get_bot_token(self, bot_id, clear=False):
        if clear:
            response = self._parent.driver.client.make_request(
                method="get", endpoint=f"/users/{bot_id}/tokens"
            ).json()
            for token in response:
                self._parent.driver.client.make_request(
                    method="post",
                    endpoint=f"/users/{bot_id}/tokens/revoke",
                    options={"token_id": token["id"]},
                )
        token = self._parent.driver.users.create_user_access_token(
            bot_id, {"description": "bot token"}
        )
        return token["token"]

    def get_bot(self, name):
        if name in self.bots:
            return self.bots[name]
        response = self._parent.driver.client.make_request(
            method="get", endpoint="/bots"
        )
        bots = response.json()
        b = None
        for bot in bots:
            if bot["username"] == name:
                b = bot
                break
        if b is None:
            b = self.create_bot(name)

        if not self.is_bot_in_team(b["user_id"]):
            self.add_bot_to_team(b["user_id"])
        token = self._get_bot_token(b["user_id"])
        bot = Bot(b["user_id"], token, self)
        self.bots[name] = bot
        return bot


class Bot:
    def __init__(self, id, token, parent):
        self.id = id
        self.token = token
        self._parent: Organization = parent
        self.driver = Driver(
            {
                "url": self._parent._parent.server,
                "scheme": "http",
                "token": self.token,
                "port": 8065,
                "basepath": "/api/v4",
                "verify": False,
                "timeout": 30,
                "debug": False,
                "auth": None,
            }
        )

        self.driver.client.token = self.token

    def get_token(self):
        return self.token

    def get_channels(self):
        response = self.driver.teams.get_public_channels(self._parent.id)
        return response

    def send_in_channel(self, channel_id, message):
        self.driver.posts.create_post(
            {
                "channel_id": channel_id,
                "message": message,
            }
        )
        return True

    def on_message(self, callback):
        self.driver.init_websocket(callback)