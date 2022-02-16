import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random

from emojis.uwuList import uwu

class Misc(commands.Cog,
            description="Miscellaneous commands."):
    def __init__(self, bot):
        self.bot = bot

    # Command to get the amount of signatures on the Cyber Cafe petition
    # using web scraping
    @commands.command(
        name="signatures",
        help=u'\u200b',
        brief="Get the signature count of the Cyber Cafe petition."
    )
    async def get_signatures(self, ctx):
        URL = "https://www.change.org/p/bring-back-cyber-cafe"

        await ctx.send("Let me check the petition right quick one guy...")
        #test = self.check_time()
        # Make it appear as if the bot is typing
        async with ctx.typing():
            # Set options for the firefox browser and make it so it does not appear
            firefox_options = Options()
            firefox_options.add_argument("--headless")

            # Open Firefox using geckodriver
            # Gets URL of petition and waits until the page has loaded.
            # 
            # Bot then sleeps for another 10 seconds because change.org decided that 
            # they needed to have the signature number trickle and make my life harder
            with Firefox(options=firefox_options, executable_path=r'C:\\WebDrivers\\bin\\geckodriver') as browser:
                browser.get(URL)
                WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'html')))
                time.sleep(10)
                html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        # Get the petition title from web page
        banner = soup.body.h1.text
        # get the number of signatures from petition
        sign_count = soup.body.strong.span.text
        # Create the embed to send info to channel
        embed = discord.Embed(title="**"+banner+"**", description=sign_count)
        # JUST SEND IT BUD
        await ctx.send(embed=embed)

    @commands.command(
        name="uwu",
        help="<message>",
        brief="Converts a message to UwU speech."
    )
    async def uwuify(self, ctx):
        uwu_rules_dict = {
            'l': 'w',
            'r': 'w',
            'th': 'ff',
            'ove': 'uv',
            'osh': 'awsh',
            '!': '! ' + uwu[int(random.uniform(0, len(uwu)))]
        }
        uwu_message = ""
        
        # UWU Rules needing to be implemented
        # "N + <Vowel>" = "Ny + <Vowel>" (e.g. No = Nyo)


        for word in ctx.message.content.split():
            if word == "$uwu": continue
            for key, value in uwu_rules_dict.items():
                if word.find(key) > -1:
                    word = word.replace(key, value)
            uwu_message += word + " "
        
        uwu_message += uwu[int(random.uniform(0, len(uwu)))]

        await ctx.channel.send(uwu_message)



def setup(bot):
    bot.add_cog(Misc(bot))