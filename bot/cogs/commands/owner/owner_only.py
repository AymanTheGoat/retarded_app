from discord.ext import commands
from discord import ApplicationContext as Context
from bot.core.core import KitsuneChan
from bot.core.embed import KitsuneEmbed as Embed 
from ... import guild_ids
from discord import SlashCommandGroup

def setup(bot):
     bot.add_cog(Owner(bot))


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    owner = SlashCommandGroup("owner", "Owner only commands")

    slash = owner.command

    ## SYNC
    @commands.is_owner()
    @slash(name="sync", description="Sync slash commands", guild_ids=guild_ids)
    async def sync(self, ctx: Context, scope: str):
        if scope == "global":
            await self.bot.sync_commands()
            embed = Embed(
                description="Slash commands have been globally synchronized.",
                color=0xBEBEFE,
            )
            await ctx.respond(embed=embed)
        elif scope == "local" or scope == "guild":
            guild = ctx.guild
            if guild:
                await self.bot.sync_commands(guild_ids=[guild])
                embed = Embed(
                    description=f"Slash commands have been synchronized in the guild: {guild.name}.",
                    color=0xBEBEFE,
                )
                await ctx.respond(embed=embed)
            else:
                embed = Embed(
                    description="This command must be used within a guild.",
                    color=0xE02B2B,
                )
                await ctx.respond(embed=embed)
        else:
            embed = Embed(
                description="The scope must be `global` or `guild`.",
                color=0xE02B2B,
            )
            await ctx.respond(embed=embed)


    ## LOAD
    @slash(name="load", description="Load a cog", guild_ids=guild_ids)
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        try:
            self.bot.load_extension(f"bot.cogs.{cog}")
        except Exception:
            embed = Embed(
                description=f"Could not load the `{cog}` cog.", color=0xE02B2B
            )
            await context.respond(embed=embed)
            return
        embed = Embed(
            description=f"Successfully loaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.respond(embed=embed)


    ## UNLOAD
    @slash(name="unload", description="Unloads a cog.", guild_ids=guild_ids)
    @commands.is_owner()
    async def unload(self, context: Context, cog: str):
        try:
            self.bot.unload_extension(f"bot.cogs.{cog}")
        except Exception:
            embed = Embed(
                description=f"Failed unloading the `{cog}` cog.", color=0xE02B2B
            )
            await context.respond(embed=embed)
            return
        embed = Embed(
            description=f"Successfully unloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.respond(embed=embed)


    ## RELOAD
    @slash(name="reload", description="Reloads a cog.", guild_ids=guild_ids)
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        try:
            self.bot.reload_extension(f"bot.cogs.{cog}")
        except Exception:
            embed = Embed(
                description=f"Failed reloading the `{cog}` cog.", color=0xE02B2B
            )
            await context.respond(embed=embed)
            return
        embed = Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.respond(embed=embed)


    ## SHUTDOWN
    @slash(name="kys", description="Turn off the bot :sleepy:", guild_ids=guild_ids)
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        embed = Embed(description="Goodbye! :sleepy:", color=0xBEBEFE)
        await context.respond(embed=embed)
        await self.bot.close()


    ## PARROT
    @slash(name="echo", description="Repeats after me", guild_ids=guild_ids)
    @commands.is_owner()
    async def echo(self, context: Context, *, message: str) -> None:
        await context.respond(message)


    ## SAY
    @slash(name="say", description="Repeats after me", guild_ids=guild_ids)
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        await context.respond("done", delete_after=2, ephemeral=True)
        await context.send(message)


