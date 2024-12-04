from jinja2 import Environment, FileSystemLoader
import os, sys, subprocess, shutil

ACTION_SERVER_PASSWORD = "f9sdhtg97ht4938hgf9d7sgh"
OPENAI_API_KEY = "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"
DEPLOYMENT_PATH = os.getcwd() + "/deployment"

# If the deployment directory does not exist, create it

required_dirs = [
    DEPLOYMENT_PATH,
    f"{DEPLOYMENT_PATH}/litellm",
    f"{DEPLOYMENT_PATH}/mattermost",
    f"{DEPLOYMENT_PATH}/neo4j",
    f"{DEPLOYMENT_PATH}/mattermost/config",
]

compose_files = [
    "litellm_docker_compose.yml",
    "mattermost_docker_compose.yml",
    "neo4j_docker_compose.yml",
    "rabbitmq_docker_compose.yml",
]

data = {
    "local_action_password": ACTION_SERVER_PASSWORD,
    "deployment_path": DEPLOYMENT_PATH,
    "OPENAI_API_KEY": OPENAI_API_KEY,
}

mapping = {
    "litellm_config.yaml": {"dest": "litellm/config.yaml"},
    "mattermost_config.json": {
        "dest": "mattermost/config/config.json",
        "user": 2000,
        "group": 2000,
    },
    "mattermost.env": {"dest": ".env"},
}

socket_dirs = [
    {"path": f"{DEPLOYMENT_PATH}/mattermost/tmp", "user": 2000, "group": 2000},
]


def init():
    if not os.path.exists(DEPLOYMENT_PATH):
        for dir in required_dirs:
            os.makedirs(dir)
    else:
        print("Deployment directory already exists. Exiting.")
        print("You can use the up command to start the services.")
        print(
            "For a redeployment, please use the clean command to remove the existing deployment."
        )
        exit()

    # iterate over the templates directory and render each file
    env = Environment(loader=FileSystemLoader("templates"))
    for template in compose_files:
        with open(f"{DEPLOYMENT_PATH}/{template}", "w") as f:
            f.write(env.get_template(template).render(data))

    for template, output in mapping.items():
        with open(f"{DEPLOYMENT_PATH}/{output['dest']}", "w") as f:
            f.write(env.get_template(template).render(data))
        if "user" in output or "group" in output:
            os.chown(
                f"{DEPLOYMENT_PATH}/{output['dest']}", output["user"], output["group"]
            )

    for dir in socket_dirs:
        if not os.path.exists(dir["path"]):
            os.makedirs(dir["path"])
        os.chown(dir["path"], dir["user"], dir["group"])

    print("Deployment initialized, please run 'up' to start the services.")
    print(
        "To access your deployed services, please export the following environment variables:"
    )
    print(f"export LOCAL_ACTION_SERVER=127.0.0.1")
    print(f"export LOCAL_ACTION_PASSWORD={ACTION_SERVER_PASSWORD}")


def up():
    # Run the docker-compose commands
    cmd = ["docker", "compose"]
    for compose_file in compose_files:
        cmd.extend(["-f", f"{DEPLOYMENT_PATH}/{compose_file}"])
    cmd.extend(["up", "-d"])
    subprocess.run(cmd, cwd=DEPLOYMENT_PATH)


def down():
    cmd = ["docker", "compose"]
    for compose_file in compose_files:
        cmd.extend(["-f", f"{DEPLOYMENT_PATH}/{compose_file}"])
    cmd.extend(["down"])
    subprocess.run(cmd, cwd=DEPLOYMENT_PATH)


def clean():
    if os.path.exists(DEPLOYMENT_PATH):
        shutil.rmtree(DEPLOYMENT_PATH)
    else:
        print("Deployment directory does not exist. Exiting.")
        exit()


def main():
    if len(sys.argv) != 2:
        print("Invalid number of arguments. Please use 'up' or 'down'.")
        exit()

    if os.geteuid():
        print("This script must be run as root.")
        exit()
    if sys.argv[1] == "up":
        up()
    elif sys.argv[1] == "down":
        down()
    elif sys.argv[1] == "init":
        init()
    elif sys.argv[1] == "clean":
        clean()
    else:
        print("Invalid command. Please use 'up' or 'down'.")


if __name__ == "__main__":
    main()
