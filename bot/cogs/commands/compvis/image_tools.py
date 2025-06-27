
from io import BytesIO
from discord import Attachment, File, ApplicationContext
from discord.ext.commands import Cog
from ... import guild_ids
from bot.core.core import KitsuneChan
from bot.core.embed import KitsuneEmbed as Embed
from logic.compvis.emojify import masterEmojify
from logic.compvis.dominant_color import extractDominantColors
from discord import option
from discord import SlashCommandGroup



class ImageToolsCog(Cog):
    def __init__(self, bot: KitsuneChan):
        self.bot = bot

    image = SlashCommandGroup("image", "Image processing commands")
    slash = image.command
    
    orientations = ["horizontal", "vertical", "auto"]

    # === Emojify Command ===
    @slash(name="emojify", description="Convert image to emoji art.", guild_ids=guild_ids)
    @option("image", Attachment, description="Image to convert to emoji art.")
    @option("dimensions", int, description="Dimensions of the image in pixels (must be square).", default=14)
    @option("distance_algorithm", str, description="Algorithm to calculate distance between colors.", default="euclydian", choices=["euclydian", "manhattan"])
    @option("color_algorithm", str, description="Algorithm to detect color per region.", default="average", choices=["average", "kmeans"])
    async def emojify(
        self,
        ctx: ApplicationContext,
        image: Attachment,
        dimensions: int,
        distance_algorithm: str,
        color_algorithm: str,
    ):
        await ctx.defer()

        imageBytes = await image.read()
        emojiString = masterEmojify(imageBytes, dimensions, distance_algorithm, color_algorithm)

        if dimensions > 14:
            stringIo = BytesIO(emojiString.encode('utf-8'))
            await ctx.respond(file=File(stringIo, filename="output.txt"))
            return

        embed = Embed(title="Emooji Art", description=emojiString, color=0xBEBEFE)
        await ctx.respond(embed=embed)

    # === Dominant Color Command ===
    @slash(name="dominant_color", description="Extract dominant colors from an image", guild_ids=guild_ids)
    @option("image", Attachment, description="Image to extract colors from")
    @option("n", int, description="Number of colors to extract", default=5)
    @option("q", int, description="Quantization factor", default=20)
    @option("orientation", str, description="Orientation of the color bar", default="auto", choices=orientations)
    async def dominant_color(
        self,
        ctx: ApplicationContext,
        image: Attachment,
        n: int,
        q: int,
        orientation: str,
    ):
        await ctx.defer()
        imageBytes = await image.read()

        if n < 1 or n > 10:
            await ctx.respond("Please choose a value for `n` between 1 and 10.")
            return
        if q < 1 or q > 255:
            await ctx.respond("Please choose a value for `q` between 1 and 255.")
            return

        jpg = extractDominantColors(imageBytes, n=n, q=q, orientation=orientation)
        await ctx.respond(file=File(BytesIO(jpg.tobytes()), filename="output.jpg"))


def setup(bot: KitsuneChan):
    bot.add_cog(ImageToolsCog(bot))
