import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from database import DbModel
from emojis import EmojiList

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojiLetters = EmojiList.emojiLetters

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
        message = message[last+1:]
        return self.get_options(message, options)


    @commands.cooldown(100,60,BucketType.user)
    @commands.command(name="poll")
    async def poll(self, ctx):
        message = ctx.message
        if not message.author.bot:
            if message.content.startswith("$poll"):
                messageContent = message.clean_content
                if messageContent.find('[') == -1:
                    # set the title of the poll
                    title = self.get_title(messageContent)
                    # Create the emebed content for the poll
                    e = discord.Embed(title="***" + title + "***",
                    description=title, colour=0x83bae3)
                    # send the embedded poll to the channel
                    msg = await message.channel.send(embed=e)
                    # CREATE POLL IN DATABASE WITHOUT CUSTOM OPTIONS
                    new_poll = DbModel.create_new_poll(msg.id, title, message.author)
                    # Add reactions to poll message for voting
                    await msg.add_reaction(EmojiList.defaultEmojis[0])
                    await msg.add_reaction(EmojiList.defaultEmojis[1])
                    await msg.add_reaction(EmojiList.defaultEmojis[2])
                else:
                    title = self.get_title(messageContent)
                    options = self.get_options(messageContent, [])
                    # User entered invalid syntax for the command.
                    if options == "You are not using the command properly.":
                        await message.channel.send(options)
                        return
                    try:
                        pollMessage = ""
                        i = 0
                        for choice in options:
                            if not options[i] == "":
                                if len(options) > 26:
                                    await message.channel.send("Please use the command correctly and have less than 21 options.")
                                    return
                                elif not i == len(options):
                                    pollMessage = pollMessage + "\n\n" + self.emojiLetters[i] + " " + choice
                            i+=1

                        e = discord.Embed(title="**" + title + "**",
                            description=pollMessage, colour=0x83bae3)
                        pollMessage = await message.channel.send(embed=e)

                        # CREATE POLL IN DATABASE HERE WITH CUSTOM OPTIONS
                        new_poll = DbModel.create_new_poll(pollMessage.id, title, message.author)

                        i=0
                        for choice in options:
                            if not i == len(options) and not options[i] == "":
                                new_option = DbModel.create_new_option(choice, new_poll.poll_id)
                                await pollMessage.add_reaction(self.emojiLetters[i])
                            i+=1
                    except KeyError:
                        return "Please make sure you are using the format '$poll {title} [option1] [option2] [option3]'"
                # Delete the message sent by the user to keep server from getting cluttered. 
                await message.delete()
        else:
            return

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command(name='polllist')
    async def get_poll_list(self, ctx):
        polls = DbModel.Poll.select()
        embed = discord.Embed(title=f"__**Poll List**__", color=0xffff00, timestamp=ctx.message.created_at)
        for poll in polls:
            poll_title = poll.poll_name[:15] + "..."
            embed.add_field(name=f'**Title: {poll_title}**', value=f'ID: {poll.poll_id}\nAuthor: {poll.poll_creator}\nTimestamp: {poll.create_date}', inline=False)

        await ctx.channel.send(embed=embed)

    @commands.command(name="results")
    async def poll_results(self, ctx, poll_name):
        pass

def setup(bot):
    bot.add_cog(Poll(bot))