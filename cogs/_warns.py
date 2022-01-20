import discord
import json
import logging
import random
import string

from discord.ext import commands
from discord.ext import vbu


class Warns(vbu.Cog):
    def __init__(self, bot):
        self.bot = bot


def check_if_guild_exists(guild_id: int):
    with open("data/warns.json", "r") as f:
        load = json.load(f)

    try:
        load[str(guild_id)]
    except KeyError:
        load[str(guild_id)] = {}


def check_if_user_exists(guild_id: int, user_id: int):
    with open("data/warns.json", "r") as f:
        load = json.load(f)

        try:
            load[str(guild_id)][str(user_id)]
        except KeyError:
            load[str(guild_id)][str(user_id)] = []

    # this function will return with all the user's warns

    def get_user_warns(guild_id: int, user_id: int):
        with open("data/warns.json", "r") as f:
            load = json.load(f)

        warnings = load[str(guild_id)][str(user_id)]

        return warnings

        # this functions removes a warning from the user's warns
        @vbu.command()
        # this will make it required to have the "kick members" permissions to use the command
        @commands.has_permissions(kick_members=True)
        async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
            """Warns a member.

            .. Note::
                Must have kick members permission

            :param ctx: The invocation context.
            :param msg: The message the bot will repeat.
            """
            check_if_guild_exists(ctx.guild.id)
            check_if_user_exists(ctx.guild.id, member.id)
            code = add_warn(ctx.guild.id, member.id, ctx.author.id, reason)

            embed = discord.Embed(
                color=ctx.author.color,
                title=f"Warning ID: {code}",
                description=f"✅ Warned **{member}** for : {reason}",
            )
            await ctx.send(embed=embed)
            embed2 = discord.Embed(
                color=ctx.author.color,
                title=f"You have been warned in {ctx.guild.name}!",
                description=f"**Warning ID:** `{code}`\n**Reason:** {reason}",
            )
            try:
                await member.send(embed=embed2)
            except Exception as e:
                logging.exception(e)
                pass

    def remove_warn(guild_id: int, user_id: int, warn_id: int):
        with open("data/warns.json", "r") as f:
            load = json.load(f)

        warnings = get_user_warns(guild_id, user_id)

        for x in warnings:
            if x["warn"]["id"] == warn_id:
                jsonForm = {
                    "warn": {
                        "id": warn_id,
                        "reason": x["warn"]["reason"],
                        "staffID": x["warn"]["staffID"],
                    }
                }
                load[str(guild_id)][str(user_id)].remove(jsonForm)

    def add_warn(guild_id: int, user_id: int, staff_id: int, reason):
        with open("data/warns.json", "r") as f:
            load = json.load(f)

        numbers = string.digits
        random_num = random.sample(numbers, 5)
        code = "".join(random_num)

        jsonForm = {"warn": {"id": code, "reason": reason, "staffID": staff_id}}

        load[str(guild_id)][str(user_id)].append(jsonForm)

        with open("data/warns.json", "w") as f:
            json.dump(load, f, indent=4)

        return code

    @vbu.command(aliases=["ws", "warnings"])
    # this will make it required to have "ban members" permissions to use the command
    @commands.has_permissions(ban_members=True)
    async def warns(ctx, member: discord.Member):
        """Lists a members warns.

        .. Note::
            Must have ban members permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        check_if_guild_exists(ctx.guild.id)
        check_if_user_exists(ctx.guild.id, member.id)
        warns = get_user_warns(ctx.guild.id, member.id)

        if len(warns) == 0:
            embed = discord.Embed(color=member.color)
            embed.set_author(
                name=f"{member.name}'s warnings",
                icon_url=member.avatar_url,
                description=f"**{member}** has no warning records.",
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color=member.color)
        embed.set_author(name=f"{member.name}'s warnings", icon_url=member.avatar_url)

        for x in warns:
            warn = x["warn"]
            staff = vbu.get_user(warn["staffID"])
            embed.add_field(
                name=f"ID: {warn['id']}",
                value=f"**Reason:** {warn['reason']}\n**Staff:** {staff} ({staff.id})",
                inline=False,
            )

        await ctx.send(embed=embed)

    @vbu.command()
    @commands.has_permissions(kick_members=True)
    async def unwarn(ctx, member: discord.Member, warn_id: int):
        """Removes a members warn.

        .. Note::
            Must have kick members permission

        :param ctx: The invocation context.
        :param msg: The message the bot will repeat.
        """
        check_if_guild_exists(ctx.guild.id)
        check_if_user_exists(ctx.guild.id, member.id)
        remove_warn(ctx.guild.id, member.id, warn_id)

        embed = discord.Embed(
            color=member.color,
            description=f"✅ Removed warning **{warn_id}** from **{member}**",
        )


def setup(bot: vbu.Bot):
    x = Warns(bot)
    bot.add_cog(x)
