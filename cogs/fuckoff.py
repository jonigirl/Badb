import discord
from discord.ext import commands, vbu
from random import randint
from random import choice as randchoice


class Fuckoff(vbu.Cog):
    """Fuck off."""

    def __init__(self, bot):
        self.bot = bot
        self.foffmsg = [
            "Locating a fuck to give",
            "Looking for a fuck to \
        give",
            "It is called KARMA and it is pronounced as haha fuck you",
            "\
        You cannot imagine the immensity of the fuck I do not give",
            "I dont \
        hate you but, lets put it this way. If I had a bucket of water and \
        you were on fire, I would drink the bucket of water",
            "I hope you \
        step on a lego",
            "Even with this wine you look ugly",
            "NO, FUCK \
        YOU",
            "Dear karma, I have a list of people you missed. \
        One of them is",
            "Attempting to give a fuck \n`PLEASE WAIT`",
        ]

    @vbu.command(pass_context=True, name="foff", aliases=["fuckoff"])
    async def _foff(self, ctx, user: discord.Member):
        """Displays a random fuck off message."""
        await ctx.send(
            "{} {}.\n\nBy yours truly {}.".format(
                randchoice(self.foffmsg), user.mention, ctx.message.author.mention
            )
        )

    @vbu.command(
        pass_context=True,
        name="afoff",
        aliases=["anonymousfoff", "afuckoff", "anonymousfuckoff"],
    )
    async def _afoff(self, ctx, user: discord.Member):
        """Displays an anonymous random fuck off message."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        await ctx.send("{} {}. ".format(randchoice(self.foffmsg), user.mention))

    @vbu.command(
        pass_context=True, name="ifoff", aliases=["itemfoff", "ifuckoff", "itemfuckoff"]
    )
    async def _ifoff(self, ctx, *, item):
        """Displays a random fuck off message for items."""
        await ctx.send(
            "{} {}.\n\nBy yours truly {}.".format(
                randchoice(self.foffmsg), item, ctx.message.author.mention
            )
        )

    @vbu.command(
        pass_context=True,
        name="iafoff",
        aliases=[
            "itemafoff",
            "iafuckoff",
            "ianonymousfuckoff",
            "itemanonymous\
        foff",
            "itemanonymousfuckoff",
        ],
    )
    async def _aifoff(self, ctx, *, item: str):
        """Displays an anonymous random fuck off message for items."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        await ctx.send("{} {}. ".format(randchoice(self.foffmsg), item))


def setup(bot: vbu.Bot):
    x = Fuckoff(bot)
    bot.add_cog(x)
