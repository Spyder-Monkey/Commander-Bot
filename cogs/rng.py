import discord
from discord.ext import commands
import random

class RNG(commands.Cog,
            description="Commands the utilize random number generation."):
    def __init__(self, bot):
        self.bot = bot

    # Roll Command Value
    @commands.command(
        name="roll",
        help="<value1> <value2> ...",
        brief="Return random item from list if more than one value is entered. Otherwise, returns a random number between 1 and [value]"
    )
    async def roll(self, ctx, *value):
        # Choose random index from tuple is length greater than 1
        if len(value) > 1:
            await ctx.channel.send('{}'.format(value[int(random.uniform(0, len(value)))]))
        # Choose random value between 1 and value[0] if length is 1
        elif len(value) == 1:
            await ctx.channel.send('I rolled a {:.0f}'.format(random.uniform(1, int(value[0]))))
        # User entered wrong format
        else:
            await ctx.channel.send("Error")

    # Coin Flip Command
    @commands.command(
        name="flip",
        help=u'\u200b',
        brief="Flips a coin and returns Heads or Tails"
    )
    async def flip(self, ctx):
        await ctx.channel.send(random.choice(["Heads", "Tails"]))

    # 8ball Command
    @commands.command(
        name="8ball",
        help="<question>",
        brief="Returns an answer from the magic 8 ball."
    )
    async def eight_ball(self, ctx, message):
        await ctx.channel.send(random.choice(open('txts/8ball.txt').read().splitlines()))


def setup(bot):
    bot.add_cog(RNG(bot))