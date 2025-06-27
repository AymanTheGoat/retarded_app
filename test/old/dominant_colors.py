import discord
from discord.ext import commands
from io import BytesIO
from bot.core.core import KitsuneChan 
from logic.compvis.dominant_color import extractDominantColors



class DominantColor(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    option = discord.option
    orientations = ["horizontal", "vertical", "auto"]

    @commands.slash_command(name="dominant_color", description="Extract dominant colors from an image")
    @option("image", discord.Attachment, description="Image to extract colors from")
    @option("n", int, description="Number of colors to extract", default=5)
    @option("q", int, description="Quantization factor", default=20)
    @option("orientation", str, description="Orientation of the color bar", default="auto", choices=orientations)
    async def dominant_color(
        self,
        ctx: discord.ApplicationContext,
        image: discord.Attachment,
        n: int = 5,
        q: int = 20,
        orientation: str = "auto",
    ):
        await ctx.defer()
        imageBytes = await image.read()

        if  n < 1 or n > 10:
            await ctx.respond("Please choose a value for `n` between 1 and 10.")
            return
        if q < 1 or q > 255:
            await ctx.respond("Please choose a value for `q` between 1 and 255.")
            return
        jpg = extractDominantColors(imageBytes, n=n, q=q, orientation=orientation)
        await ctx.respond(file=discord.File(BytesIO(jpg.tobytes()), filename="output.jpg"))


def setup(bot:commands.Bot):
    bot.add_cog(DominantColor(bot))