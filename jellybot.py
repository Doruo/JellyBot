import discord
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

class JellyfinBot(commands.Bot):

    def __init__(self, jellyfin_url, api_key):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.jellyfin_url = jellyfin_url
        self.api_key = api_key
        self.last_episodes = set()

    async def setup_hook(self):
        self.check_jellyfin.start()

    def cog_unload(self):
        self.check_jellyfin.cancel()

    async def show_jellyfin_status(self, server_status):
        server_status_color = ":green_circle:" if server_status == 'started' else ":red_circle:"  
        await self.send_server_notification(f"Status serveur: {server_status} {server_status_color}")

    @tasks.loop(minutes=15)
    async def check_jellyfin(self):
        try:
            # Vérifier le statut du serveur
            server_status = self.check_server_status()
            await self.show_jellyfin_status(server_status)
  
            # Vérification nouveaux épisodes
            new_episodes = await self.get_new_episodes()

            for episode in new_episodes:
                await self.send_episode_notification(episode)
        
        except Exception as e:
            print(f"Erreur lors de la vérification Jellyfin : {e}")


    # Vérifie le statut du serveur
    def check_server_status(self):
        try:
            response = requests.get(f"{self.jellyfin_url}/System/Ping", headers={'X-Emby-Token': self.api_key},timeout=5)
            return 'started' if response.status_code == 200 else 'stopped'
        except requests.exceptions.RequestException:
            return 'stopped'

    async def get_new_episodes(self):

        headers = {'X-Emby-Token': self.api_key}
        response = requests.get(f"{self.jellyfin_url}/Users/277241eb1aca499ebb408bce16393bea/Items/Latest", headers=headers)

        resultat = response.json()

        if resultat.success :
            episodes = resultat.get('Items', [])
 
            new_episodes = [
                ep for ep in episodes 
                if ep['Id'] not in self.last_episodes
            ]

            self.last_episodes.update(ep['Id'] for ep in new_episodes)
            return new_episodes
        else : 
            return False

    # Envoie une notification par message au canal du serveur discord
    async def send_server_notification(self, message):
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        await channel.send(message)

    # Envoie une notification concernant un nouvelle épisode au canal du serveur discord
    async def send_episode_notification(self, episode):
        channel = self.get_channel(DISCORD_CHANNEL_ID)

        embed = discord.Embed(
            title="Nouvel épisode disponible !",
            description=f"{episode['Name']} - {episode['SeriesName']}",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

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