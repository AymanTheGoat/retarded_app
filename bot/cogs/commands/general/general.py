import discord
from ... import guild_ids
from discord.ext import commands
from discord import ApplicationContext as Context, SlashCommandGroup
import re
from bot.core.core import KitsuneChan
from discord import SlashCommandGroup

def setup(bot):
    bot.add_cog(General(bot))


class General(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    general = SlashCommandGroup("general", "General commands")

    slash = general.command

    ## PING
    @slash(name="ping", description="Ping the bot", guild_ids=guild_ids)
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")
    

    ## FAKE NITRO
    @slash(name="nitro", description="Send emoji without nitro", guild_ids=guild_ids)
    @discord.option("message", description="Message with emoji ids or full emojis", required=True)
    async def fitro(self, context: Context, message: str):
        await context.respond("Okay!", ephemeral=True, delete_after=0)

        webhook: discord.Webhook = await context.channel.create_webhook(name="Kitsune-Emocheese!")
        new_content = message

        emoji_matches = re.findall(r'<a?:\w+:(\d+)>', message)

        for match in emoji_matches:
            for guild_emoji in context.guild.emojis:
                if str(guild_emoji.id) == match:
                    emoji_str = f"<a:{guild_emoji.name}:{guild_emoji.id}>" if guild_emoji.animated else f"<:{guild_emoji.name}:{guild_emoji.id}>"
                    new_content = new_content.replace(f"<a:{guild_emoji.name}:{guild_emoji.id}>", emoji_str)
                    new_content = new_content.replace(f"<:{guild_emoji.name}:{guild_emoji.id}>", emoji_str)

        emoji_matches = re.findall(r'\b(?:0|[1-9]\d{0,19})\b', message)

        for match in emoji_matches:
            for guild_emoji in context.guild.emojis:
                if str(guild_emoji.id) == match:
                    if guild_emoji.animated:
                        emoji_str = f"<a:{guild_emoji.name}:{guild_emoji.id}>"
                    else:
                        emoji_str = f"<:{guild_emoji.name}:{guild_emoji.id}>"
                    new_content = new_content.replace(match, emoji_str)

        await webhook.send(
            content=new_content,
            username=context.author.display_name,
            avatar_url=context.author.avatar.url if context.author.avatar else None
        )

        webhooks = await context.channel.webhooks()
        for webhook in webhooks:
            if webhook.name == "Kitsune-Emocheese!":
                await webhook.delete()

