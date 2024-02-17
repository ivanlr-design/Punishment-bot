from discord.ext import commands
import datetime
import os
import discord
import firebase_admin
from firebase_admin import db, credentials
import time
from discord import app_commands
import random
import json
import typing
import string
import asyncio
from Utils.database.AuthUsers import get_authorized_users
from Utils.MakeUID import MakeUID
from Utils.GetTime import GetTime
from Utils.bot.ChannelAutoRol import GetAllMembers
from Utils.GetEarlyTime import GetEarlyTime
from Utils.GetIndex import GetIndex
from Utils.GlobalVar import HelpList,v1patchnote,current_version
from Utils.bot.Actions import GetActions
from Utils.database.GetBans import GetBans
from dotenv import load_dotenv, dotenv_values

load_dotenv(".env")

databaseUrl = "https://db-wanab-default-rtdb.europe-west1.firebasedatabase.app/"

cred_file = os.getenv("Certificate")
token = os.getenv("TokenBot")

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())
        
async def StartListening():

    while True:
        await GetAllMembers(bot)
        await asyncio.sleep(0.2)

allowed_users = []
Owner = "ivanlr._1_45557"

@bot.event
async def on_ready():
    global allowed_users
    try:
        cred = credentials.Certificate(json.loads(cred_file))
        firebase_admin.initialize_app(cred, {"databaseURL" : databaseUrl})
        #db.reference("/AuthorizedUsers").update({1153415324591476887 : {"name":"ivanlr._1_45557"}})
        allowed_users = get_authorized_users()
        synced = await bot.tree.sync()
        await StartListening()
    except Exception as e:
        channel = bot.get_channel(1202999872983273508)
        embed = discord.Embed(title="PUNISHMENT BOT",color=discord.Color.red())
        embed.add_field(name="PUNISHMENT ERROR",value=f"FAILED TO SYNC TREE COMMAND OR LOGIN TO DATABASE! ERROR : {e}")
        await channel.send(embed=embed)

@bot.command()
async def debug(ctx):
    await GetActions(bot)
    await ctx.send("executed")

@bot.command()
async def AddAuthorizedUser(ctx, username):
    if str(ctx.author) != Owner:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    member = discord.utils.get(ctx.guild.members, name=str(username))
    if member:
        id = member.id
        if db.reference(f"/AuthorizedUsers/{id}").get() != None:
            embed = discord.Embed(title="Add Authorized User function",color=discord.Color.orange())
            embed.add_field(name="USER",value=username)
            embed.add_field(name="Error",value="Username is already a Authorized user!")
            await ctx.send(embed=embed)
            return
        try:
            db.reference("/AuthorizedUsers").update({id : {'name': username}})
            embed = discord.Embed(title="Add Authorized User function",color=discord.Color.green())
            embed.add_field(name="USER",value=username)
            embed.add_field(name="DATABASE STATUS",value=f"Succesfully added to database!")
            await ctx.send(embed=embed)
            return
        except Exception as e:
            embed = discord.Embed(title="Add Authorized User function",color=discord.Color.red())
            embed.add_field(name="USER",value=username)
            embed.add_field(name="Error",value=f"Error while adding to database error : {e}")
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(title="Add Authorized User function",color=discord.Color.red())
        embed.add_field(name="USER",value=username)
        embed.add_field(name="Error",value=f"User {username} does not exist in discord server")
        await ctx.send(embed=embed)
        return
    

