import asyncio
import discord
import json
import time

from discord.ext import commands
from discord.ext import vbu


class Moderation(vbu.Cog):
    def __init__(self, bot):
        self.bot = bot

    @vbu.command(usage="[#channel/id]", name="lock", description="Locks a channel")
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Locks a text channel.

        .. Note::
            Must have manage messages permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"{channel.mention} locked!")

    @vbu.command(usage="[#channel/id]", name="unlock", description="Unlocks a channel")
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlocks a text channel.

        .. Note::
            Must have manage messages permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"{channel.mention} unlocked!")

    @vbu.command(
        name="kick",
        usage="<member> [reason]",
        description="Kicks a user from the server",
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kicks a user from the server.
        .. Note::
            Must have kick members permission
        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        if member.id == ctx.author.id:
            await ctx.send("You cannot kick yourself!")
            return

        await member.kick(reason=reason)

        await ctx.message.delete()
        kick = discord.Embed(
            description=f"**A member has been kicked.**\n\n"
            f"Moderator: {ctx.author.mention}\n"
            f"Member: {member.mention}",
            colour=discord.Colour.blue(),
        )
        kick.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=kick)

    @vbu.command(
        usage="<member> [reason]", name="ban", description="Bans a user from the server"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Bans a member from the server.

        .. Note::
            Must have ban members permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        if member.id == ctx.author.id:
            await ctx.send("You cannot ban yourself!")
            return

        await member.ban(reason=reason, delete_message_days=0)
        ban = discord.Embed(
            description=f"**A member has been banned.**\n\n"
            f"Moderator: {ctx.author.mention}\n"
            f"Member: {member.mention}",
            colour=discord.Colour.blue(),
        )
        ban.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=ban)

    @vbu.command(
        usage="<member> [reason]",
        name="softban",
        description="Bans a user from the server and deletes all of his messages of the last 7 days",
    )
    @commands.has_permissions(ban_members=True)
    async def softban(
        self, ctx, member: discord.Member, *, reason="No reason provided"
    ):
        """Bans a member from the server and deletes
        all of his messages of the last 7 days.

        .. Note::
            Must have ban members permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        if member.id == ctx.author.id:
            await ctx.send("You cannot ban yourself!")
            return

        await member.ban(reason=reason, delete_message_days=7)
        softban = discord.Embed(
            description=f"**A member has been banned.**\n\n"
            f"Moderator: {ctx.author.mention}\n"
            f"Member: {member.mention}",
            colour=discord.Colour.blue(),
        )
        softban.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=softban)

    @vbu.command(
        usage="<id>", name="unban", description="Unbans a user from the server"
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user_id: int):
        """Unbans a member from the server.

        .. Note::
            Must have ban members permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        user = await self.client.fetch_user(user_id)
        await ctx.guild.unban(user)
        unban = discord.Embed(
            description=f"**A user has been unbanned.**\n\n"
            f"Moderator: {ctx.author.mention}\n"
            f"Member: {user.mention}",
            colour=discord.Colour.blue(),
        )
        await ctx.send(embed=unban)

    @vbu.command(
        usage="amount", name="clear", description="Deletes a certain number of messages"
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        """Clears channel history of x messages.

        .. Note::
            Must have manage messages permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"I have cleared **{amount}** messages.", delete_after=3)

    @vbu.command(
        usage="<member> [reason]", name="mute", description="Mutes a user on the server"
    )
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Mutes a member and gived the the Muted role.

        .. Note::
            Must have manage messages permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=False,
                )
        mute = discord.Embed(
            description=f"**A member has been muted.**\n\n"
            f"Moderator: {ctx.author.mention}\n"
            f"Member: {member.mention}",
            colour=discord.Colour.blue(),
        )
        mute.add_field(name="Reason", value=reason)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(embed=mute)

    @vbu.command(usage="<member>", name="Unmutes a user on the server")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes a member that has been prevously muted.

        .. Note::
            Must have manage messages permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        unmute = discord.Embed(
            description=f"**A member has been unmuted.**\n\n"
            f"Moderator: {ctx.author.mention}\n"
            f"Member: {member.mention}",
            colour=discord.Colour.blue(),
        )
        await ctx.send(embed=unmute)

    @vbu.command(
        name="nuke", description="Clones a text channel and then deletes the old one"
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def nuke(self, ctx):
        """Clones a test channel the nukes the old one.

        .. Note::
            Must be administrator

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        channelthings = [ctx.channel.category, ctx.channel.position]
        await ctx.channel.clone()
        await ctx.channel.delete()
        nukedchannel = channelthings[0].text_channels[-1]
        await nukedchannel.edit(position=channelthings[1])
        await nukedchannel.send(f"Channel was nuked by {ctx.author.mention}")

    @vbu.command(
        usage="<add/remove> <member> <role>",
        name="role",
        description="Adds or removes a role from a user",
    )
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, addORremove, member: discord.Member, role: discord.Role):
        """Adds or Removes roles to members.

        .. Note::
            Must have manage roles permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        addORremove = addORremove.lower()

        if addORremove == "add":

            if role == ctx.author.top_role:
                return await ctx.send(
                    "That role has the same position as your top role!"
                )

            if role in member.roles:
                return await ctx.send("The member already has this role assigned!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(
                    "This role is higher than my role, move it to the top!"
                )

            await member.add_roles(role)
            await ctx.send(f"I have added {member.mention} the role {role.mention}")

        if addORremove == "remove":

            if role == ctx.author.top_role:
                return await ctx.send(
                    "That role has the same position as your top role!"
                )

            if role not in member.roles:
                return await ctx.send("The member does not have this role!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(
                    "This role is higher than my role, move it to the top!"
                )

            await member.remove_roles(role)
            await ctx.send(f"I have removed {member.mention} the role {role.mention}")

    @vbu.command(usage="<seconds>")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int):
        """Invokes slowmode for the channel for the stated seconds.

        .. Note::
            Must have manage messages permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(
            f"Slowmode is now enabled in this channel with a chat delay of {seconds} seconds."
        )

    @vbu.command(name="say", hidden=True)
    @commands.is_owner()
    async def repeat_message(self, ctx, *, msg: str):
        """Repeats the message as the bot. The invoking message is deleted.

        .. Note::
            Only the bot owner can use this.

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        await ctx.message.delete()
        await ctx.send(msg)

    @vbu.command(name="spam", hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def delete_spam_messages(self, ctx):
        """Deletes duplicate messages in the channel.

        .. Note::
            Messages are checked per author.
            The original message will remain.

        :param ctx: The invocation context.
        """
        msgs = []
        spam = []
        async for msg in ctx.channel.history(limit=50):
            c = str(msg.author) + msg.content
            if c in msgs:
                spam.append(msg)
            else:
                msgs.append(c)

        spam.append(ctx.message)
        await ctx.channel.delete_messages(spam)
        if len(spam) > 1:
            embed = quickembed.info(
                "```Deleted {} spam messages```".format(len(spam)),
                DiscordUser(ctx.author),
            )
            self.bot.log(embed=embed)


def setup(bot: vbu.Bot):
    x = Moderation(bot)
    bot.add_cog(x)
