from discord.ext import commands
from firebase_admin import db, credentials
import asyncio
import discord

tribe_warnings = {}

def GetTotalWarnings(TribeName):
    data = db.reference("/Punishments").get()
    Seasonal = 0
    Permanent = 0
    Verbal = 0

    for uid in data:
        if data[uid]['Tribe Name'] == TribeName:
            try:
                data[uid]['TempBan']
            except:
                
                if data[uid]['Warning_type'] == "Seasonal Warning":
                    Seasonal += data[uid]['Warnings']
                elif data[uid]['Warning_type'] == "Permanent Warning":
                    Permanent += data[uid]['Warnings']
                elif data[uid]['Warning_type'] == "Verbal Warning":
                    Verbal += data[uid]['Warnings']

    return Seasonal, Permanent, Verbal

def updateWarnings():
    global tribe_warnings
    data = db.reference("/Punishments").get()

    for uid in data:
        tribe_warnings[data[uid]['Tribe Name']] = {"Seasonal Warning":0,"Permanent Warning":0,"Verbal Warning":0}

    for uid in data:
        Seasonal, Permanent, Verbal = GetTotalWarnings(data[uid]['Tribe Name'])
        if tribe_warnings[data[uid]['Tribe Name']]['Seasonal Warning'] != Seasonal:
            tribe_warnings[data[uid]['Tribe Name']]['Seasonal Warning'] = Seasonal
        elif tribe_warnings[data[uid]['Tribe Name']]['Permanent Warning'] != Permanent:
            tribe_warnings[data[uid]['Tribe Name']]['Permanent Warning']  = Permanent
        elif tribe_warnings[data[uid]['Tribe Name']]['Verbal Warning'] != Verbal:
            tribe_warnings[data[uid]['Tribe Name']]['Verbal Warning'] = Verbal

async def GetActions(bot : commands.Bot):
    global tribe_warnings
    updateWarnings()
    for name in tribe_warnings:
        if tribe_warnings[name]['Seasonal Warning'] > 3:
            ref = db.reference("/Warned").get()
            found = False
            for tribename in ref:
                if tribename == name:
                    found = True

            if found == False:
                db.reference("/Warned").update({name : {"Usable":True}})
                get_channel = bot.get_channel(1073357812786282536)
                embed = discord.Embed(title="YOU NEED TO TAKE ACTIONS",description=f"Tribe Name : {name}",color=discord.Color.dark_blue())
                embed.add_field(name=f"Seasonal Warnings",value=tribe_warnings[name]['Seasonal Warning'])
                embed.add_field(name=f"Permanent Warnings",value=tribe_warnings[name]['Permanent Warning'])
                embed.add_field(name=f"Verbal Warnings",value=tribe_warnings[name]['Verbal Warning'])

                await get_channel.send(embed=embed)
      
            
