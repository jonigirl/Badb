import discord
from discord.ext import vbu utils
from discord.ext import utils
import os
import asyncio
import typing
import collections


class Warner(vbu.Cog):
    """Warn people."""

    def __init__(self, bot: utils.Bot):
        super().__init__(bot)
        self.set_profile_locks: typing.Dict[int, asyncio.Lock] = collections.defaultdict(asyncio.Lock)
        # self.settings = dataIO.load_json("warner/warnings.json")  # point this to sql

    def member_is_moderator(bot, member) -> bool:
        """
        Returns whether or not a given discord.Member object is a moderator
        """

        # Make sure they're an actual member
        if member.guild is None:
            return False

        # And return checks
        return any([
            member.guild_permissions.manage_roles,
            member.id in bot.config['owners'],
            member.guild.owner == member,
        ])

    @vbu.command(pass_context=True, no_pm=True, member_is_moderator=True)
    async def warn(self, ctx, user: discord.Member, times: int = 1):
        """Warn people for their actions."""
        serverid = ctx.message.server.id
        userid = user.id
        if serverid not in self.settings:
            self.settings[serverid] = {}
            self.save_settings()
        if userid not in self.settings[serverid]:
            self.settings[serverid][userid] = 1
            self.save_settings()
            await ctx.send("The user has 1 warnings but nothing happens yet, next up: 5 minute mute.")
            return
        else:
            self.settings[serverid][userid] += times
            self.save_settings()
            if self.settings[serverid][userid] == 1:
                await ctx.send("The user has 1 warnings but nothing happens yet, next up: 5 minute mute.")
            if self.settings[serverid][userid] == 2:
                await ctx.send("The user has 2 warnings and has been muted for 5 minutes, next up: 30 minute mute.")
                await self.mute(user, 5)
            elif self.settings[serverid][userid] == 3:
                await ctx.send("The user has 3 warnings and has been muted for 30 minutes, next up: kick.")
                await self.mute(user, 30)
            elif self.settings[serverid][userid] == 4:
                try:
                    await self.bot.kick(user)
                    await ctx.send("The user has 4 warnings and has been kicked, next up: ban.")
                except discord.Forbidden:
                    await ctx.send("The user has 4 warnings but could not be kicked because I do not have the right perms for that.")
                except commands.CommandError:
                    await ctx.send("The user has 4 warnings but an unknown error occured while trying to kick the user.")
            elif self.settings[serverid][userid] >= 5:
                try:
                    await self.bot.ban(user, delete_message_days=3)
                    del self.settings[serverid][userid]
                    self.save_settings()
                    await ctx.send("The user has 5 warnings and has been banned.")
                except discord.Forbidden:
                    await ctx.send("The user has 5 warnings but could not be banned because I do not have the right perms for that.")
                except commands.CommandError:
                    await ctx.send("The user has 5 warnings but an unknown error occured while trying to ban the user.")

    @vbu.command(pass_context=True, no_pm=True, member_is_moderator=True)
    async def resetwarns(self, ctx, user: discord.Member):
        """Reset the warnings you gave to someone"""
        serverid = ctx.message.server.id
        userid = user.id
        if serverid not in self.settings:
            await ctx.send("No one in this server has got a warning yet.")
            return
        elif userid not in self.settings[serverid]:
            await ctx.send("This user doesn't have a warning yet.")
            return
        else:
            del self.settings[serverid][userid]
            self.save_settings()
            await ctx.send("Users warnings succesfully reset!")
            return

    @vbu.command(pass_context=True, no_pm=True, member_is_moderator=True)
    async def warns(self, ctx, user: discord.Member):
        """See how much warnings someone has."""
        if ctx.message.server.id not in self.settings:
            await ctx.send("No one in this server has got a warning yet.")
            return
        elif user.id not in self.settings[ctx.message.server.id]:
            await ctx.send("This user doesn't have a warning yet.")
            return
        elif self.settings[ctx.message.server.id][user.id] == 1:
            await ctx.send("This user has {} warning.".format(self.settings[ctx.message.server.id][user.id]))
            return
        else:
            await ctx.send("This user has {} warnings.".format(self.settings[ctx.message.server.id][user.id]))

    def save_settings(self):
        dataIO.save_json("data/badb.json", self.settings)

    async def mute(self, member, minutes: int):
        for channel in member.server.channels:
            perms = discord.PermissionOverwrite()
            perms.send_messages = False
            await self.bot.edit_channel_permissions(channel, member, perms)
        await asyncio.sleep(minutes * 60)
        for channel in member.server.channels:
            perms = discord.PermissionOverwrite()
            perms.send_messages = None
            await self.bot.edit_channel_permissions(channel, member, perms)


def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")


def check_files():
    if not os.path.exists("data/badb.db"):
        try:
            with open('badb.db', 'x') as f:
                f.write('Creating /badb.db file... a new text file!')
                f = open("data/badb.db")
        except FileNotFoundError:
            print("The Directory of Database does not exist")


def setup(bot: vbu.Bot):
    check_folders()
    check_files()
    x = Warner(bot)
    bot.add_cog(x)
