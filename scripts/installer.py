#!/usr/bin/env python3

import json
import os
import subprocess
import platform
import sys
from time import sleep

# Confirm Prompt
def confirm(message: str = "Continue", default: bool | None = None, direct: bool | None = None) -> bool:
    
    prompts = {True: "(Y/n)", False: "(y/N)", None: "(y/n)"}
    full_message = f"{message} {prompts[default]}: "

    valid_inputs = {
        "y": True, "Y": True, "ye": True, "yes": True, "Ye": True, "YE": True, "YES": True,
        "n": False, "N":False, "no": False, "No": False,"NO" : False
    }

    if default is not None:
        valid_inputs[""] = default
    
    while (response := input(full_message).strip().lower()) not in valid_inputs:
        print("Invalid input, please type y or n")

    output = valid_inputs[response]

    if direct is not None and not output:
        return None
    return output

# INSTALLATION START

path = ""

# OS CONFIG DETECTION
"""
    if platform.system() != "Windows":
        if os.environ.get("XDG_CONFIG_HOME"):
            path = os.environ["XDG_CONFIG_HOME"].removesuffix("/") + "/JellyBot/"
        else:
            path = os.environ["HOME"].removesuffix("/") + "/.config/JellyBot/"

        subprocess.run(["mkdir", "-p", path])
    else:
        path = os.environ["APPDATA"].removesuffix("\\") + "\\JellyBot\\"
        subprocess.run(
            ["powershell", "-Command", f'mkdir "{path}"'],
            stdout=subprocess.DEVNULL,
        )
"""

print("""
Welcome to the "JellyBot" Jellyfin Discord Bot installer
[https://github.com/Doruo/JellyBot#installation]
""")

print("----------Jellyfin----------")

protocol = input("http/https: ")
host = input("hostname: ")
port = input("port: ")
url = f'{protocol}://{host}:{port}'

print(f"url: {url}")

print("Enter a single username or enter multiple usernames in a comma separated list.")
username = input("username[s]: ").split(",")

self_signed_cert = None

if protocol == "https":
    self_signed_cert = confirm(
        message="Are you using a self signed certificate?", default=False, direct=True
        )

api_key = input(f"API key [Create one here: {url}/web/index.html#!/apikeys.html]: ")

print ("To find your admin user id : connect to your jellyfin website as Admin > Left Panel > Users > your user, and copy the user Id from the url")
admin_user_id = input("Admin User ID: ")

print("----------Discord----------")

app_id = input("Application ID: ")
discord_token = input("Discord Token: ")
discord_channel_id = input("Discord Channel ID: ")

f = open("../config/.env", "w")

f.write("# DISCORD\n")
f.write(f"APPLICATION_ID={app_id}\n")
f.write(f"DISCORD_TOKEN={discord_token}\n")
f.write(f"DISCORD_CHANNEL_ID={discord_channel_id}\n")

f.write("# JELLYFIN\n")
f.write(f"JELLYFIN_PROTOCOL={protocol}\n")
f.write(f"JELLYFIN_HOST={host}\n")
f.write(f"JELLYFIN_PORT={port}\n")
f.write(f"JELLYFIN_API_KEY={app_id}\n")
f.write(f"ADMIN_USER_ID={app_id}\n")
f.close()