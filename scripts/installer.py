#!/usr/bin/env python3

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
def get_env_vars_input():
    
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

    print("Enter a single username or enter multiple usernames in a comma separated list.")
    username = input("Username[s]: ").split(",")

    api_key = input(f"API key [Create one here: {url}/web/index.html#!/apikeys.html]: ")

    print ("To find your admin user id : connect to your jellyfin website as Admin > Left Panel > Users > your user, and copy the user Id from the url")
    admin_user_id = input("Admin User ID: ")

    print("\n----------Discord----------\n")

    app_id = input("Application ID: ")
    discord_token = input("Discord Token: ")
    discord_channel_id = input("Discord Channel ID: ")

    env_var = {
        protocol,host,port,url,username,api_key,admin_user_id,
        app_id,discord_token,discord_channel_id
    }
    
    return env_var

# Configure environnement from parameters
def create_env_file(env_var: set):
    
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
            file.write(f"JELLYFIN_PROTOCOL={env_var['protocol']}\n")
            file.write(f"JELLYFIN_HOST={env_var['host']}\n")
            file.write(f"JELLYFIN_PORT={env_var['port']}\n")

            # Jellyfin API
            file.write(f"JELLYFIN_API_KEY={env_var['api_key']}\n")

            # Jellyfin admin user
            file.write(f"ADMIN_USER_ID={env_var['admin_user_id']}\n")
            file.write(f"ADMIN_USERNAME={env_var['username']}\n")

            # Discord environment variables
            file.write("# DISCORD\n")

            # Discord Bot Application
            file.write(f"APPLICATION_ID={env_var['app_id']}\n")
            file.write(f"DISCORD_TOKEN={env_var['discord_token']}\n")

            # Discord Text Channel ID
            file.write(f"DISCORD_CHANNEL_ID={env_var['discord_channel_id']}\n")
        
        print(f"Successfully created .env file at: {env_path}")
        
    except Exception as e:
        print(f"Error creating .env file: {e}")

def configure():
    env_var = get_env_vars_input()
    create_env_file(env_var)

def install():
    configure()
    
install()