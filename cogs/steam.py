import xml.etree.ElementTree as etree
import os
from dotenv import load_dotenv
import requests
from utils.tools import *

import discord
from discord.ext import commands
# Steam API
from steam.webapi import WebAPI
from steam.steamid import SteamID
from steam.enums import EPersonaState

load_dotenv('secrets.env')
token = os.getenv('STEAM_TOKEN')

steamAPI = WebAPI(token)

class Steam(commands.Cog,
            description='Commands for interacting with Steam.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='steamdebug', hidden=True)
    @commands.is_owner()
    async def steam_debug(self, ctx, *, shit: str):
        pass

    @commands.command(name='steamuser')
    async def get_steam_users(self, ctx, user_id:str):
        await ctx.channel.trigger_typing()
        steamID = SteamID.from_url("http://steamcommunity.com/id/{}".format(user_id))
        if steamID is None:
            steamID = user_id
        try:
            steam_user = steamAPI.ISteamUser.GetPlayerSummaries_v2(steamids=steamID)["response"]["players"][0]
        except IndexError:
            await ctx.send("User not found! Make sure you are using community IDs")
            return
        # Get steam user ban information
        # ban = steamAPI.ISteamUser.GetPlayerBans_v1(steamids=steamID)["players"][0]
        # vacBanned = ban["VACBanned"]
        # communityBan = ban['CommunityBanned']
        # ban_info = {"Vac Ban": vacBanned, "Community Ban":communityBan}
        # if vacBanned:
        #     ban_info['Vac Ban'] = ban['NumberOfVacBans']
        #     ban_info['Days Since Last VAC Ban'] = ban['DaysSinceLastBan']
        if steam_user['communityvisibilitystate'] != 3:
            embed = discord.Embed(title=steam_user['personaname'], description="This profile is private.", color=0xFF0000, url=steam_user['profileurl'])
            embed.set_thumbnail(url=steam_user['avatarfull'])
            await ctx.send(embed=embed)
            return

        # Get list of games the steam user has played
        games = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}".format(token, steamID)).json()["response"]
        played_games = games['game_count']

        friend_list = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(token, steamID)).json()["friendslist"]
        friends = friend_list['friends']
        friend_count = len(friends)

        status = {0:'Offline', 1:'Online', 2:'Busy', 3:'Away', 4:'Snooze', 5:'Looking to trade', 6:'Looking to play'}
        colors = {0:0xFF0000, 1:0x00FF00, 2:0xFFd200, 3:0x00ebff, 4:0x808080, 5: 0xae62ff, 6: 0x9922ff}
        embed = discord.Embed()
        # embed = make_list_embed(ban_info)
        embed.title = '{}'.format(steam_user['personaname'])
        #embed.add_field(name=status[steam_user['personastate']], value="***{}***".format(status[steam_user['personastate']]), inline=False)
        
        embed.description = '***{}***'.format(status[steam_user['personastate']])
        embed.color = colors[steam_user['personastate']]
        embed.url = steam_user['profileurl']
        embed.set_thumbnail(url=steam_user['avatarfull'])
        embed.add_field(name="Games", value=played_games, inline=False)
        embed.add_field(name="Friends", value=friend_count, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Steam(bot))