import discord
from discord import app_commands
from discord.ext import commands
import random

class Amimir(commands.Cog):
    def __init__(self, bot): #função q vai iniciar qnd for chamada
        self.bot = bot
        super().__init__()
        

    @app_commands.command(name="amimir", description="Happy a mimir")   
    async def amimir(self, interaction: discord.Interaction):
        gifs_amimir = ["https://i.pinimg.com/originals/d6/39/40/d639408ae1f0365b63d5afbfb4d5a6a4.gif",
            "https://media.tenor.com/m/VySTk2IGD9wAAAAd/fairy-tail-sleeping.gif"]
        
        gif_escolhido = random.choice(gifs_amimir)

        embed = discord.Embed(

            color=discord.Color.from_rgb(158, 242, 255)
        )
        embed.set_image(url=gif_escolhido)

        # envia a resposta e salva a mensagem retornada
        await interaction.response.send_message(embed=embed)
        response = await interaction.original_response()

        # reage com emoji a mimir
        await response.add_reaction("😴")   
        
 
 
 
async def setup(bot):
    await bot.add_cog(Amimir(bot))