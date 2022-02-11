import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import threading

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_time(self):
        threading.Timer(1, self.check_time).start()

        now = datetime.now()

        print(now)

        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)

        return now

        
    # Command to get the amount of signatures on the Cyber Cafe petition
    # using web scraping
    @commands.command(name="signatures")
    async def get_signatures(self, ctx):
        URL = "https://www.change.org/p/bring-back-cyber-cafe"

        await ctx.send("Let me check the petition right quick one guy...")
        test = self.check_time()
        async with ctx.typing():

            firefox_options = Options()
            firefox_options.add_argument("--headless")

            with Firefox(options=firefox_options, executable_path=r'C:\\WebDrivers\\bin\\geckodriver') as browser:
                browser.get(URL)
                WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'html')))
                time.sleep(10)
                html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')

        banner = soup.body.h1.text
        sign_count = soup.body.strong.span.text

        embed = discord.Embed(title="**"+banner+"**", description=sign_count)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Misc(bot))