## Copied and modified from https://github.com/Twentysix26/26-Cogs ##

try:
    from cleverbot import Cleverbot as Clv
except:
    Clv = False
from discord.ext import commands
from cogs.utils import checks
from .utils.dataIO import dataIO
from __main__ import send_cmd_help, user_allowed
import os
import discord
import asyncio
import re
import datetime

class Cleverbot():
    """Cleverbot"""

    def __init__(self, bot):
        self.bot = bot
        self.clv = Clv()
        self.settings = dataIO.load_json("data/cleverbot/settings.json")
        self.greeting = re.compile(r"\bmorning\b|\bafternoon\b|\bevening\b", re.IGNORECASE)
        self.targets = re.compile(r"\beveryone\b|\bpeoples*\b|\bdudes*\b|\bevery1\b|\bguys\b", re.IGNORECASE)
        self.history = {"LastDay": 0}

    @commands.group(no_pm=True, invoke_without_command=True)
    async def cleverbot(self, *, message):
        """Talk with cleverbot"""
        result = await self.get_response(message)
        await self.bot.say(result)

    @cleverbot.command()
    @checks.is_owner()
    async def toggle(self):
        """Toggles reply on mention"""
        self.settings["TOGGLE"] = not self.settings["TOGGLE"]
        if self.settings["TOGGLE"]:
            await self.bot.say("I will reply on mention.")
        else:
            await self.bot.say("I won't reply on mention anymore.")
        dataIO.save_json("data/cleverbot/settings.json", self.settings)

    async def get_response(self, msg):
        question = self.bot.loop.run_in_executor(None, self.clv.ask, msg)
        try:
            answer = await asyncio.wait_for(question, timeout=10)
        except asyncio.TimeoutError:
            answer = "We'll talk later..."
        return answer

    async def on_message(self, message):
        now = datetime.datetime.now()

        if not self.settings["TOGGLE"] or message.channel.is_private:
            return

        if not user_allowed(message):
            return
        
        if now.day != self.history["LastDay"]:
            self.history = {"LastDay": now.day}

        if message.author.id != self.bot.user.id:
            mention = message.server.me.mention
            if message.content.find(mention) >= 0:
                content = message.content.replace(mention, "").strip()
                await self.bot.send_typing(message.channel)
                response = await self.get_response(content)
                await self.bot.send_message(message.channel, response)
            elif self.greeting.search(message.content) and self.targets.search(message.content) and str(message.author.id) not in self.history.keys():
                self.history[str(message.author.id)] = True
                content = message.content.replace(mention, "").strip()
                await self.bot.send_typing(message.channel)
                response = await self.get_response(content)
                await self.bot.send_message(message.channel, response)

def check_folders():
    if not os.path.exists("data/cleverbot"):
        print("Creating data/cleverbot folder...")
        os.makedirs("data/cleverbot")

def check_files():
    f = "data/cleverbot/settings.json"
    data = {"TOGGLE" : True}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)

def setup(bot):
    if Clv is False:
        raise RuntimeError("You're missing the cleverbot library.\n"
                           "Install it with: 'pip3 install cleverbot' "
                           "and reload the module.")
    check_folders()
    check_files()
    n = Cleverbot(bot)
    bot.add_cog(n)
