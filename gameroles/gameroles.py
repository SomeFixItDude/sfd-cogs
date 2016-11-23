#https://raw.githubusercontent.com/Rapptz/discord.py/fb1f9ac65977f82cbec2ab89f975fa8b21eb48f9/docs/api.rst
import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from __main__ import send_cmd_help
import os
import asyncio

class GameRoles:
    """Auto-create roles based on games played by users"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/gameroles/settings.json", "load")
        self.games = fileIO("data/gameroles/games.json", "load")

    @commands.group(pass_context=True, no_pm=True)
    async def gameroles(self, ctx):
        """Sets gameroles module settings"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
            self.games[server.id] = {}
            fileIO("data/gameroles/settings.json","save",self.settings)
            fileIO("data/gameroles/games.json","save",self.games)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            msg = "```"
            msg += "leave [game name] - Removes you from the role\n"
            msg += "  example: [p]gameroles leave GangBeasts\n"
            msg += "join [game name] - Adds you to a role\n"
            msg += "  example: [p]gameroles join GangBeasts\n"
            msg += "list - Lists available game roles\n"
            msg += "  example: [p]gameroles list\n"
            msg += "exclude [game name] - Exlcude a game from auto role\n"
            msg += "  example: [p]gameroles exclude GangBeasts\n"
            msg += "```"
            await self.bot.say(msg)
    
    async def member_update(self, before, after):
        server = member.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
            self.games[server.id] = {}
            fileIO("data/gameroles/settings.json","save",self.settings)
            fileIO("data/gameroles/games.json","save",self.games)


def check_setup():
    if not os.path.exists("data/gameroles"):
        print("Creating data/gameroles folder")
        os.makedirs("data/gameroles")

    if not fileIO("data/gameroles/settings.json", "check"):
        print("Creating welcome settings.json")
        fileIO("data/gameroles/settings.json", "save", {})

    if not fileIO("data/gameroles/games.json", "check"):
        print("Creating welcome games.json")
        fileIO("data/gameroles/games.json", "save", {})

def setup(bot):
    check_setup()
    n = GameRoles(bot)
    bot.add_listener(n.member_update,"on_member_update")
    bot.add_cog(n)
