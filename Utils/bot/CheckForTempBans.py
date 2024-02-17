import datetime
from discord.ext import commands
from firebase_admin import db
import discord
import re

def GetTime():
    now = datetime.datetime.now()

    return now.strftime("%d/%m/%Y %H:%M")

async def SearchForTerminateBan(bot : commands.Bot):
    log_channel = 1073357812786282536

    channel = bot.get_channel(log_channel)
    if channel:
        data = db.reference("/TempBans").get()
        
        for uid in data:
            date = GetTime()
            
            print(date, str(data[uid]['Date']))
            if re.findall(str(data[uid]['User']), date, re.IGNORECASE):
                print("MATCH")
                name = str(data[uid]['User'])
                user = discord.utils.get(bot.users, name=name)
                embed = discord.Embed(title="TEMP BAN",description=f"Hey {user.mention}, You have to UNBAN this name(s) : {data[uid]['Names']} with Steam IDs : {data[uid]['Steam IDs']}!",color=discord.Color.greyple())
                ref = db.reference(f"/TempBans/{uid}")
                ref.delete()
                await channel.send(embed=embed) 