import discord
from discord.ext import commands

from database import DbModel

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Load cog
    @commands.command(
        name="load", 
        brief="Load command(s).",
        hidden=True
    )
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("***`ERROR:`***")
        else:
            await ctx.send("***`SUCCESS`***")

    # Unload cog
    @commands.command(
        name="unload", 
        brief="Unload command(s).",
        hidden=True
    )
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
    @commands.command(
        name="reload", 
        brief="Reload command(s).",
        hidden=True
    )
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
    @commands.command(
        name="kill", 
        brief="Log the bot out.",
        hidden=True
    )
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.logout()

    @commands.command(
        name="status",
        help='<status>',
        brief="Set the status of the Bot.",
        hidden=True
    )
    @commands.is_owner()
    async def set_status(self, ctx, new_status):
        new_status = new_status.lower()

        print("New Bot Status: ", end='')
        match new_status:
            case 'online':
                self.bot.is_awake = True
                await self.bot.change_presence(status=discord.Status.online)
                await ctx.channel.send("IT'S TICKLE TIME!")
            case 'offline':
                self.bot.is_awake = False
                await self.bot.change_presence(status=discord.Status.offline)
            case 'idle':
                self.bot.is_awake = False
                await self.bot.change_presence(status=discord.Status.idle)
            case 'invisible':
                self.bot.is_awake = False
                await self.bot.change_presence(status=discord.Status.invisible)
            case 'dnd':
                self.bot.is_awake = False
                await self.bot.change_presence(status=discord.Status.dnd)
            case _:
                new_status = 'INVALID'
                await ctx.channel.send("Not a valid status.")

        print(new_status)

    # Drops all tables in database WILL BE REMOVED AFTER TESTING
    @commands.command(
        name="drop_tables", 
        brief="Drop poll tables. USED FOR TESTING ONLY",
        hidden=True
    )
    @commands.is_owner()
    async def drop_tables(self, ctx):
        DbModel.drop_tables()
        

def setup(bot):
    bot.add_cog(Owner(bot))