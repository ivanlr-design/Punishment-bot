import discord
from firebase_admin import db
from discord.ext import commands

class BanPage(discord.ui.View):
    current_page : int = 1
    sep : int = 5
    
    async def send(self, ctx):
        self.msj = await ctx.send(view=self)
        self.UIDS = []
        self.data = []
        self.appendbans()
        await self.update_embed(self.data[:self.sep])
    
    def appendbans(self):
        alldata = db.reference("/Punishments").get()

        for uid in alldata:
            if 'ban' in alldata[uid]['Punishment'].lower():
                embed = discord.Embed(title="BAN",description=alldata[uid]['Names'])
                embed.add_field(name="When banned",value=alldata[uid]['Time'],inline=True)
                embed.add_field(name="Reason",value=alldata[uid]['Reason'],inline=True)
                embed.set_footer(text=f"UID : {uid}")
                self.data.append(embed)
        
        alldata = db.reference("/TempBans").get()

        
    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
        else:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
        

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
        else:
            self.next_button.disabled = True
            self.last_page_button.disabled = True

    async def update_embed(self, data):
        self.update_buttons()
        await self.msj.edit(embeds=data) 

    @discord.ui.button(label="|<",style=discord.ButtonStyle.primary)
    async def first_page_button(self, button : discord.ui.Button, interaction : discord.Interaction, ):
        await interaction.response.defer()
        self.current_page = 1
        final = self.sep * self.current_page
        inicio = final - self.sep
        await self.update_embed(self.data[inicio:final])
    
    @discord.ui.button(label="⬅️",style=discord.ButtonStyle.primary)
    async def prev_button(self, button : discord.ui.Button, interaction : discord.Interaction):
        await interaction.response.defer()
        self.current_page -= 1
        final = self.sep * self.current_page
        inicio = final - self.sep
        await self.update_embed(self.data[inicio:final])

    @discord.ui.button(label="➡️",style=discord.ButtonStyle.primary)
    async def next_button(self,button : discord.ui.Button, interaction : discord.Interaction, ):
        await interaction.response.defer()
        self.current_page += 1
        final = self.sep * self.current_page
        inicio = final - self.sep
        await self.update_embed(self.data[inicio:final])
    

    @discord.ui.button(label=">|",style=discord.ButtonStyle.primary)
    async def last_page_button(self, button : discord.ui.Button , interaction : discord.Interaction):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep) + 1
        final = self.sep * self.current_page
        inicio = final - self.sep
        await self.update_embed(self.data[inicio:final])