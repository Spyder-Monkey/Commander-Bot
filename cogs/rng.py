import discord
from discord.ext import commands
import random

class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Roll Command Value
    @commands.command(
        name="roll",
        help="Used to get a random number between 1 and [value].",
        brief=": Returns a random number between 1 and [value]."
    )
    async def roll(self, ctx, value):
        # Check type of value and if it is list, get random from list
        # if it is int, do below
        print(type(value))
        print(value)
        await ctx.channel.send('I rolled a {:.0f}'.format(random.uniform(1, int(value))))
    # Roll Command List
    @commands.command(
        help="Used to get a random value from a list seperated by commas.",
        brief=": Returns a random value from [list], seperate values with a comma."
    )
    async def roll_list(self, ctx, lst):
        pass

    # Coin Flip Command
    @commands.command(
        name="flip",
        help="",
        brief=": Flips a coin and returns Heads or Tails"
    )
    async def flip(self, ctx):
        await ctx.channel.send(random.choice(["Heads", "Tails"]))

    # 8ball Command
    @commands.command(
        name="8ball",
        help="",
        brief=": Returns an answer from the magic 8 ball."
    )
    async def eight_ball(self, ctx, message):
        await ctx.channel.send(random.choice(open('txts/8ball.txt').read().splitlines()))


def setup(bot):
    bot.add_cog(RNG(bot))