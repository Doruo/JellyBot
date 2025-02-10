import discord
import requests
from discord.ext import commands, tasks
from pathlib import Path

class JellyfinBot(commands.Bot):

    def __init__(
            self, 
            server_protocol,server_host,server_port, 
            api_key, admin_user_key, 
            discord_channel_id, 
            application_id
        ):

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix='/', intents=intents)

        self.server_protocol = server_protocol
        self.server_host = server_host
        self.server_port = server_port
        self.api_key = api_key
        self.admin_user_key = admin_user_key
        self.discord_channel_id = discord_channel_id
        self.discord_application_id = application_id

        self.type_emoji = {
            # Video
            "Series": "📺", "Season": "📺", "Episode": "📺", "Movie": "🎬","MusicVideo": "🎥","Video": "📹","Trailer": "🎦",
            # Audio
            "Music": "🎵","Audio": "🔊","AudioBook": "🎧","Podcast": "🎙️","Album": "💿","Song": "🎼",
            # Reading
            "Book": "📚","Comic": "📖","Magazine": "📰","Manga": "📓",
            # Collections
            "Collection": "📁","BoxSet": "📦","Playlist": "📑",
            # Others
            "PhotoAlbum": "📸","Photo": "🖼️","Game": "🎮","TvChannel": "📡","Program": "🖥️","Recording": "⏺️"
        }

        self.last_items = set()

    # Called on bot starting
    async def on_ready(self):
        
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.update_presence()

    @tasks.loop(minutes=1)  # Update status every n parameters
    async def update_presence(self):
        
        # Possible values: watching, playing, listening, streaming
        activity_type = discord.ActivityType.watching  
        name = 'Jellyfin'
        state = self.check_server_status()
        status = 'dnd'
        
        # Rich Presence Creation
        activity = discord.Activity(
            application_id=self.discord_application_id,
            type=activity_type,
            name=name,
            state=state,
        )
        
        await self.change_presence(status=status, activity=activity)

    @update_presence.before_loop
    async def before_update_presence(self):
        await self.wait_until_ready()

    # Ping server to check if  it's running
    def check_server_status(self):

        server_url = f'{self.server_protocol}://{self.server_host}:{self.server_port}'
        try:
            response = requests.get(f"{server_url}/System/Ping", headers={'X-Emby-Token': self.api_key},timeout=4)

            if response.status_code == 200: 
                server_status = "Online"
                server_status_color = "🟢"
            else :
                server_status = "Offline"
                server_status_color = "🔴"
        
            return f"Server state: {server_status} {server_status_color}"
        except requests.exceptions.Timeout or requests.exceptions.RequestException:
            return f"Server state: Offline 🔴"

    async def get_latest_items(self):

        server_url = f'{self.server_protocol}://{self.server_host}:{self.server_port}'

        headers = {'X-Emby-Token': self.api_key}
        response = requests.get(f"{server_url}//Users/{self.admin_user_key}/Items/Latest", headers=headers)
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

    # /-/-/-/-/ COMMANDS /-/-/-/-/

    ## COMMAND: STATUS
    async def state(self, ctx):
        await ctx.send(self.check_server_status())

    ## COMMAND: LATEST
    async def latest(self, ctx):

        new_items = await self.get_latest_items()

        if new_items == False:
            await ctx.send("❌ Aucune réponse du serveur.")
            return
        
        self.last_items.update(item['Name'] for item in new_items)
        
      
        message = "🆕 **New Content !**\n\n"
        
        for item in new_items:
            item_name = item["Name"]
            item_type = item["Type"]

            # Emoji type choice
            type_emoji = self.type_emoji.get(item_type, "📎")
            
            message += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Main title
            message += f"{type_emoji} **{item_name}**\n"
            # Type
            message += f"*Type: {item_type}*\n"
            
            # episodes information for series
            if item_type == "Series":
                episode_count = item["ChildCount"]
                episode_emoji = "✨" if episode_count > 1 else "⭐"
                message += f"{episode_emoji} {episode_count} new episode{'s' if episode_count > 1 else ''}\n"
    
            message += "\n"
        
        message += "━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Send msg to discord with 2k caracter limit
        if len(message) > 2000:
            messages = [message[i:i+1900] for i in range(0, len(message), 1900)]
            for message in messages:
                await ctx.send(message)
        else:
            await ctx.send(message)

    ## COMMAND: SUGGEST
    async def suggest(self, ctx, *args: tuple):
        try:
        
            # At least one suggestion given
            if (args is not None) :

                if len(args) == 0 :
                    suggestions=""
                else :
                    # Parses given suggestions
                    suggestions = '\n'+'\n'.join(args)+'\n'

                # Number of suggestions
                sugg_len = len(suggestions)

                # Get the current directory path 
                current_script_path = Path(__file__).resolve()
                # Get the project root path
                project_root = current_script_path.parent.parent.parent
                    
                # Create config directory if it doesn't exist
                config_dir = project_root / "ressources/suggestions" 
                config_dir.mkdir(exist_ok=True)

                # Create suggestions file
                env_path = config_dir / "suggestions.txt"

                # Try to add suggestions in a suggestion.txt file
                # Create file if it doesn't exist 
                with open(env_path, "a") as file:
                    file.write(suggestions)
 
                await ctx.send(f"Numbers of suggestions sent: {sugg_len} \n Your suggestions: {suggestions}")

            # No suggestions given
            else :
                await ctx.send(f"You just sent no suggestions, try adding arguments to command")
        except Exception as e:
            print(f"Error when trying to send suggestions to server : {e}")
