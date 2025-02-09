import os
from dotenv import load_dotenv
from typing import Final

class GlobalConfig:

    load_dotenv()

    # APPLICATION
    APPLICATION_ID: Final = os.getenv('APPLICATION_ID')
    
    # DISCORD
    DISCORD_TOKEN: Final = os.getenv('DISCORD_TOKEN')
    DISCORD_CHANNEL_ID: Final = os.getenv('DISCORD_CHANNEL_ID')

    # JELLYFIN
    JELLYFIN_HOST: Final = os.getenv('JELLYFIN_HOST', 'localhost')
    JELLYFIN_PORT: Final = os.getenv('JELLYFIN_PORT', '8096')
    JELLYFIN_API_KEY: Final = os.getenv('JELLYFIN_API_KEY')
    ADMIN_USER_ID: Final = os.getenv('ADMIN_USER_ID')

    def __init__(self):
        raise RuntimeError("Cette classe ne doit pas être instanciée")

    @staticmethod
    def validate_config(cls):
        required_vars = ['DISCORD_TOKEN','DISCORD_CHANNEL_ID','JELLYFIN_HOST','JELLYFIN_PORT']
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"La variable d'environnement {var} est requise")