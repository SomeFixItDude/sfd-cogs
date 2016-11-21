import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from __main__ import send_cmd_help
import os
import asyncio

default_rules = "Welcome to the server!"
default_settings = {"RULES": default_rules, "RULESON": False}

class JoinRules:
    """Sends new members a direct pm with the server rules"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/joinrules/settings.json", "load")

    @commands.group(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def joinrules(self, ctx):
        """Sets joinrules module settings"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = default_settings
            fileIO("data/joinrules/settings.json","save",self.settings)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            msg = "```"
            msg += "RULES: {}\n".format(self.settings[server.id]["RULES"])
            msg += "RULESON: {}\n".format(self.settings[server.id]["RULESON"])
            msg += "```"
            await self.bot.say(msg)

    @joinrules.command(pass_context=True)
    async def rules(self, ctx, *, format_msg):
        """Sets the rules message format for the server.

        {0} is user
        {1} is server
        Default is set to: 
            Welcome to the server!
        """
        server = ctx.message.server
        self.settings[server.id]["RULES"] = format_msg
        fileIO("data/joinrules/settings.json","save",self.settings)
        await self.bot.say("Rules message set for the server.")
        await self.send_testing_rulesmsg(ctx)

    @joinrules.command(pass_context=True)
    async def togglerules(self, ctx):
        """Turns on/off sending rules new users to the server"""
        server = ctx.message.server
        self.settings[server.id]["RULESON"] = not self.settings[server.id]["RULESON"]
        if self.settings[server.id]["RULESON"]:
            await self.bot.say("I will now send rules to new users of the server.")
            await self.send_testing_rulesmsg(ctx)
        else:
            await self.bot.say("I will no longer send rules to new users of the server.")
        fileIO("data/joinrules/settings.json", "save", self.settings)

    async def member_join(self, member):
        server = member.server
        if server.id not in self.settings:
            self.settings[server.id] = default_settings
            self.settings[server.id]["CHANNEL"] = server.default_channel.id
            fileIO("data/joinrules/settings.json","save",self.settings)
        if self.settings[server.id]["RULESON"]:
            await self.bot.send_message(member, self.settings[server.id]["RULES"].format(member, server))

    async def send_testing_rulesmsg(self, ctx):
        server = ctx.message.server
        await self.bot.send_message(ctx.message.author, self.settings[server.id]["RULES"].format(ctx.message.author, server))

def check_folders():
    if not os.path.exists("data/joinrules"):
        print("Creating data/joinrules folder...")
        os.makedirs("data/joinrules")

def check_files():
    f = "data/joinrules/settings.json"
    if not fileIO(f, "check"):
        print("Creating welcome settings.json...")
        fileIO(f, "save", {})
    else: #consistency check
        current = fileIO(f, "load")
        for k,v in current.items():
            if v.keys() != default_settings.keys():
                for key in default_settings.keys():
                    if key not in v.keys():
                        current[k][key] = default_settings[key]
                        print("Adding " + str(key) + " field to welcome settings.json")
        fileIO(f, "save", current)

def setup(bot):
    check_folders()
    check_files()
    n = JoinRules(bot)
    bot.add_listener(n.member_join,"on_member_join")
    bot.add_cog(n)
