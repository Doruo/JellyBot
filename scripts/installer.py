#!/usr/bin/env python3

import subprocess
from pathlib import Path

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

# Input environnement
def get_env_varss_input():
    
    print("""
    Welcome to the JellyBot - Jellyfin Discord Bot installer
    More docs at: [https://github.com/Doruo/JellyBot#installation]
    """)

    print("\n----------Jellyfin----------\n")

    protocol = input("Protocol (http/https): ")
    host = input("Hostame: ")
    port = input("Port: ")
    url = f'{protocol}://{host}:{port}'

    print(f"Jellyfin Server url: {url}")

    username = input("Username: ")

    api_key = input(f"API key [Create one here: {url}/web/index.html#!/apikeys.html]: ")

    print ("To find your admin user id : connect to your jellyfin website as Admin > Left Panel > Users > your user, and copy the user Id from the url")
    admin_user_id = input("Admin User ID: ")

    print("\n----------Discord----------\n")

    app_id = input("Application ID: ")
    discord_token = input("Discord Token: ")
    discord_channel_id = input("Discord Channel ID: ")

    env_vars = {
        'PROTOCOL': protocol,
        'HOST': host,
        'PORT': port,
        'URL': url,
        'USERNAME': username,
        'API_KEY': api_key,
        'ADMIN_USER_ID': admin_user_id,
        'APP_ID': app_id,
        'DISCORD_TOKEN': discord_token,
        'DISCORD_CHANNEL_ID': discord_channel_id
    }

    return env_vars

# Configure environnement from parameters
def create_env_file(env_vars: set):
    
    # Get the directory where the current script is located (scripts folder)
    current_script_path = Path(__file__).resolve()
    project_root = current_script_path.parent.parent
        
    # Create config directory if it doesn't exist
    config_dir = project_root / "config"
    config_dir.mkdir(exist_ok=True)

    # Create .env file in config directory
    env_path = config_dir / ".env"

    # Try creating .env with environment variables given in the correct folder
    try:
        with open(env_path, "w") as file:
            
            # write environment variables
            # Jellyfin environment variables
            file.write("# JELLYFIN\n")

            # Jellyfin server url
            file.write(f"JELLYFIN_PROTOCOL={env_vars['PROTOCOL']}\n")
            file.write(f"JELLYFIN_HOST={env_vars['HOST']}\n")
            file.write(f"JELLYFIN_PORT={env_vars['PORT']}\n")

            # Jellyfin API
            file.write(f"JELLYFIN_API_KEY={env_vars['API_KEY']}\n")

            # Jellyfin admin user
            file.write(f"ADMIN_USER_ID={env_vars['ADMIN_USER_ID']}\n")
            file.write(f"ADMIN_USERNAME={env_vars['USERNAME']}\n")

            # Discord environment variables
            file.write("# DISCORD\n")

            # Discord Bot Application
            file.write(f"APPLICATION_ID={env_vars['APP_ID']}\n")
            file.write(f"DISCORD_TOKEN={env_vars['DISCORD_TOKEN']}\n")

            # Discord Text Channel ID
            file.write(f"DISCORD_CHANNEL_ID={env_vars['DISCORD_CHANNEL_ID']}\n")
        
        print(f"Successfully created .env file at: {env_path}")

        bot_start_wanted = confirm(
            message="Do you want to start the bot ?", default=True, direct=True
        )

        if bot_start_wanted == True:
            start_bot()


    except Exception as e:
        print(f"Error creating .env file: {e}")

def start_bot():
    subprocess.run["python3","../scripts/run.bash"]

def configure():
    env_vars = get_env_varss_input()
    create_env_file(env_vars)

def install():
    configure()
    
install()