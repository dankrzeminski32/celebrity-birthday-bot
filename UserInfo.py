import csv
import discord
from csv import reader
from datetime import datetime
from datetime import date
from discord.ext import commands
from discord.utils import get

# Create permission intents, state what our bot should be able to do
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = ".", intents = intents)

class UserAgeInfo(commands.Cog):

    def __init__(self, bot):
        self.csvFile = "DiscordBirthdays.csv"
        self.bot = bot

    """ ---- COMMANDS ---- """
    @commands.command()
    async def test(self, ctx, arg):

        def check(arg):
            return arg.author == ctx.author and arg.channel == ctx.channel
        
        arg = arg[2:len(arg)]
        arg = arg[:-1]

        birthdate = []
        with open(self.csvFile) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row[2] == arg:
                    birthdate = row[1]
        
        userAge = self.getUserAge(birthdate)
        numDays = self.daysAway(birthdate)
        print(userAge)
        print(numDays)
    
    """ ---- HELPERS ---- """
    def getUserAge(self, birthdate):
        today = date.today()
        today = today.strftime("%m/%d/%Y")

        age = int(today[-4:]) - int(birthdate[-4:]) - ((int(today[:1]), int(today[3:5])) < (int(birthdate[:1]), int(birthdate[3:5])))
        return age

    def daysAway(self, birthdate):
        today = date.today()
        #date_format = "%m/%d/%Y"
        today = datetime.today()
        birthdate = datetime.strptime(birthdate,'%m/%d')

        days = (today - birthdate).days
        return days

async def setup(bot):
    await bot.add_cog(UserAgeInfo(bot))
#test = UserAgeInfo("DiscordBirthdays.csv", bot)