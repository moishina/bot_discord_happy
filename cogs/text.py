import discord
from discord import app_commands
from discord.ext import commands
import random

class Text(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        
# envia o texto que for digitado no campo
    @app_commands.command(name="text", description='Envia o texto que for digitado como Happy')   
    async def text(self, interact:discord.Interaction, texto:str):
        await interact.response.send_message(texto)    
        
 
 
 
async def setup(bot):
    await bot.add_cog(Text(bot))