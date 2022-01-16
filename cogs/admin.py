"""This cog provides administrative commands to Discord users with elevated privileges."""
import discord
from discord.ext import commands, vbu


class Admin(vbu.Cog):
    """The Admin cog class."""

    def __init__(self, bot):
        self.bot = bot

    @vbu.command(name='clear', hidden=True)
    @vbu.has_permissions(administrator=True)
    async def delete_messages(self, ctx, limit: int = 1):
        """Deletes the latest messages in the channel. The invoking message is deleted.

        .. Note::
            Requires `administrator` privilege.

        :param ctx: The invocation context.
        :param limit: The number of messages to delete. Default is 1.
        """
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)

    @vbu.command(name='say', hidden=True)
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

    @vbu.command(name='spam', hidden=True)
    @vbu.has_permissions(manage_messages=True)
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
                '```Deleted {} spam messages```'.format(len(spam)),
                DiscordUser(ctx.author),
            )
            self.bot.log(embed=embed)


    @vbu.command(name='add-command', hidden=True)
    @commands.is_owner()
    async def add_discord_command(self, ctx, command, *, response):
        """Inserts a quick chatroom command.

        :param ctx: The invocation context.
        :param command: The command name to add.
        :param response: The response for the command.
        """
        user = DiscordUser(ctx.author)
        command = '!{}'.format(command.strip('!'))
        res = user.add_chatroom_command(command, response)
        if res['success']:
            embed = quickembed.success(
                desc='Command `{}` updated'.format(command), user=user
            )
        else:
            embed = quickembed.error(desc='Failed', user=user)
        await ctx.send(embed=embed)

    @vbu.command(name='update-command', hidden=True)
    @commands.is_owner()
    async def update_discord_command(self, ctx, command, *, response):
        """Updates a quick chatroom command.

        .. Note::
            Only the bot owner can use this.

        :param ctx: The invocation context.
        :param command: The command name to update.
        :param response: The updated response for the command.
        """
        user = DiscordUser(ctx.author)
        command = '!{}'.format(command.strip('!'))
        res = user.update_chatroom_command(command, response)
        if res['success']:
            embed = quickembed.success(
                desc='Command `{}` updated'.format(command), user=user
            )
        else:
            embed = quickembed.error(desc='Failed', user=user)
        await ctx.send(embed=embed)

    @vbu.command(name='mute', hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def mute_member(self, ctx, member: discord.Member):
        """Mutes a member by assigning them the `Muted` role.

        .. Note::
            Requires `Manage Roles` privilege.

        .. Note::
            A `Muted` role must exist with the proper permissions.
            It's a simple role that can only read the channels and not send messages.

        :param ctx: The invocation context.
        :param member:
        """
        user = DiscordUser(ctx.author)
        role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        if not role:
            embed = quickembed.error(desc='`Muted` role does not exist', user=user)
        elif role not in member.roles:
            await member.add_roles(role)
            embed = quickembed.success(desc='Muted {}'.format(member), user=user)
        else:
            embed = quickembed.error(
                desc='{} is already muted'.format(member), user=user
            )
        await ctx.send(embed=embed)

    @vbu.command(name='unmute', hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute_member(self, ctx, member: discord.Member):
        """Unmutes a member by removing their `Muted` role.

        .. Note::
            Requires `Manage Roles` privilege.

        .. Note::
            A `Muted` role must exist with the proper permissions.
            It's a simple role that can only read the channels and not send messages.

        :param ctx: The invocation context.
        :param member:
        """
        user = DiscordUser(ctx.author)
        role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        if not role:
            embed = quickembed.error(desc='`Muted` role does not exist', user=user)
        elif role in member.roles:
            await member.remove_roles(role)
            embed = quickembed.success(desc='Unmuted {}'.format(member), user=user)
        else:
            embed = quickembed.error(
                desc='{} is already unmuted'.format(member), user=user
            )
        await ctx.send(embed=embed)



def setup(bot: vbu.bot):
    """Required for cogs.

    :param bot: The Discord bot.
    """
    bot.add_cog(Admin(bot))
    x = Admin(bot)
    bot.add_cog(x)
