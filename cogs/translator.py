import discord
from discord.ext import commands, vbu
from subprocess import check_output

import goslate


class Translator(vbu.Cog):
    """Translate text using google translate."""

    def __init__(self, bot):
        self.bot = bot
        self.gs = goslate.Goslate()

    @vbu.group(pass_context=True, invoke_without_command=True, aliases=["tr"])
    async def translate(self, ctx, to_lang, *, text):
        """Translate text using google translate."""
        if to_lang in self.gs.get_languages():
            try:
                lang_id = self.gs.detect(text)
                lang = self.gs.get_languages()[lang_id]
                await ctx.send("{} (detected as {} ({}))".format(self.gs.translate(text, to_lang), lang, lang_id))
            except Exception as e:
                await ctx.send("An error occured while translating. ({})".format(e))
        else:
            await ctx.send("That language could not be found in the list, for a list of supported languages do {}translate langlist".format(ctx.prefix))

    @translate.command()
    async def langlist(self, ctx):
        """Shows you a list of supported languages."""
        msg = "```fix\nCurrent available languages are:\n"
        for lang in self.gs.get_languages():
            msg += "\t{}: {}\n".format(self.gs.get_languages()[lang], lang)
            if len(msg) > 1750:
                await ctx.send(msg + "```")
                msg = "```fix\n"
        await ctx.send(msg + "```")


def setup(bot: vbu.Bot):
    x = Translator(bot)
    bot.add_cog(x)
