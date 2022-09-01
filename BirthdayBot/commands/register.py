import discord
from discord.ext import commands
import csv
from discord.ui import Button, View

class Registration(commands.Cog):
    """Class Dedicated to housing all commands related to registration"""
    def __init__(self, bot):
        self.bot = bot

    """ ---- COMMANDS ---- """
    @commands.command()
    async def bday(self, ctx):
        await self.sendRegistrationMessage(ctx)

        #Need to improve this validation
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.startswith("0")

        msg = await self.bot.wait_for('message', check=check)
        await ctx.send("{}, Your birthday ({}) has been stored in our database!".format(msg.author,msg.content))
        await self.sendConfirmationMessage(ctx)
        self.writeUserToCSV(username = msg.author,birthday = msg.content)

    """ ---- HELPERS ---- """
    async def sendConfirmationMessage(self, ctx):
        view = RegistrationButtons()
        await ctx.send("Is this correct?", view=view)
    
    
    async def sendRegistrationMessage(self, ctx):
        embed = discord.Embed(
            title = "Please enter your Birthday (Ex:07/11/01)",
            description = "This will store your birthday in our database",
            color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @staticmethod
    def writeUserToCSV(username: str, birthday: str):
        with open('DiscordBirthdays.csv', "a", newline="") as file:
            myFile = csv.writer(file)
            myFile.writerow([username, birthday])

async def setup(bot):
    await bot.add_cog(Registration(bot))


class RegistrationButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)  
        
    @discord.ui.button(label="Yes!",style=discord.ButtonStyle.green) # or .success
    async def green_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="No!",style=discord.ButtonStyle.red) # or .danger
    async def red_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
