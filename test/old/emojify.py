## this is a script to take an image and covert it to emoji art.
import discord
from discord.ext import commands
import io

from bot.core.embed import KitsuneEmbed as Embed
from bot.core.core import KitsuneChan
from logic.compvis.emojify import masterEmojify


class Emojify(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    option = discord.option
    orientations = ["horizontal", "vertical", "auto"]

    @commands.slash_command(name="emojify", description="Convert image to emoji art.")  # Replace with your guild ID
    @option("image", discord.Attachment, description="Image to convert to emoji art.")
    @option("dimensions", int, description="Dimensions of the image in pixels (must be square).", default=14)
    @option("distance_algorithm", str, description="Algorithm to calculate distance between colors.", default="euclydian", choices=["euclydian", "manhattan"])
    @option("color_algorithm", str, description="Algorithm to detect color per region.", default="average", choices=["average", "kmeans"])
    async def emojify(
        self,
        ctx: discord.ApplicationContext,
        image: discord.Attachment,
        dimensions,
        distance_algorithm,
        color_algorithm,
    ):
        await ctx.defer()

        imageBytes = await image.read()

        emojiString = masterEmojify(imageBytes, dimensions, distance_algorithm, color_algorithm)

        if dimensions > 14:
            stringIo = io.BytesIO(emojiString.encode('utf-8'))
            await ctx.respond(file=discord.File(stringIo, filename="output.txt"))
            return

        embed = Embed(title="Emooji Art", description=emojiString, color=0xBEBEFE)

        await ctx.respond(embed=embed)




def setup(bot:commands.Bot):
    bot.add_cog(Emojify(bot))
