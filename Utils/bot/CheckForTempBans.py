import datetime
from discord.ext import commands
from firebase_admin import db
import discord
from ..Debug.Messages import Alert, Succed, info
Sq = []

class RemoveView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.uid = False
        self.author = None

    @discord.ui.button(label="✔️", style=discord.ButtonStyle.green)
    async def remove(self, interaction : discord.Interaction, button : discord.ui.Button):
        if interaction.user.name == self.author:
            try:
                ref = db.reference(f"Punishments/{self.uid}")
                ref.delete()
                embed = discord.Embed(title="Removed correctly!",description=f"uid : {self.uid} was removed successfully",color=discord.Color.green())
                self.disabled = True
            except Exception as e:
                embed = discord.Embed(title=f"Error while deleting : {self.uid}",description=f"Error : {e}",color=discord.Color.red())
            
            await interaction.response.send_message(embed=embed)
            return
        else:
            embed = discord.Embed(title="Only the user that created this punishment can decide",description="Only the user that created this punishment can decide",color=discord.Color.red()) 
            await interaction.response.send_message(embed=embed)
            return
    
    @discord.ui.button(label="❎", style=discord.ButtonStyle.red)
    async def dont(self, interaction : discord.Interaction, button : discord.ui.Button):
        if interaction.user.name == self.author:
            self.disabled = True
            embed = discord.Embed(title="Done!",description=f"uid : {self.uid}",color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
            return
        else:
            embed = discord.Embed(title="Only the user that created this punishment can decide",description="Only the user that created this punishment can decide",color=discord.Color.red()) 
            await interaction.response.send_message(embed=embed)
            return

def GetTime():
    now = datetime.datetime.now()

    return now.strftime("%d/%m/%Y %H:%M")

async def SearchForTerminateBan(bot : commands.Bot):
    log_channel = 1208151847974473889

    channel = bot.get_channel(log_channel)
    if channel:
        data = db.reference("/Punishments").get()
        for uid in data:
            date = GetTime()
            try:
                dbDate = str(data[uid]['Date'])
                if str(dbDate) == str(date):
                    if uid not in Sq:
                        Sq.append(uid)
                        name = str(data[uid]['User'])
                        user = discord.utils.get(bot.users, name=name)
                        info(f"Punishment : {uid} has to be unbaned! (Created by : {user.name}, in {data[uid]['Made']}), unban : {data[uid]['Names']} - {data[uid]['Steam IDs']}")
                        req = RemoveView()
                        req.uid = uid
                        req.author = name
                        embed = discord.Embed(title="TEMP BAN",description=f"Hey {user.name}, You have to UNBAN this name(s) : {data[uid]['Names']} with Steam IDs : {data[uid]['Steam IDs']}, you made this punishment the day : {data[uid]['Made']}! ",color=discord.Color.greyple())
                        embed.add_field(name="REMOVE PUNISHMENT FROM DATABASE?",value="",inline=False)
                        await channel.send(embed=embed,view=req)
                        await channel.send(user.mention)
            except Exception as e:
                print(e)
                pass