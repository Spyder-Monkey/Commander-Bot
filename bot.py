import discord
from discord.utils import get
import os
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp
from database import DbModel

load_dotenv('secrets.env')
API_TOKEN = os.getenv('DISCORD_TOKEN')

extensions = (
    "cogs.poll",
    "cogs.strawpoll",
    "cogs.owner",
    "cogs.rng",
    "cogs.conversions"
)

class CommanderBot(commands.AutoShardedBot):
    def __init__(self, config):
        prefix = "$"
        super().__init__(
            command_prefix = prefix,
            status = discord.Status.online,
            activity = discord.Game(name="with your feelings")
        )
        self.config = config
        self.shard_count = self.config["shards"]["count"]
        shard_ids_list = []
        shard_ids = []

        for i in range(self.config["shards"]["first_shard_id"], self.config["shards"]["last_shard_id"]+1):
            shard_ids_list.append(i)
        self.shard_ids = tuple(shard_ids_list)

        for extension in extensions:
            self.load_extension(extension)

    async def on_ready(self):
        print('Logging in...\t\t', end='')
        self.http_session = aiohttp.ClientSession()
        print('SUCCESS')
        print("\n------------")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------------")

    # Triggered each time a message is sent in chat
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    # Triggered each time a user adds a reaction to a message
    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        userid = payload.user_id
        reactions = message.reactions
        # Current reaction being added to
        reaction = get(message.reactions, emoji=payload.emoji.name)

        for i in range(len(reactions)):
            # Remove any duplicate votes if user changes mind.
            reaction_users = await reactions[i].users().flatten()
            if reaction == reactions[i]: continue
            else:
                user = None
                for x in reaction_users:
                    if x.id == userid: 
                        user = x
                # Remove reaction if user has made a previous choice and
                # is reacting to a message sent by bot
                if user is not None and message.author == self.user:
                    await reactions[i].remove(user)
            # Remove any user added reactions
            if message.author == self.user and not reactions[i].me:
                reactions.pop(i)

    def run(self):
        DbModel.init_tables()
        super().run(API_TOKEN, reconnect=True)
        DbModel.db.close()