@bot.tree.command(name="searchforpunishment",description="Search for a punishment with tribe name/tribe id/uid")
async def searchforpunishment(interaction : discord.Interaction, name_id_uid : str):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    alldata = db.reference("/Punishments").get()
    UIDS = []
    
    try:
        alldata[name_id_uid]
        UID = name_id_uid
        embed = discord.Embed(title=alldata[UID]["Tribe Name"], color=discord.Color.greyple())
        embed.add_field(name="Names",value=alldata[UID]["Names"],inline=True)
        embed.add_field(name="Punishments",value=alldata[UID]["Punishment"],inline=True)
        embed.add_field(name="Steam IDs",value=alldata[UID]["Steam IDs"],inline=True)
        embed.add_field(name="Reason",value=alldata[UID]["Reason"],inline=True)
        embed.add_field(name="Warning Type",value=alldata[UID]["Warning_type"],inline=True)
        embed.add_field(name="Warnings",value=alldata[UID]["Warnings"],inline=True)
        embed.add_field(name="Time",value=alldata[UID]["Time"],inline=True)
        embed.set_footer(text=f"UID : {name_id_uid}")

        await interaction.response.send_message(embed=embed)
        return 
    except Exception as e:
        pass
    try:
        tribe_id = int(name_id_uid)

        embed = discord.Embed(title=tribe_id, color=discord.Color.greyple())
        warnings = 0
        UIDS = []
        found = False
        for UID in alldata:
            if alldata[UID]["Tribe ID"] == tribe_id:
                found = True
                warnings += 1
                embed.add_field(name=f"Warning {warnings}",value="",inline=False)
                embed.add_field(name="Tribe Name",value=alldata[UID]["Tribe Name"],inline=True)
                embed.add_field(name="Names",value=alldata[UID]["Names"],inline=True)
                embed.add_field(name="Punishments",value=alldata[UID]["Punishment"],inline=True)
                embed.add_field(name="Steam IDs",value=alldata[UID]["Steam IDs"],inline=True)
                embed.add_field(name="Reason",value=alldata[UID]["Reason"],inline=True)
                embed.add_field(name="Warning Type",value=alldata[UID]["Warning_type"],inline=True)
                embed.add_field(name="Warnings",value=alldata[UID]["Warnings"],inline=True)
                embed.add_field(name="Time",value=alldata[UID]["Time"],inline=True)
                UIDS.append(UID)
            elif alldata[UID]['Tribe Name'] == str(tribe_id):
                found = True
                warnings += 1
                embed.add_field(name=f"Warning {warnings}",value="",inline=False)
                embed.add_field(name="Tribe Name",value=alldata[UID]["Tribe Name"],inline=True)
                embed.add_field(name="Names",value=alldata[UID]["Names"],inline=True)
                embed.add_field(name="Punishments",value=alldata[UID]["Punishment"],inline=True)
                embed.add_field(name="Steam IDs",value=alldata[UID]["Steam IDs"],inline=True)
                embed.add_field(name="Reason",value=alldata[UID]["Reason"],inline=True)
                embed.add_field(name="Warning Type",value=alldata[UID]["Warning_type"],inline=True)
                embed.add_field(name="Warnings",value=alldata[UID]["Warnings"],inline=True)
                embed.add_field(name="Time",value=alldata[UID]["Time"],inline=True)
                UIDS.append(UID)

        if found == False:
            embed = discord.Embed(title=tribe_id,description=f"Couldn't find any warning related to : {tribe_id}",color=discord.Color.red())    
        else:
            UIDS = ', '.join(UIDS)
            embed.set_footer(text=f"UIDS : {UIDS} coded by Ivan")
    except:
        tribe_name = str(name_id_uid)
    
        embed = discord.Embed(title=tribe_name, color=discord.Color.greyple())
        warnings = 0
        UIDS = []
        found = False
        for UID in alldata:
            if str(alldata[UID]["Tribe Name"]).lower() == tribe_name.lower():
                found = True
                warnings += 1
                embed.add_field(name=f"Warning {warnings}",value="",inline=False)
                embed.add_field(name="Tribe ID",value=alldata[UID]["Tribe ID"],inline=True)
                embed.add_field(name="Punishments",value=alldata[UID]["Punishment"],inline=True)
                embed.add_field(name="Steam IDs",value=alldata[UID]["Steam IDs"],inline=True)
                embed.add_field(name="Reason",value=alldata[UID]["Reason"],inline=True)
                embed.add_field(name="Warning Type",value=alldata[UID]["Warning_type"],inline=True)
                embed.add_field(name="Warnings",value=alldata[UID]["Warnings"],inline=True)
                embed.add_field(name="Time",value=alldata[UID]["Time"],inline=True)
                UIDS.append(UID)

        if found == False:
            embed = discord.Embed(title=tribe_name,description=f"Couldn't find any warning related to : {tribe_name}",color=discord.Color.red())    
        else:
            UIDS = ', '.join(UIDS)
            embed.set_footer(text=f"UIDS : {UIDS} coded by Ivan")
    await interaction.response.send_message(embed=embed)

