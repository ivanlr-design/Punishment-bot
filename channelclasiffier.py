from discord.ext import commands
import discord
from discord import app_commands
import time
bot = commands.Bot(command_prefix="-",intents=discord.Intents.all())

token = 'HERE YOUR TOKEN'
meshticketId = 1205818053397315634
meshStructuresId = 1205821986706690049
ticketsId = 1205817944240824331
InsidingId = 1205822408955789353
HacksId = 1205822384872095764
OtherId = 1205824013012570163
OverspamId = 1205831054854852639

rapidtime = 0.5

async def CheckChannels():
    meshTicket = 0
    Struct = 0
    Insiding = 0
    Hacks = 0
    Other = 0
    Overspam = 0
    start = time.time()
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.category:
                if channel.category.id  == ticketsId:
                    if "mesh" in channel.name and "struc" not in channel.name:
                        categoria = discord.utils.get(guild.categories, id=meshticketId)
                        await channel.edit(category=categoria)
                        meshTicket += 1
                    elif "mesh" in channel.name and "struc" in channel.name:
                        categoria = discord.utils.get(guild.categories, id=meshStructuresId)
                        await channel.edit(category=categoria)
                        Struct += 1
                    elif "insid" in channel.name:
                        categoria = discord.utils.get(guild.categories, id=InsidingId)
                        await channel.edit(category=categoria)
                        Insiding += 1
                    elif "hacks" in channel.name:
                        categoria = discord.utils.get(guild.categories, id=HacksId)
                        await channel.edit(category=categoria)
                        Hacks += 1
                    elif "other" in channel.name:
                        categoria = discord.utils.get(guild.categories, id=OtherId)
                        await channel.edit(category=categoria)
                        Other += 1
                    elif "overspam" in channel.name:
                        categoria = discord.utils.get(guild.categories, id=OverspamId)
                        await channel.edit(category=categoria)
                        Overspam += 1
            
    
                time.sleep(rapidtime)
    
    return meshTicket, Struct, Insiding, Hacks, Other, Overspam, round(time.time() - start,2)

    
@bot.event
async def on_ready():
    pass

@bot.command()
async def order(ctx):
    meshTicket, Struct, Insiding, Hacks, Other, Overspam, Took = await CheckChannels()
    embed = discord.Embed(title="Ticket Order",description=f"Total Tickets ordered : {meshTicket + Struct + Insiding + Hacks + Other}",color=discord.Color.green())
    embed.add_field(name=f"Mesh tickets ordered",value=meshTicket)
    embed.add_field(name=f"Mesh Structures tickets ordered",value=Struct)
    embed.add_field(name=f"Insiding tickets ordered",value=Insiding)
    embed.add_field(name=f"Hacks tickets ordered",value=Hacks)
    embed.add_field(name=f"Other tickets ordered",value=Other)
    embed.add_field(name=f"Overspam tickets ordered",value=Overspam)
    embed.add_field(name=f"Took",value=f"{Took}s")
    await ctx.send(embed=embed)

@bot.command()
async def TakenTime(ctx, numOne: float):
    global rapidtime
    embed = discord.Embed(title="Taken Time",description=f"{rapidtime} -> {numOne}",color=discord.Color.green())
    rapidtime = numOne
    await ctx.send(embed=embed)

bot.run(token)