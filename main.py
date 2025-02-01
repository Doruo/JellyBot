import os
from dotenv import load_dotenv
from src.bot import JellyfinBot

# /-/-/-/-/ MAIN /-/-/-/-/

load_dotenv()
# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
JELLYFIN_URL = os.getenv('JELLYFIN_URL')
# ID du canal Discord utilisé par le bot
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
JELLYFIN_API_KEY = os.getenv('JELLYFIN_API_KEY')
# Admin user ID
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')

bot = JellyfinBot(JELLYFIN_URL, JELLYFIN_API_KEY)

@bot.event
async def on_ready():
    print(f'Bot connecté : {bot.user}')

# /-/-/-/-/ GESTION DES COMMANDES /-/-/-/-/

## COMMANDE: STATUS
@bot.command(name="status")
async def status(ctx):

    server_status = bot.check_server_status()

    server_status_msg = "en marche" if server_status == 'started' else "éteind"
    server_status_color = ":green_circle:" if server_status == 'started' else ":red_circle:"

    await ctx.send(f"{server_status_color} ~ Server {server_status_msg} !")

## COMMANDE: NEW
@bot.command(name="new")
async def new (ctx) :

    new_episodes = await bot.get_new_episodes()

    if not new_episodes:
        await ctx.send("Aucun réponse du serveur.")

    else :
        await ctx.send("Nouveaux épisodes disponibles: ")
        for episode in new_episodes :
            await ctx.send(f"{episode['Name']} - {episode['SeriesName']}")

# /-/-/-/-/-----------------------/-/-/-/-/

bot.run(DISCORD_TOKEN)