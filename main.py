
from src.bot import JellyfinBot
from config.globals import GlobalConfig

print("Validating global config...")
GlobalConfig.validate_config(GlobalConfig)

print("Importing global values...")

# APPLICATION
APPLICATION_ID = GlobalConfig.APPLICATION_ID
# Jellyfin
JELLYFIN_HOST = GlobalConfig.JELLYFIN_HOST
JELLYFIN_PORT = GlobalConfig.JELLYFIN_PORT
JELLYFIN_API_KEY = GlobalConfig.JELLYFIN_API_KEY
# Admin User ID
ADMIN_USER_ID = GlobalConfig.ADMIN_USER_ID
# DISCORD
DISCORD_CHANNEL_ID = GlobalConfig.DISCORD_CHANNEL_ID
DISCORD_TOKEN = GlobalConfig.DISCORD_TOKEN


print("Starting bot...")
bot = JellyfinBot (JELLYFIN_HOST, JELLYFIN_PORT, JELLYFIN_API_KEY, ADMIN_USER_ID, DISCORD_CHANNEL_ID,APPLICATION_ID)

print("Binding Discord commands...")
@bot.command(name="state")
async def state(ctx):
    await bot.state(ctx)
@bot.command(name="latest")
async def latest(ctx):
    await bot.latest(ctx)

print("Connecting to Discord...")
bot.run(DISCORD_TOKEN)