@bot.command()
async def reload(ctx):
    global allowed_users
    allowed_users = get_authorized_users()
    embed = discord.Embed(title="Authorized Users",color=discord.Color.blue())
    for name in allowed_users:
        embed.add_field(name="NAME",value=name)

    await ctx.send(embed=embed)

@bot.tree.command(name="help",description="Print help list")
async def help(interaction : discord.Interaction):
    embed = discord.Embed(title="Help",color=discord.Color.green())
    embed.add_field(name="Commands",value=HelpList)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="patchnotes",description="Print patchnotes")
async def patchnotes(interaction : discord.Interaction):
    embed = discord.Embed(title=current_version, color=discord.Color.dark_orange())
    embed.add_field(name="Version v1.2.5",value=v1patchnote,inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="getbans",description="Send all banned users")
async def getbans(interaction : discord.Interaction):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    bansUID = GetBans()
    alldata = db.reference("/Punishments").get()

    embed = discord.Embed(title=f"BANS",color=discord.Color.red())
    ban = 0
    for uid in alldata:
        embed.add_field(name=f"BAN {ban}",value="",inline=False)
        embed.add_field(name=f"Name",value=alldata[uid]['Names'],inline=True)
        ban += 1
    bansUID = ', '.join(bansUID)
    embed.set_footer(text=f"UIDS : {bansUID}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="earlypunishment",description="Send the earlier punishment registered")
async def earlypunishment(interaction : discord.Interaction):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    times = []
    uids = []
    alldata = db.reference("/Punishments").get()
    for uid in alldata:
        time =alldata[uid]['Time']
        time = time.replace("/"," ")
        time = time.replace(":"," ")
        times.append(time)
        uids.append(uid)
    
    earlyTime = GetEarlyTime(times)
    index = 0

    index = GetIndex(earlyTime, times)
    
    data = alldata[uids[index]]

    embed = discord.Embed(title=data["Tribe Name"],description=f"Date : {data['Time']}",color=discord.Color.green())
    embed.add_field(name="Tribe ID",value=data['Tribe ID'],inline=True)
    embed.add_field(name="Names",value=data['Names'],inline=True)
    embed.add_field(name="Steam IDs",value=data['Steam IDs'],inline=True)
    embed.add_field(name="Warning Type",value=data['Warning_type'],inline=True)
    embed.add_field(name="Warnings",value=data['Warnings'],inline=True)
    embed.add_field(name="Reason",value=data['Reason'],inline=True)
    embed.add_field(name="Punishment",value=data['Punishment'],inline=True)
    embed.set_footer(text=f"UID : {uids[index]}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="removepunishment", description="remove a punishment trought uid")
async def removepunishment(interaction : discord.Interaction, warning_uid : str):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    if db.reference(f"/Punishments/{warning_uid}").get() == None:
        embed = discord.Embed(title="Invalid UID provided",description="Invalid UID was provided, if you think this was an error please contact ivanlr._1_45557 providing the UID so he can remove it manually!",color=discord.Color.red())

        await interaction.response.send_message(embed=embed)
    else:
        ref = db.reference(f"/Punishments/{warning_uid}")
        ref2 = db.reference(f"/Punishments/{warning_uid}").get()
        try:
            tribe_name = ref2['Tribe Name']
            tribe_Punish = ref2['Punishment']
            Reason = ref2['Reason']
            ref.delete()
            embed = discord.Embed(title=f"Removed {warning_uid} from database!",color=discord.Color.green())
            embed.add_field(name="Tribe Name",value=tribe_name,inline=False)
            embed.add_field(name="Punishment",value=tribe_Punish,inline=False)
            embed.add_field(name="Reason",value=Reason,inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error while deleting warning from database!",description=f"Error : {e}, please contact ivanlr._1_45557 with a screenshot! ")
            await interaction.response.send_message(embed=embed)

@bot.tree.command(name="totalwarnings",description="Gives total warnings from a tribe")
async def totalwarnings(interaction : discord.Interaction, tribe_name : str):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    alldata = db.reference("/Punishments").get()

    Seasonal = 0
    Permanent = 0
    Verbal = 0

    for UID in alldata:
        if str(alldata[UID]['Tribe Name']).lower() == tribe_name.lower():
            if alldata[UID]['Warning_type'] == "Seasonal Warning":
                Seasonal += alldata[UID]['Warnings']
            elif alldata[UID]['Warning_type'] == "Permanent Warning":
                Permanent += alldata[UID]['Warnings']
            elif alldata[UID]['Warning_type'] == "Verbal Warning":
                Verbal += alldata[UID]['Warnings']
    
    embed = discord.Embed(title=tribe_name, color=discord.Color.green())
    embed.add_field(name="Seasonal Warnings",value=Seasonal,inline=True)
    embed.add_field(name="Permanent Warnings",value=Permanent,inline=True)
    embed.add_field(name="Verbal Warnings",value=Verbal,inline=True)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="wipeseasonalwarnings",description="Wipe all seasonal warnings")
async def wipeseasonalwarnings(interaction : discord.Interaction):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    alldata = db.reference("/Punishments").get()
    channel_id = interaction.channel_id

    channel = bot.get_channel(channel_id)

    embed = discord.Embed(title="Wiping Seasonal warnings...",description=f"```Fetching all seasonal warnings...```",color=discord.Color.greyple())
    await interaction.response.send_message("Starting...")
    uid_to_delete =[]
    msj = await channel.send(embed=embed)
    await asyncio.sleep(1)
    start = time.time()
    for uid in alldata:
        if alldata[uid]['Warning_type'] == "Seasonal Warning":
            embed = discord.Embed(title="Fetching seasonal warnings...",description=f"```Fetched : {uid}```",color=discord.Color.orange())
            await msj.edit(embed=embed)
            uid_to_delete.append(uid)
            await asyncio.sleep(0.2)

    embed = discord.Embed(title="Fetched all seasonal warnings",description=f"```Fetched : {len(uid_to_delete)} warnings on {round(time.time() - start,2)}```",color=discord.Color.green())
    await msj.edit(embed=embed)
    await asyncio.sleep(1)
    for uid in uid_to_delete:
        try:
            ref = db.reference(f"Punishments/{uid}")
            ref2 = db.reference(f"Punishments/{uid}").get()
            ref.delete()
            Tribe_name = ref2['Tribe Name']
            embed = discord.Embed(title="Deleting",description=f"```Deleted : {uid} ({Tribe_name})``` ",color=discord.Color.green())
            await msj.edit(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Deleting",description=f"```Failed to delete : {uid}, error : {e}```",color=discord.Color.red())
            await msj.edit(embed=embed)
        await asyncio.sleep(1)
    
    embed = discord.Embed(title="Done",description="```Done```",color=discord.Color.green())
    await msj.edit(embed=embed)

@bot.tree.command(name="check", description="Check if an Id is in database")
async def check(interaction : discord.Interaction, id : str):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    alldata = db.reference("/Punishments").get()

    embed = discord.Embed(title="Id related",color=discord.Color.orange())
    
    warnings = 0

    UIDS = []

    for uid in alldata:
        ids = alldata[uid]['Steam IDs']
        splited_ids = str(ids).split("|")
        index = 0
        for check_id in splited_ids:
            if check_id == id:
                warnings += 1
                Names = alldata[uid]['Names']
                Warnings = alldata[uid]['Warnings']
                Warning_type = alldata[uid]['Warning_type']
                Date = alldata[uid]['Time']
                splited_names = str(Names).split("|")
                name = splited_names[index]
                embed.add_field(name=f"",value=f"```Warning {warnings}```",inline=False)
                embed.add_field(name=f"ID",value=id,inline=True)
                embed.add_field(name=f"Name",value=name,inline=True)
                embed.add_field(name=f"Warnings",value=Warnings,inline=True)
                embed.add_field(name=f"Warning Type",value=Warning_type,inline=True)
                embed.add_field(name=f"Date",value=Date,inline=True)
                UIDS.append(uid)
            else:
                index += 1
    
    if warnings > 0:

        UIDS = ', '.join(UIDS)
        
        embed.set_footer(text=f"Uid(s) : {UIDS} , coded by Ivan")
    else:
        embed.add_field(name=f"",value=f"```Cannot find ID : {id} in punishments```",inline=False)
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="punishment",description="Make a punishment")
async def punishment(interaction : discord.Interaction,steam_ids : str,names : str,tribe_name : str,tribe_id : int, warning_type : str, warnings : int,reason : str, punishment : str, proof : str):
    global allowed_users
    name = interaction.user.name
    if str(name) not in allowed_users:
        embed = discord.Embed(title="Error",description="You are not allowed to use this command!",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    try:
        uid = MakeUID()
        while True:
            if db.reference(f"/Punishments/{uid}").get() == None:
                break
        date = GetTime()

        db.reference("/Punishments").update({uid : {"Tribe Name":tribe_name,"Names":names, "Tribe ID" : tribe_id, "Steam IDs" : steam_ids,"Reason":reason, "Warning_type":warning_type, 'Warnings':warnings, 'Punishment':punishment, 'Proof':proof, 'Time':date}})

        embed = discord.Embed(title="PUNISH",color=discord.Color.orange())
        embed.add_field(name="Tribe ID",value=tribe_id,inline=False)
        embed.add_field(name="Tribe Name",value=tribe_name,inline=False)
        embed.add_field(name="Names",value=names,inline=False)
        embed.add_field(name="Steam IDs",value=steam_ids,inline=False)
        embed.add_field(name="Warning Type",value=warning_type,inline=False)
        embed.add_field(name="Warnings",value=warnings,inline=False)
        embed.add_field(name="Reason",value=reason,inline=False)
        embed.add_field(name="Punishment",value=punishment,inline=False)
        embed.add_field(name="Proof",value=proof,inline=False)
        embed.add_field(name="DATABASE STATUS",value="Succesfully added to database",inline=False)
        embed.set_thumbnail(url="https://th.bing.com/th/id/R.a1849d676a332b5516f3dd3cf3d90609?rik=XwaA15sdUDGrag&riu=http%3a%2f%2fwww.freepngimg.com%2fdownload%2fgreen_tick%2f27880-5-green-tick-clipart.png&ehk=23wDe1sjBvA6xbwbaYRnxtE0tnwNzqbafc3L5kmYcms%3d&risl=&pid=ImgRaw&r=0")
        embed.set_footer(text=f"UID : {uid}, coded by Ivan")
        await interaction.response.send_message(embed=embed)
        return
    except Exception as e:
        embed = discord.Embed(title="PUNISHMENT FUNCTION",color=discord.Color.red())
        embed.add_field(name="DATABASE FATAL ERROR",value=f"Error : {e}")
        await interaction.response.send_message(embed=embed)
        return

@punishment.autocomplete("warning_type")
async def autocomplete(interaction : discord.Interaction, current : str) -> typing.List[app_commands.Choice[str]]:
    data = []
    for options in ["Seasonal Warning","Permanent Warning","Verbal Warning"]:
        data.append(app_commands.Choice(name=options,value=options)) 
    return data 

@punishment.autocomplete("warnings")
async def warn_autocomplete(interaction : discord.Interaction, current: int) -> typing.List[app_commands.Choice[int]]:
    data = []
    for number in [1,2,3,4,5]:
        data.append(app_commands.Choice(name=number,value=number))
    
    return data



bot.run(token)
