import discord
from discord.ext import commands
from discord.errors import Forbidden

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey there guy, looks like you don't have permission for that.")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)

class Help(commands.Cog):
    """
        Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx, *input):
        """ Shows all modules of that bot """
        prefix = '$'

        # Setting owner name
        owner = 433332926935990293
        owner_name = 'Spyder#5038'

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as err:
                owner = owner

            # starting to build embed
            embed = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                    description=f'Use `{prefix}help <module>` to gain more information about that module '
                                                f':smiley:\n')

            # iterating through cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                if (cog == 'Owner' and str(ctx.message.author) != owner_name) or cog == 'Help': continue
                cogs_desc += f'**`{cog}`** {self.bot.cogs[cog].description}\n'

            # adding list of cogs to embed
            embed.add_field(name='Modules', value=cogs_desc, inline=True)

            # iterating through uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # set the footer of the embed
            embed.set_footer(text=f"Please report any bugs to {owner_name}")

            # adding those commands to embed
            if commands_desc:
                embed.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

        elif len(input) == 1:
            # iterating through cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():
                    # making title - getting description from doc-string below class
                    embed = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].description, color=discord.Color.green())

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            embed.add_field(name=f'`{prefix}{command.name} {command.help}`', value=command.brief, inline=False)
                    # found cog - break from loop
                    break
                else:
                    embed = discord.Embed(title="What's that?!",
                                            description=f"I've never heard of a module called `{input[0]}` before :scream:",
                                            color=discord.Color.orange())
        elif len(input) > 1:
            embed = discord.Embed(title="That's too much guy.",
                                    description="Please request only one module at once :sweat_smile:",
                                    color=discord.Color.orange())
        else:
            embed = discord.Embed(title="It's a magical place.",
                                    description="I don't know how you get here. But I didn't see this coming at all.\n"
                                    "Would you please be so kind to report that issue to `{owner.nickname}`?\n"
                                    "I do appreciate it!",
                                    color=discord.Color.red())
        # sending reply embed using function defined above
        await send_embed(ctx, embed)

def setup(bot):
    bot.add_cog(Help(bot))
        