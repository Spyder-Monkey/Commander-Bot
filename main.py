import discord
from bot import CommanderBot
import json

with open('config.json') as config_file:
    config = json.load(config_file)

client = CommanderBot(config)
client.run()
