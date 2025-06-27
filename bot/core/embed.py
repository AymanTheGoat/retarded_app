from discord import Embed, Color
from datetime import datetime



url = "https://cdn.discordapp.com/avatars/1353375373722910904/5fa746a1fadea11b305269451ec4e751.webp" 



class KitsuneEmbed(Embed):
    def __init__(self, description: str, color: Color|int, title: str|None = None):
        super().__init__(title=title, description=description, color=color, timestamp=datetime.now())
        self.set_footer(text="Kitsune-Chan • Made by Ayman", icon_url=url)
