import asyncio
import functools
import io
import typing

from datetime import datetime as dt

import discord

from discord.ext import commands
from discord.ext import vbu


class UserInfo(vbu.Cog):
    @vbu.command(
        aliases=["avatar", "av"],
        application_command_meta=commands.ApplicationCommandMeta(
            options=[
                discord.ApplicationCommandOption(
                    name="target",
                    description="The item that you want to enlarge.",
                    type=discord.ApplicationCommandOptionType.string,
                ),
            ],
        ),
    )
    async def enlarge(
        self,
        ctx: vbu.Context,
        target: typing.Union[
            discord.Member, discord.User, discord.Emoji, discord.PartialEmoji
        ] = None,
    ):
        """
        Enlarges the avatar or given emoji.
        """

        target = target or ctx.author
        if isinstance(target, (discord.User, discord.Member, discord.ClientUser)):
            url = target.display_avatar.url
        elif isinstance(target, (discord.Emoji, discord.PartialEmoji)):
            url = target.url
        with vbu.Embed(color=0x1) as embed:
            embed.set_image(url=str(url))
        await ctx.send(embed=embed)

    @commands.context_command(name="Get user info")
    async def _get_user_info(self, ctx: commands.SlashContext, user: discord.Member):
        command = self.whois
        await command.can_run(ctx)
        await ctx.invoke(command, user)

    @vbu.command(
        aliases=["whoami"],
        application_command_meta=commands.ApplicationCommandMeta(
            options=[
                discord.ApplicationCommandOption(
                    name="user",
                    description="The user you want to get the information of.",
                    type=discord.ApplicationCommandOptionType.user,
                    required=False,
                ),
            ],
        ),
    )
    async def whois(self, ctx: vbu.Context, user: discord.Member = None):
        """
        Give you some information about a user.
        """

        # Set up our intial vars
        user = user or ctx.author
        embed = vbu.Embed(use_random_colour=True)
        embed.set_author_to_user(user)

        # Get the user account creation time
        create_value = f"{discord.utils.format_dt(user.created_at)}\n{discord.utils.format_dt(user.created_at, 'R')}"
        embed.add_field("Account Creation Time", create_value, inline=False)

        # Get the user guild join time
        if ctx.guild:
            join_value = f"{discord.utils.format_dt(user.joined_at)}\n{discord.utils.format_dt(user.joined_at, 'R')}"
            embed.add_field("Guild Join Time", join_value, inline=False)

        # Set the embed thumbnail
        embed.set_thumbnail(user.display_avatar.with_size(1024).url)

        # Sick
        if isinstance(ctx, commands.SlashContext):
            return await ctx.interaction.response.send_message(embed=embed)
        else:
            return await ctx.send(embed=embed)


def setup(bot: vbu.Bot):
    x = UserInfo(bot)
    bot.add_cog(x)
