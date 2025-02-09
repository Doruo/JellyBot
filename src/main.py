import sys
import os

# Add parent path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot import JellyfinBot
from config.globals import GlobalConfig

print("Validating global config...")
GlobalConfig.validate_config(GlobalConfig)

print("Importing global values...")

# DISCORD
APPLICATION_ID = GlobalConfig.APPLICATION_ID
DISCORD_CHANNEL_ID = GlobalConfig.DISCORD_CHANNEL_ID
DISCORD_TOKEN = GlobalConfig.DISCORD_TOKEN
# Jellyfin
JELLYFIN_PROTOCOL = GlobalConfig.JELLYFIN_PROTOCOL
JELLYFIN_HOST = GlobalConfig.JELLYFIN_HOST
JELLYFIN_PORT = GlobalConfig.JELLYFIN_PORT
JELLYFIN_API_KEY = GlobalConfig.JELLYFIN_API_KEY
ADMIN_USER_ID = GlobalConfig.ADMIN_USER_ID

print("Starting bot...")
bot = JellyfinBot (JELLYFIN_PROTOCOL, JELLYFIN_HOST, JELLYFIN_PORT, JELLYFIN_API_KEY, ADMIN_USER_ID, DISCORD_CHANNEL_ID,APPLICATION_ID)

print("Binding Discord commands...")
@bot.command(name="state")
async def state(ctx):
    await bot.state(ctx)
@bot.command(name="latest")
async def latest(ctx):
    await bot.latest(ctx)

print("Connecting to Discord...")
bot.run(DISCORD_TOKEN)
