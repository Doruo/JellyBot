import discord
import requests
from discord.ext import commands, tasks

class JellyfinBot(commands.Bot):

    def __init__(self, jellyfin_url, api_key, admin_user_key,discord_channel_id):

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix='/', intents=intents)

        self.server_url = jellyfin_url
        self.api_key = api_key
        self.admin_user_key = admin_user_key
        self.discord_channel_id = discord_channel_id

        self.last_items = set()

    async def on_ready(self):
        print(f'Bot connected as : {self.user}')

    # Vérifie le statut du serveur
    def check_server_status(self):
        try:
            response = requests.get(f"{self.server_url}/System/Ping", headers={'X-Emby-Token': self.api_key},timeout=5)
            return 'started' if response.status_code == 200 else 'stopped'
        except requests.exceptions.RequestException:
            return 'stopped'

    async def get_latest_items(self):

        headers = {'X-Emby-Token': self.api_key}
        response = requests.get(f"{self.server_url}/Users/{self.admin_user_key}/Items/Latest", headers=headers)
        resultat = response.json()

        if resultat is not None:

            new_items = [
                item for item in resultat
                if item['Name'] not in self.last_items
            ]

            self.last_items.update(item['Name'] for item in new_items)
            return new_items
        else:
            return False

    # /-/-/-/-/ GESTION DES COMMANDES /-/-/-/-/

    ## COMMANDE: STATUS
    async def state(self, ctx):

        server_status = self.check_server_status()
        server_status_color = "🟢" if server_status == 'started' else "🔴"

        await ctx.send(f"Server state : {server_status} ! {server_status_color}")

    ## COMMANDE: LATEST
    async def latest(self, ctx) :

        new_items = await self.get_latest_items()

        if not new_items:
            await ctx.send("No response from server.")

        else :
            msg = "# *New episodes !* \n/-------------------------/\n"
            for item in new_items :

                item_name = item["Name"]
                item_type = item["Type"]

                msg += (
                    f"## ***{item_name}***\n"
                    f"### - {item_type}\n"
                        )

                if item_type == "Series":
                    item_chil_cound = item["ChildCount"]
                    msg += f"### - {item_chil_cound} episodes\n"

                msg += "\n/-------------------------/\n"
            await ctx.send(msg)