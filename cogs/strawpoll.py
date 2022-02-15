import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from dotenv import load_dotenv
import os
import requests

load_dotenv('secrets.env')

class StrawPoll(commands.Cog,
                description="Creates a StrawPoll link for users to vote."):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("STRAWPOLL_TOKEN")

    def get_title(self, message):
        first = message.find('{')+1
        last = message.find('}')

        if first == 0 or last == -1:
            return "You are not using the command properly."
        return message[first:last]

    def get_options(self, message, options):
        first = message.find('[')+1
        last = message.find(']')

        if first == 0 or last == -1:
            if len(options) < 2:
                return "You are not using the command properly."
            else:
                return options
        options.append(message[first:last])
        message=message[last+1:]
        return self.get_options(message, options)

    @commands.command(
        name='strawpoll',
        help='{question} [Answer1] [Answer2] ...',
        brief="Create a Strawpoll link."
    )
    @commands.cooldown(2,60,BucketType.user)
    async def strawpoll(self, ctx):
        if not ctx.message.author.bot:
            print(ctx.message.content)
            message = ctx.message.clean_content
            title = self.get_title(message)
            options = self.get_options(message, [])

            try:
                data = {
                    "poll": {
                        "priv": False,
                        "title": title,
                        "answers": options,
                        "ma": False,
                        "mip": False,
                        "enter_name": False,
                        "only_reg": False,
                        "vpn": True,
                        "captcha": False
                    }
                }
                poll = requests.post("https://strawpoll.com/api/poll", json=data, headers={'API-KEY': self.api_key}).json()
                await ctx.channel.send("https://strawpoll.com/" + str(poll["content_id"]))

            except KeyError:
                return "Please make sure you are using the format '$strawpoll {title} [Option1] [Option2] [Option3]'"
    
    @strawpoll.error
    async def strawpoll_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

def setup(bot):
    bot.add_cog(StrawPoll(bot))
