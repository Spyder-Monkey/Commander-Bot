import discord
from discord.ext import commands

from database import DbModel

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Load cog
    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("***`ERROR:`***")
        else:
            await ctx.send("***`SUCCESS`***")

    # Unload cog
    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, * cog: str):
        print(cog)
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("***`ERROR:`***")
        else:
            await ctx.send("***`SUCCESS:`***")

    # Reload cog
    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("***`ERROR:`***")
        else:
            await ctx.send("***`SUCCESS:`***")

    # Shutdown bot
    @commands.command(name="shutdown", hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.logout()

    # Set bot status to offline
    @commands.command(name="sleep", hidden=True)
    @commands.is_owner()
    async def go_idle(self, ctx):
        await self.bot.change_presence(status=discord.Status.offline)

    # Set bot status to online
    @commands.command(name="awake", hidden=True)
    @commands.is_owner()
    async def awake(self, ctx):
        await ctx.channel.send("It's tickle time!")
        await self.bot.change_presence(status=discord.Status.online)

    # Drops all tables in database WILL BE REMOVED AFTER TESTING
    @commands.command(name="drop_tables", hidden=True)
    @commands.is_owner()
    async def drop_tables(self, ctx):
        DbModel.drop_tables()
        

def setup(bot):
    bot.add_cog(Owner(bot))