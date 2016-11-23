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

    @commands.group(pass_context=True, no_pm=True)
    async def gameroles(self, ctx):
        """Sets gameroles module settings"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
            self.games[server.id] = {}
            self.gamealias[server.id] = {}
            fileIO("data/gameroles/settings.json","save",self.settings)
            fileIO("data/gameroles/games.json","save",self.games)
            fileIO("data/gameroles/gamealias.json","save",self.gamealias)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            msg = "```"
            msg += "leave [game name] - Removes you from the role"
            msg += "  example: [p]gameroles leave GangBeasts"
            msg += "join [game name] - Adds you to a role"
            msg += "  example: [p]gameroles join GangBeasts"
            msg += "list - Lists available game roles"
            msg += "  example: [p]gameroles list"
            msg += "exclude [game name] - Exlcude a game from auto role"
            msg += "  example: [p]gameroles exclude GangBeasts"
            msg += "```"
            await self.bot.say(msg)

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

    if not fileIO("data/gameroles/gamealias.json", "check"):
        print("Creating welcome gamealias.json")
        fileIO("data/gameroles/gamealias.json", "save", {})

def setup(bot):
    check_setup()
    bot.add_cog(GameRoles(bot))